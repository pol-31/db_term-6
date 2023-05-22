from main import db

class ormTblZnoRegion(db.Model):
    __tablename__ = 'tbl_zno_region'
    __table_args__ = (db.UniqueConstraint('reg', 'area', 'ter', name='region_unique'),
    {'extend_existing': True})
    
    id = db.Column(db.Integer, primary_key=True)
    reg = db.Column(db.String(30), nullable=True)
    area = db.Column(db.String(50), nullable=True)
    ter = db.Column(db.String(40), nullable=True)

    reg_region = db.relationship('ormTblZnoRegRegion')
    eo = db.relationship('ormTblZnoEO')
    pt = db.relationship('ormTblZnoPT')

class ormTblZnoRegRegion(db.Model):
    __tablename__ = 'tbl_zno_reg_region'
    __table_args__ = (db.UniqueConstraint('ter_type', 'fk_region', name='reg_reg_unique'),
    {'extend_existing': True})
    
    id = db.Column(db.Integer, primary_key=True)
    ter_type = db.Column(db.String(5), nullable=True)
    fk_region = db.Column(db.Integer, db.ForeignKey('tbl_zno_region.id'))

    students = db.relationship('ormTblZnoStudent')
    
class ormTblZnoEO(db.Model):
    __tablename__ = 'tbl_zno_eo'
    __table_args__ = (db.UniqueConstraint('name', 'type', 'parent', name='eo_unique'),
    {'extend_existing': True})
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=True)
    type = db.Column(db.String(60), nullable=True)
    parent = db.Column(db.String(300), nullable=True)
    fk_region = db.Column(db.Integer, db.ForeignKey('tbl_zno_region.id'))

    students = db.relationship('ormTblZnoStudent')


class ormTblZnoPT(db.Model):
    __tablename__ = 'tbl_zno_pt'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)
    fk_region = db.Column(db.Integer, db.ForeignKey('tbl_zno_region.id'))

    marks = db.relationship('ormTblZnoMarks')


class ormTblZnoStudent(db.Model):
    __tablename__ = 'tbl_zno_student'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String(36), primary_key=True)
    birth = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(120), nullable=True)
    class_profile = db.Column(db.String(40), nullable=True)
    class_lang = db.Column(db.String(10), nullable=True)
    fk_student_reg = db.Column(db.Integer, db.ForeignKey('tbl_zno_reg_region.id'))
    fk_eo = db.Column(db.Integer, db.ForeignKey('tbl_zno_eo.id'))

    marks = db.relationship('ormTblZnoSubject', secondary='tbl_zno_marks')


class ormTblZnoSubject(db.Model):
    __tablename__ = 'tbl_zno_subject'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    
    marks = db.relationship('ormTblZnoStudent', secondary='tbl_zno_marks')

class ormTblZnoMarks(db.Model):
    __tablename__ = 'tbl_zno_marks'
    __table_args__ = {'extend_existing': True}

    fk_student_id = db.Column(db.String(36), db.ForeignKey('tbl_zno_student.id'), primary_key=True)
    fk_subject = db.Column(db.Integer, db.ForeignKey('tbl_zno_subject.id'), primary_key=True)
    fk_pt = db.Column(db.Integer, db.ForeignKey('tbl_zno_pt.id'), nullable=True)
    test = db.Column(db.String(30), nullable=True)
    test_status = db.Column(db.String(20), nullable=True)
    ball100 = db.Column(db.Numeric, nullable=True)
    ball12 = db.Column(db.Integer, nullable=True)
    ball = db.Column(db.Integer, nullable=True)
    adapt_scale = db.Column(db.Integer, nullable=True)
    lang = db.Column(db.String(10), default='українська')
    dpa = db.Column(db.String(30), nullable=True)






