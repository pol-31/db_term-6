import threading
import schedule
import time
import socket
import os
import json

import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import redis

from forms import *

from db_config import *

import db_init
import db_backup

from db_class_model import *
from model_sqlalchemy import *
from model_mongodb import *

backup_file = '../backups/backup_file.dump'
schedule.every().day.at("02:00").do(db_backup.create_backup, backup_file)


conn = db_init.connect_to_db()

scheduler_thread = threading.Thread(target=db_backup.run_scheduler)
scheduler_thread.start()


if os.getenv('DB_DO_INIT') == 'False':
    conn = db_backup.restore_backup(conn, backup_file, do_db_init=False)
else:
    conn = db_backup.restore_backup(conn, backup_file)
    conn = db_init.execute_querries(conn)
  

conn.commit()

db_init.timer()
db_backup.create_backup(backup_file)
print("Backup created --> \t{};".format(db_init.timer()), flush=True)

conn.commit()
conn.close()

HOST = 'flyway'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
    send_socket.connect((HOST, PORT))
    send_socket.sendall(b'Main table is ready for migration')
    send_socket.shutdown(socket.SHUT_RDWR)
     
# waiting until the migration will be completed
HOST = 'app'
PORT = 3000
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receive_socket:
    receive_socket.bind((HOST, PORT))
    receive_socket.listen(1)

    client_socket, address = receive_socket.accept()
       
    client_socket.close()
    receive_socket.shutdown(socket.SHUT_RDWR)
    
print("Flask-migration completed --> \t{};".format(db_init.timer()), flush=True)


conn = db_init.connect_to_db()
conn.close()


db.reflect()
db.create_all()

print("Migration to SQLAlchemy completed --> \t{};".format(db_init.timer()), flush=True)

# -- MIGRATE TO MONGODB (...)

postgres_regions = db.session.query(ormTblZnoRegion).all()
for region in postgres_regions:
    collZnoRegion.create(region.id, region.reg, region.area, region.ter)

postgres_reg_regions = db.session.query(ormTblZnoRegRegion).all()
for reg_region in postgres_reg_regions:
    collZnoRegRegion.create(reg_region.id, reg_region.ter_type, reg_region.fk_region)

postgres_eos = db.session.query(ormTblZnoEO).all()
for eo in postgres_eos:
        collZnoEO.create(eo.id, eo.name, eo.type, eo.parent, eo.fk_region)

postgres_pts = db.session.query(ormTblZnoPT).all()
for pt in postgres_pts:
        collZnoPT.create(pt.id, pt.name, pt.fk_region)

postgres_students = db.session.query(ormTblZnoStudent).all()
for student in postgres_students:
    collZnoStudent.create(student.id, student.birth, student.sex, student.status,
                            student.class_profile, student.class_lang, student.fk_student_reg,
                            student.fk_eo)

postgres_subjects = db.session.query(ormTblZnoSubject).all()
for subject in postgres_subjects:
    collZnoSubject.create(subject.id, subject.name)

postgres_marks = db.session.query(ormTblZnoMarks).all()
for mark in postgres_marks:
    collZnoMarks.create(mark.fk_student_id, mark.fk_subject, mark.fk_pt, mark.test,
                          mark.test_status, mark.ball100, mark.ball12, mark.ball,
                          mark.adapt_scale, mark.lang, mark.dpa)
                          
print("Migration to MongoDb completed --> \t{};".format(db_init.timer()), flush=True)
#-------------------------

redis_client = redis.Redis(host='redis', port=6379)

db_mongo = DatabaseMongo(mongo_db)
db_postgre = DatabasePostgre(db)

cur_db = db_postgre

      
@app.route('/switch_db', methods=['GET'])
def switch_db():
    global cur_db, db_mongo, db_postgre
    cur_db = db_postgre if (cur_db.name == "mongo") else db_mongo
    return 'Switched successfully'
    

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html', bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/student', methods=['GET'])
def student():
    global cur_db
    cached_data = redis_client.get('student_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoStudent, 50)

    rendered_template = render_template('student.html', students=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('student_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    global cur_db
    form = studentForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            
            cur_db.add(ZnoStudent, form)
            
            redis_client.delete('student_data_{}'.format(cur_db.name))
            
            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    global cur_db
    form = studentForm()

    if request.method == 'GET':

        id = request.args.get('student_id')
        
        student = cur_db.get_by_id(ZnoStudent, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoStudent):
            getattr(form, attr).data = cur_db.get_value(student, attr)

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
                    
            cur_db.update(ZnoStudent, {"id":form.id.data}, form)

            redis_client.delete('student_data_{}'.format(cur_db.name))
            
            return redirect(url_for('student'))


@app.route('/delete_student', methods=['POST'])
def delete_student():
    global cur_db
    id = request.form['student_id']
    
    cur_db.delete(ZnoStudent, {"id":id})
    
    redis_client.delete('student_data_{}'.format(cur_db.name))
    
    return id

    
@app.route('/marks', methods=['GET'])
def marks():
    global cur_db
    cached_data = redis_client.get('marks_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')
        
    result = cur_db.get(ZnoMarks, 50)

    rendered_template = render_template('marks.html', markss=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('marks_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_marks', methods=['GET', 'POST'])
def new_marks():
    global cur_db
    form = marksForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('marks_form.html', form=form, form_name="New marks", action="new_marks", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
        
            cur_db.add(ZnoMarks, form)

            redis_client.delete('marks_data_{}'.format(cur_db.name))

            return redirect(url_for('marks'))

    return render_template('marks_form.html', form=form, form_name="New marks", action="new_marks", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_marks', methods=['GET', 'POST'])
def edit_marks():
    global cur_db
    form = marksForm()

    if request.method == 'GET':
        student_id = request.args.get('fk_student_id')
        subject_id = int(request.args.get('fk_subject'))
        
                
        marks = cur_db.get_by_id(ZnoMarks, {
            "fk_student_id":student_id,
            "fk_subject":subject_id
        })
        
        for attr in cur_db.get_attrs(ZnoMarks):
            getattr(form, attr).data = cur_db.get_value(marks, attr)


        return render_template('marks_form.html', form=form, form_name="Edit marks", action="edit_marks", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('marks_form.html', form=form, form_name="Edit marks", action="edit_marks", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:    
            
            cur_db.update(ZnoMarks, {
                "fk_student_id":form.fk_student_id.data,
                "fk_subject":int(form.fk_subject.data)}, form)


            redis_client.delete('marks_data_{}'.format(cur_db.name))

            return redirect(url_for('marks'))


@app.route('/delete_marks', methods=['POST'])
def delete_marks():
    global cur_db
    student_id = request.form['fk_student_id']
    subject_id = int(request.form['fk_subject'])
        
    cur_db.delete(ZnoMarks, {
                "fk_student_id":student_id,
                "fk_subject":subject_id})

    redis_client.delete('marks_data_{}'.format(cur_db.name))

    return { "fk_student_id": student_id,
             "fk_subject": subject_id }
    

@app.route('/subject', methods=['GET'])
def subject():
    global cur_db
    cached_data = redis_client.get('subject_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoSubject, 50)

    rendered_template = render_template('subject.html', subjects=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('subject_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    global cur_db
    form = subjectForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            form.id.data = cur_db.get_new_id(ZnoSubject)
                            
            cur_db.add(ZnoSubject, form)

            redis_client.delete('subject_data_{}'.format(cur_db.name))

            return redirect(url_for('subject'))

    return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_subject', methods=['GET', 'POST'])
def edit_subject():
    global cur_db
    form = subjectForm()

    if request.method == 'GET':

        id = int(request.args.get('subject_id'))
        
        subject = cur_db.get_by_id(ZnoSubject, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoSubject):
            getattr(form, attr).data = cur_db.get_value(subject, attr)

        return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
                    
            cur_db.update(ZnoSubject, {"id":int(form.id.data)}, form)

            redis_client.delete('subject_data_{}'.format(cur_db.name))

            return redirect(url_for('subject'))


@app.route('/delete_subject', methods=['POST'])
def delete_subject():
    global cur_db
    id = request.form['subject_id']
    
    cur_db.delete(ZnoSubject, {"id":int(id)})

    redis_client.delete('subject_data_{}'.format(cur_db.name))

    return id
    
@app.route('/region', methods=['GET'])
def region():
    global cur_db
    cached_data = redis_client.get('region_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoRegion, 50)

    rendered_template = render_template('region.html', regions=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('region_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_region', methods=['GET', 'POST'])
def new_region():
    global cur_db
    form = regionForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('region_form.html', form=form, form_name="New region", action="new_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            form.id.data = cur_db.get_new_id(ZnoRegion)
                            
            cur_db.add(ZnoRegion, form)

            redis_client.delete('region_data_{}'.format(cur_db.name))

            return redirect(url_for('region'))

    return render_template('region_form.html', form=form, form_name="New region", action="new_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_region', methods=['GET', 'POST'])
def edit_region():
    global cur_db
    form = regionForm()

    if request.method == 'GET':

        id = int(request.args.get('region_id'))
        
        region = cur_db.get_by_id(ZnoRegion, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoRegion):
            getattr(form, attr).data = cur_db.get_value(region, attr)

        return render_template('region_form.html', form=form, form_name="Edit region", action="edit_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('region_form.html', form=form, form_name="Edit region", action="edit_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
                    
            cur_db.update(ZnoRegion, {"id":int(form.id.data)}, form)

            redis_client.delete('region_data_{}'.format(cur_db.name))

            return redirect(url_for('region'))


@app.route('/delete_region', methods=['POST'])
def delete_region():
    global cur_db
    id = request.form['region_id']
    
    cur_db.delete(ZnoRegion, {"id":int(id)})

    redis_client.delete('region_data_{}'.format(cur_db.name))

    return id
    

@app.route('/eo', methods=['GET'])
def eo():
    global cur_db
    cached_data = redis_client.get('eo_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoEO, 50)

    rendered_template = render_template('eo.html', eos=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('eo_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_eo', methods=['GET', 'POST'])
def new_eo():
    global cur_db
    form = eoForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('eo_form.html', form=form, form_name="New eo", action="new_eo", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            form.id.data = cur_db.get_new_id(ZnoEO)
                            
            cur_db.add(ZnoEO, form)

            redis_client.delete('eo_data_{}'.format(cur_db.name))

            return redirect(url_for('eo'))

    return render_template('eo_form.html', form=form, form_name="New eo", action="new_eo", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_eo', methods=['GET', 'POST'])
def edit_eo():
    global cur_db
    form = eoForm()

    if request.method == 'GET':

        id = int(request.args.get('eo_id'))
        
        eo = cur_db.get_by_id(ZnoEO, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoEO):
            getattr(form, attr).data = cur_db.get_value(eo, attr)
            
        return render_template('eo_form.html', form=form, form_name="Edit eo", action="edit_eo", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('eo_form.html', form=form, form_name="Edit eo", action="edit_eo", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
                    
            cur_db.update(ZnoEO, {"id":int(form.id.data)}, form)

            redis_client.delete('eo_data_{}'.format(cur_db.name))

            return redirect(url_for('eo'))


@app.route('/delete_eo', methods=['POST'])
def delete_eo():
    global cur_db
    id = request.form['eo_id']
    
    cur_db.delete(ZnoEO, {"id":int(id)})

    redis_client.delete('eo_data_{}'.format(cur_db.name))

    return id
    
    
@app.route('/pt', methods=['GET'])
def pt():
    global cur_db
    cached_data = redis_client.get('pt_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoPT, 50)

    rendered_template = render_template('pt.html', pts=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('pt_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_pt', methods=['GET', 'POST'])
def new_pt():
    global cur_db
    form = ptForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('pt_form.html', form=form, form_name="New pt", action="new_pt", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            form.id.data = cur_db.get_new_id(ZnoPT)
                            
            cur_db.add(ZnoPT, form)
            
            redis_client.delete('pt_data_{}'.format(cur_db.name))

            return redirect(url_for('pt'))

    return render_template('pt_form.html', form=form, form_name="New pt", action="new_pt", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_pt', methods=['GET', 'POST'])
def edit_pt():
    global cur_db
    form = ptForm()
    if request.method == 'GET':

        id = int(request.args.get('pt_id'))
        
        pt = cur_db.get_by_id(ZnoPT, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoPT):
            getattr(form, attr).data = cur_db.get_value(pt, attr)

        return render_template('pt_form.html', form=form, form_name="Edit pt", action="edit_pt", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('pt_form.html', form=form, form_name="Edit pt", action="edit_pt")
        else:
                    
            cur_db.update(ZnoPT, {"id":int(form.id.data)}, form)

            redis_client.delete('pt_data_{}'.format(cur_db.name))

            return redirect(url_for('pt'))


@app.route('/delete_pt', methods=['POST'])
def delete_pt():
    global cur_db
    id = request.form['pt_id']
    
    cur_db.delete(ZnoPT, {"id":int(id)})

    redis_client.delete('pt_data_{}'.format(cur_db.name))

    return id


@app.route('/reg_region', methods=['GET'])
def reg_region():
    global cur_db
    cached_data = redis_client.get('reg_region_data_{}'.format(cur_db.name))
    if cached_data:
        return cached_data.decode('utf-8')

    result = cur_db.get(ZnoRegRegion, 50)

    rendered_template = render_template('reg_region.html', reg_regions=result, bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

    redis_client.set('reg_region_data_{}'.format(cur_db.name), rendered_template)

    return rendered_template


@app.route('/new_reg_region', methods=['GET', 'POST'])
def new_reg_region():
    global cur_db
    form = regRegionForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('reg_region_form.html', form=form, form_name="New reg_region", action="new_reg_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
            form.id.data = cur_db.get_new_id(ZnoRegRegion)
                            
            cur_db.add(ZnoRegRegion, form)

            redis_client.delete('reg_region_data_{}'.format(cur_db.name))

            return redirect(url_for('reg_region'))

    return render_template('reg_region_form.html', form=form, form_name="New reg_region", action="new_reg_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


@app.route('/edit_reg_region', methods=['GET', 'POST'])
def edit_reg_region():
    global cur_db
    form = regRegionForm()

    if request.method == 'GET':

        id = int(request.args.get('reg_region_id'))
        
        reg_region = cur_db.get_by_id(ZnoRegRegion, {"id":id})
        
        for attr in cur_db.get_attrs(ZnoRegRegion):
            getattr(form, attr).data = cur_db.get_value(reg_region, attr)
            
        return render_template('reg_region_form.html', form=form, form_name="Edit reg_region", action="edit_reg_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)


    else:

        if form.validate():
            return render_template('reg_region_form.html', form=form, form_name="Edit reg_region", action="edit_reg_region", bg_color=cur_db.bg_color, cur_db_name=cur_db.name)
        else:
                    
            cur_db.update(ZnoRegRegion, {"id":int(form.id.data)}, form)

            redis_client.delete('reg_region_data_{}'.format(cur_db.name))

            return redirect(url_for('reg_region'))


@app.route('/delete_reg_region', methods=['POST'])
def delete_reg_region():
    global cur_db
    id = request.form['reg_region_id']
    
    cur_db.delete(ZnoRegRegion, {"id":int(id)})

    redis_client.delete('reg_region_data_{}'.format(cur_db.name))

    return id
    

@app.route('/results', methods=['GET', 'POST'])
def results():
    global cur_db
    if request.method == 'POST':
        json_data = request.get_json()
        
        subjectValue = json_data.get('subject')
        yearValue = json_data.get('year')
        regionValue = json_data.get('region')
       

        subjectValue = int(subjectValue) if subjectValue is not None else 0
        yearValue = int(yearValue) if yearValue is not None else 0
        
        cached_subject = redis_client.get('querySubject_{}'.format(cur_db.name))
        cached_year = redis_client.get('queryYear_{}'.format(cur_db.name))
        cached_region = redis_client.get('queryRegion_{}'.format(cur_db.name))
        
        if (cached_subject is not None) and (cached_year is not None) and (cached_region is not None):
            if (cached_subject == subjectValue) and (cached_year == yearValue) and (cached_region == regionValue):
                return jsonify(redis_client.get('query_plot_data_{}'.format(cur_db.name)))
            else:
                redis_client.delete('query_plot_data_{}'.format(cur_db.name))
        else:
            redis_client.mset({
                'querySubject_{}'.format(cur_db.name): subjectValue,
                'queryYear_{}'.format(cur_db.name): yearValue,
                'queryRegion_{}'.format(cur_db.name): regionValue
            })
        

        avg_ball, reg = cur_db.make_query(regionValue, subjectValue, yearValue)

        bar = {
            'x': reg,
            'y': [float(x) for x in avg_ball],
            'type': 'bar'
        }

        pie = {
            'labels': reg,
            'values': [float(x) for x in avg_ball],
            'type': 'pie'
        }
    
        data = {
            'bar': [bar],
            'pie': [pie]
        }
        

        redis_client.set('query_plot_data_{}'.format(cur_db.name), json.dumps(data))
    
        return jsonify(data)
    else:
        return render_template('results.html', bg_color=cur_db.bg_color, cur_db_name=cur_db.name)

            
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
            

