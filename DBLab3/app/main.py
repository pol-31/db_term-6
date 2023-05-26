import threading
import schedule
import time
import socket
import os

import db_init
import db_backup

import json

import plotly
import plotly.graph_objs as go
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import redis

from orm_model import *
from forms import *

if __name__ == "__main__":
    backup_file = '../backups/backup_file.dump'
    schedule.every().day.at("02:00").do(db_backup.create_backup, backup_file)


    conn = db_init.connect_to_db()

    scheduler_thread = threading.Thread(target=db_backup.run_scheduler)
    scheduler_thread.start()


    # to create or not to create,
    # that is the question
    if os.getenv('DB_DO_INIT') == 'False':
        conn = db_backup.restore_backup(conn, backup_file, do_db_init=False)
    else:
        conn = db_backup.restore_backup(conn, backup_file)
        conn = db_init.execute_querries(conn)
  

    # creating backup file
    conn.commit()

    db_init.timer()
    db_backup.create_backup(backup_file)
    print("Backup created --> \t{};".format(db_init.timer()), flush=True)

    conn.commit()
    conn.close()

    print("\n--python script main.py is done--")


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

    print(">-- migration completed --<")



conn = db_init.connect_to_db()
conn.close()

app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dreamTeam:dreamTeam@db:5432/zno_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

db.reflect()
db.create_all()

redis_client = redis.Redis(host='redis', port=6379)

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/student', methods=['GET'])
def student():
    cached_data = redis_client.get('student_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoStudent).limit(50).all()

    rendered_template = render_template('student.html', students=result)

    redis_client.set('student_data', rendered_template)

    return rendered_template


@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = studentForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_student = ormTblZnoStudent(
                id=form.student_id.data,
                birth=form.student_birth.data,
                sex=form.student_sex.data,
                status=form.student_status.data,
                class_profile=form.student_class_profile.data,
                class_lang=form.student_class_lang.data,
                fk_student_reg=form.student_fk_student_reg.data,
                fk_eo=form.student_fk_eo.data
            )
            
            try:
                db.session.add(new_student)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")
            
            redis_client.delete('student_data')
            
            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
def edit_student():
    form = studentForm()

    if request.method == 'GET':

        id = request.args.get('student_id')
        student = db.session.query(ormTblZnoStudent).filter(ormTblZnoStudent.id == id).one()

        # fill form and send to user
        form.student_id.data = student.id
        form.student_birth.data = student.birth
        form.student_sex.data = student.sex
        form.student_status.data = student.status
        form.student_class_profile.data = student.class_profile
        form.student_class_lang.data = student.class_lang
        form.student_fk_student_reg.data = student.fk_student_reg
        form.student_fk_eo.data = student.fk_eo

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")


    else:

        if form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            # find student
            student = db.session.query(ormTblZnoStudent).filter(ormTblZnoStudent.id == form.student_id.data).one()

            # update fields from form data
            try:
                student.id=form.student_id.data
                student.birth=form.student_birth.data
                student.sex=form.student_sex.data
                student.status=form.student_status.data
                student.class_profile=form.student_class_profile.data
                student.class_lang=form.student_class_lang.data
                student.fk_student_reg=form.student_fk_student_reg.data
                student.fk_eo=form.student_fk_eo.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('student_data')
            
            return redirect(url_for('student'))


@app.route('/delete_student', methods=['POST'])
def delete_student():
    id = request.form['student_id']

    result = db.session.query(ormTblZnoStudent).filter(ormTblZnoStudent.id == id).one()
    
    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")
    
    redis_client.delete('student_data')
    
    return id
    
    
@app.route('/marks', methods=['GET'])
def marks():
    cached_data = redis_client.get('marks_data')
    if cached_data:
        return cached_data.decode('utf-8')
        
    result = db.session.query(ormTblZnoMarks).limit(50).all()

    rendered_template = render_template('marks.html', markss=result)

    redis_client.set('marks_data', rendered_template)

    return rendered_template


@app.route('/new_marks', methods=['GET', 'POST'])
def new_marks():
    form = marksForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('marks_form.html', form=form, form_name="New marks", action="new_marks")
        else:
            new_marks = ormTblZnoMarks(
                fk_student_id=form.marks_fk_student_id.data,
                fk_subject=form.marks_fk_subject.data,
                fk_pt=form.marks_fk_pt.data,
                test=form.marks_test.data,
                test_status=form.marks_test_status.data,
                ball100=form.marks_ball100.data,
                ball12=form.marks_ball12.data,
                ball=form.marks_ball.data,
                adapt_scale=form.marks_adapt_scale.data,
                lang=form.marks_lang.data,
                dpa=form.marks_dpa.data
            )
            
            try:
                db.session.add(new_marks)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('marks_data')

            return redirect(url_for('marks'))

    return render_template('marks_form.html', form=form, form_name="New marks", action="new_marks")


@app.route('/edit_marks', methods=['GET', 'POST'])
def edit_marks():
    form = marksForm()

    if request.method == 'GET':
        student_id = request.args.get('marks_fk_student_id')
        subject_id = request.args.get('marks_fk_subject')
        
        marks = db.session.query(ormTblZnoMarks).filter(
            ormTblZnoMarks.fk_student_id == student_id,
            ormTblZnoMarks.fk_subject == subject_id
        ).one()

        form.marks_fk_student_id.data = marks.fk_student_id
        form.marks_fk_subject.data = marks.fk_subject
        form.marks_fk_pt.data = marks.fk_pt
        form.marks_test.data = marks.test
        form.marks_test_status.data = marks.test_status
        form.marks_ball100.data = marks.ball100
        form.marks_ball12.data = marks.ball12
        form.marks_ball.data = marks.ball
        form.marks_adapt_scale.data = marks.adapt_scale
        form.marks_lang.data = marks.lang
        form.marks_dpa.data = marks.dpa

        return render_template('marks_form.html', form=form, form_name="Edit marks", action="edit_marks")


    else:

        if form.validate():
            return render_template('marks_form.html', form=form, form_name="Edit marks", action="edit_marks")
        else:
            marks = db.session.query(ormTblZnoMarks).filter(
                ormTblZnoMarks.fk_student_id == form.marks_fk_student_id.data,
                ormTblZnoMarks.fk_subject == form.marks_fk_subject.data
            ).one()

            try:
                marks.fk_student_id=form.marks_fk_student_id.data
                marks.fk_subject=form.marks_fk_subject.data
                marks.fk_pt=form.marks_fk_pt.data
                marks.test=form.marks_test.data
                marks.test_status=form.marks_test_status.data
                marks.ball100=form.marks_ball100.data
                marks.ball12=form.marks_ball12.data
                marks.ball=form.marks_ball.data
                marks.adapt_scale=form.marks_adapt_scale.data
                marks.lang=form.marks_lang.data
                marks.dpa=form.marks_dpa.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('marks_data')

            return redirect(url_for('marks'))


@app.route('/delete_marks', methods=['POST'])
def delete_marks():
    student_id = request.form['marks_fk_student_id']
    subject_id = request.form['marks_fk_subject']
    
    result = db.session.query(ormTblZnoMarks).filter(
        ormTblZnoMarks.fk_student_id == student_id,
        ormTblZnoMarks.fk_subject == subject_id
    ).one()

    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('marks_data')

    return { "fk_student_id": student_id,
             "fk_subject": subject_id }
    
    
@app.route('/subject', methods=['GET'])
def subject():
    cached_data = redis_client.get('subject_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoSubject).limit(50).all()

    rendered_template = render_template('subject.html', subjects=result)

    redis_client.set('subject_data', rendered_template)

    return rendered_template


@app.route('/new_subject', methods=['GET', 'POST'])
def new_subject():
    form = subjectForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")
        else:
            new_id = db.session.query(func.max(ormTblZnoSubject.id)).scalar() + 1
            new_subject = ormTblZnoSubject(
                id=new_id,
                name=form.subject_name.data,
            )
            
            try:
                db.session.add(new_subject)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('subject_data')

            return redirect(url_for('subject'))

    return render_template('subject_form.html', form=form, form_name="New subject", action="new_subject")


@app.route('/edit_subject', methods=['GET', 'POST'])
def edit_subject():
    form = subjectForm()

    if request.method == 'GET':

        id = request.args.get('subject_id')
        subject = db.session.query(ormTblZnoSubject).filter(ormTblZnoSubject.id == id).one()

        form.subject_name.data = subject.name
        form.subject_id.data = subject.id

        return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject")


    else:

        if form.validate():
            return render_template('subject_form.html', form=form, form_name="Edit subject", action="edit_subject")
        else:
            subject = db.session.query(ormTblZnoSubject).filter(ormTblZnoSubject.id == form.subject_id.data).one()

            try:
                subject.name=form.subject_name.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('subject_data')

            return redirect(url_for('subject'))


@app.route('/delete_subject', methods=['POST'])
def delete_subject():
    id = request.form['subject_id']

    result = db.session.query(ormTblZnoSubject).filter(ormTblZnoSubject.id == id).one()
    
    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('subject_data')

    return id
    
    
@app.route('/region', methods=['GET'])
def region():
    cached_data = redis_client.get('region_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoRegion).limit(50).all()

    rendered_template = render_template('region.html', regions=result)

    redis_client.set('region_data', rendered_template)

    return rendered_template


@app.route('/new_region', methods=['GET', 'POST'])
def new_region():
    form = regionForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('region_form.html', form=form, form_name="New region", action="new_region")
        else:
            new_id = db.session.query(func.max(ormTblZnoRegion.id)).scalar() + 1
            new_region = ormTblZnoRegion(
                id=new_id,
                reg=form.region_reg.data,
                area=form.region_area.data,
                ter=form.region_ter.data
            )
            
            try:
                db.session.add(new_region)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('region_data')

            return redirect(url_for('region'))

    return render_template('region_form.html', form=form, form_name="New region", action="new_region")


@app.route('/edit_region', methods=['GET', 'POST'])
def edit_region():
    form = regionForm()

    if request.method == 'GET':

        id = request.args.get('region_id')
        
        region = db.session.query(ormTblZnoRegion).filter(ormTblZnoRegion.id == id).one()

        form.region_reg.data = region.reg
        form.region_area.data = region.area
        form.region_ter.data = region.ter
        form.region_id.data = region.id

        return render_template('region_form.html', form=form, form_name="Edit region", action="edit_region")


    else:

        if form.validate():
            return render_template('region_form.html', form=form, form_name="Edit region", action="edit_region")
        else:
            region = db.session.query(ormTblZnoRegion).filter(
                ormTblZnoRegion.id == form.region_id.data
            ).one()

            try:
                region.reg=form.region_reg.data
                region.area=form.region_area.data
                region.ter=form.region_ter.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('region_data')

            return redirect(url_for('region'))


@app.route('/delete_region', methods=['POST'])
def delete_region():
    id = request.form['region_id']

    result = db.session.query(ormTblZnoRegion).filter(ormTblZnoRegion.id == id).one()

    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('region_data')

    return id
    

@app.route('/eo', methods=['GET'])
def eo():
    cached_data = redis_client.get('eo_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoEO).limit(50).all()

    rendered_template = render_template('eo.html', eos=result)

    redis_client.set('eo_data', rendered_template)

    return rendered_template


@app.route('/new_eo', methods=['GET', 'POST'])
def new_eo():
    form = eoForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('eo_form.html', form=form, form_name="New eo", action="new_eo")
        else:
            new_id = db.session.query(func.max(ormTblZnoEO.id)).scalar() + 1
            new_eo = ormTblZnoEO(
                id=new_id,
                name=form.eo_name.data,
                type=form.eo_type.data,
                parent=form.eo_parent.data,
                fk_region=form.eo_fk_region.data
            )
            
            try:
                db.session.add(new_eo)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('eo_data')

            return redirect(url_for('eo'))

    return render_template('eo_form.html', form=form, form_name="New eo", action="new_eo")


@app.route('/edit_eo', methods=['GET', 'POST'])
def edit_eo():
    form = eoForm()

    if request.method == 'GET':

        id = request.args.get('eo_id')
        
        eo = db.session.query(ormTblZnoEO).filter(ormTblZnoEO.id == id).one()

        form.eo_name.data = eo.name
        form.eo_type.data = eo.type
        form.eo_parent.data = eo.parent
        form.eo_fk_region.data = eo.fk_region
        form.eo_id.data = eo.id

        return render_template('eo_form.html', form=form, form_name="Edit eo", action="edit_eo")


    else:

        if form.validate():
            return render_template('eo_form.html', form=form, form_name="Edit eo", action="edit_eo")
        else:
            eo = db.session.query(ormTblZnoEO).filter(
                ormTblZnoEO.id == form.eo_id.data
            ).one()

            try:
                eo.name=form.eo_name.data
                eo.type=form.eo_type.data
                eo.parent=form.eo_parent.data
                eo.fk_region=form.eo_fk_region.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('eo_data')

            return redirect(url_for('eo'))


@app.route('/delete_eo', methods=['POST'])
def delete_eo():
    id = request.form['eo_id']

    result = db.session.query(ormTblZnoEO).filter(ormTblZnoEO.id == id).one()
    
    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('eo_data')

    return id
    
    
@app.route('/pt', methods=['GET'])
def pt():
    cached_data = redis_client.get('pt_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoPT).limit(50).all()

    rendered_template = render_template('pt.html', pts=result)

    redis_client.set('pt_data', rendered_template)

    return rendered_template


@app.route('/new_pt', methods=['GET', 'POST'])
def new_pt():
    form = ptForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('pt_form.html', form=form, form_name="New pt", action="new_pt")
        else:
            new_id = db.session.query(func.max(ormTblZnoPT.id)).scalar() + 1
            new_pt = ormTblZnoPT(
                id=new_id,
                name=form.pt_name.data,
                fk_region=form.pt_fk_region.data
            )
            
            try:
                db.session.add(new_pt)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('pt_data')

            return redirect(url_for('pt'))

    return render_template('pt_form.html', form=form, form_name="New pt", action="new_pt")


@app.route('/edit_pt', methods=['GET', 'POST'])
def edit_pt():
    form = ptForm()
    if request.method == 'GET':

        id = request.args.get('pt_id')
                
        pt = db.session.query(ormTblZnoPT).filter(ormTblZnoPT.id == id).one()

        form.pt_name.data = pt.name
        form.pt_fk_region.data = pt.fk_region
        form.pt_id.data = pt.id

        return render_template('pt_form.html', form=form, form_name="Edit pt", action="edit_pt")


    else:

        if form.validate():
            return render_template('pt_form.html', form=form, form_name="Edit pt", action="edit_pt")
        else:
            pt = db.session.query(ormTblZnoPT).filter(
                ormTblZnoPT.id == form.pt_id.data
            ).one()

            try:
                pt.name=form.pt_name.data
                pt.fk_region=form.pt_fk_region.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('pt_data')

            return redirect(url_for('pt'))


@app.route('/delete_pt', methods=['POST'])
def delete_pt():
    id = request.form['pt_id']

    result = db.session.query(ormTblZnoPT).filter(ormTblZnoPT.id == id).one()

    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('pt_data')

    return id


@app.route('/reg_region', methods=['GET'])
def reg_region():
    cached_data = redis_client.get('reg_region_data')
    if cached_data:
        return cached_data.decode('utf-8')

    result = db.session.query(ormTblZnoRegRegion).limit(50).all()

    rendered_template = render_template('reg_region.html', reg_regions=result)

    redis_client.set('reg_region_data', rendered_template)

    return rendered_template


@app.route('/new_reg_region', methods=['GET', 'POST'])
def new_reg_region():
    form = regRegionForm()

    if request.method == 'POST':
        if form.validate():
            return render_template('reg_region_form.html', form=form, form_name="New reg_region", action="new_reg_region")
        else:
            new_id = db.session.query(func.max(ormTblZnoRegRegion.id)).scalar() + 1
            new_reg_region = ormTblZnoRegRegion(
                id=new_id,
                ter_type=form.reg_region_ter_type.data,
                fk_region=form.reg_region_fk_region.data
            )
            
            try:
                db.session.add(new_reg_region)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('reg_region_data')

            return redirect(url_for('reg_region'))

    return render_template('reg_region_form.html', form=form, form_name="New reg_region", action="new_reg_region")


@app.route('/edit_reg_region', methods=['GET', 'POST'])
def edit_reg_region():
    form = regRegionForm()

    if request.method == 'GET':

        id = request.args.get('reg_region_id')
        
        reg_region = db.session.query(ormTblZnoRegRegion).filter(ormTblZnoRegRegion.id == id).one()

        form.reg_region_ter_type.data = reg_region.ter_type
        form.reg_region_fk_region.data = reg_region.fk_region
        form.reg_region_id.data = reg_region.id

        return render_template('reg_region_form.html', form=form, form_name="Edit reg_region", action="edit_reg_region")


    else:

        if form.validate():
            return render_template('reg_region_form.html', form=form, form_name="Edit reg_region", action="edit_reg_region")
        else:
            reg_region = db.session.query(ormTblZnoRegRegion).filter(
                ormTblZnoRegRegion.id == form.reg_region_id.data
            ).one()

            try:
                reg_region.ter_type=form.reg_region_ter_type.data
                reg_region.fk_region=form.reg_region_fk_region.data
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"ERROR: {str(e)}")

            redis_client.delete('reg_region_data')

            return redirect(url_for('reg_region'))


@app.route('/delete_reg_region', methods=['POST'])
def delete_reg_region():
    id = request.form['reg_region_id']

    result = db.session.query(ormTblZnoRegRegion).filter(ormTblZnoRegRegion.id == id).one()

    try:
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: {str(e)}")

    redis_client.delete('reg_region_data')

    return id
    

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        json_data = request.get_json()
        
        subjectValue = json_data.get('subject')
        yearValue = json_data.get('year')
        regionValue = json_data.get('region')
       

        subjectValue = int(subjectValue) if subjectValue is not None else 0
        yearValue = int(yearValue) if yearValue is not None else 0
        
        cached_subject = redis_client.get('querySubject')
        cached_year = redis_client.get('queryYear')
        cached_region = redis_client.get('queryRegion')
        
        if (cached_subject is not None) and (cached_year is not None) and (cached_region is not None):
            if (cached_subject == subjectValue) and (cached_year == yearValue) and (cached_region == regionValue):
                return jsonify(redis_client.get('query_plot_data'))
            else:
                redis_client.delete('query_plot_data')
        else:
            redis_client.mset({
                'querySubject': subjectValue,
                'queryYear': yearValue,
                'queryRegion': regionValue
            })
        
        if regionValue == '0':
            query = (
                db.session.query(
                    func.avg(ormTblZnoMarks.ball100).label('avg_ball'),
                    func.min(ormTblZnoRegion.reg)
                ).join(
                ormTblZnoStudent,
                ormTblZnoStudent.id == ormTblZnoMarks.fk_student_id
                ).join(
                    ormTblZnoRegRegion,
                    ormTblZnoRegRegion.id == ormTblZnoStudent.fk_student_reg
                ).join(
                    ormTblZnoRegion,
                    ormTblZnoRegRegion.fk_region == ormTblZnoRegion.id
                ).filter(
                    ormTblZnoMarks.test_status == 'Зараховано'
                )
            )
        else:
            query = (
                db.session.query(
                    func.avg(ormTblZnoMarks.ball100).label('avg_ball'),
                    func.min(ormTblZnoRegion.area)
                ).join(
                    ormTblZnoStudent,
                    ormTblZnoStudent.id == ormTblZnoMarks.fk_student_id
                ).join(
                    ormTblZnoRegRegion,
                    ormTblZnoRegRegion.id == ormTblZnoStudent.fk_student_reg
                ).join(
                    ormTblZnoRegion,
                    ormTblZnoRegRegion.fk_region == ormTblZnoRegion.id
                ).filter(
                    ormTblZnoMarks.test_status == 'Зараховано'
                ).filter(
                    ormTblZnoRegion.reg == regionValue
                )
            )

        if subjectValue != 0:
            query = query.filter(
                ormTblZnoMarks.fk_subject == subjectValue
            )

        if yearValue == 1:
            query = query.filter(
                ormTblZnoStudent.birth >= 2002
            )
        elif yearValue == 2:
            query = query.filter(
                ormTblZnoStudent.birth <= 2002
            )

        if regionValue == 0:
            query = query.group_by(
                ormTblZnoRegion.reg
            ).order_by(
                'avg_ball'
            )
        else:
            query = query.group_by(
                ormTblZnoRegion.area
            ).order_by(
                'avg_ball'
            )
        
        result = query.all()


        avg_ball, reg = zip(*result)

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
        

        redis_client.set('query_plot_data', json.dumps(data))
    
        return jsonify(data)
    else:
        return render_template('results.html')

            
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
            

