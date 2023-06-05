from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms import validators


class regionForm(FlaskForm):
    id = StringField("Region ID: ")
    
    reg = StringField("Region name: ", [
        validators.Length(max=30, message="Region name should be up to 30 characters")
    ])
    
    area = StringField("Area name: ", [
        validators.Length(max=50, message="Area name should be up to 50 characters")
    ])
    
    ter = StringField("Territory name: ", [
        validators.Length(max=40, message="Territory name should be up to 40 characters")
    ])
    
    submit = SubmitField("Save")


class regRegionForm(FlaskForm):
    id = StringField("Registration region ID: ")
    
    ter_type = StringField("Territory type: ", [
        validators.Length(max=5, message="Territory type should be up to 5 characters")
    ])
    
    fk_region = IntegerField("Region ID: ", [
        validators.DataRequired(message="Please enter region ID.")
    ])
    
    submit = SubmitField("Save")


class eoForm(FlaskForm):
    id = StringField("EO ID: ")
    
    name = StringField("EO name: ", [
        validators.Length(max=300, message="EO name should be up to 300 characters")
    ])
    
    type = StringField("EO type: ", [
        validators.Length(max=60, message="EO type should be up to 60 characters")
    ])
    
    parent = StringField("EO parent: ", [
        validators.Length(max=300, message="EO parent should be up to 300 characters")
    ])
    
    fk_region = IntegerField("Region ID: ", [
        validators.DataRequired(message="Please enter region ID.")
    ])
    
    submit = SubmitField("Save")


class ptForm(FlaskForm):
    id = StringField("PT ID: ")
    
    name = StringField("PT name: ", [
        validators.Length(max=300, message="PT name should be up to 300 characters")
    ])
    
    fk_region = IntegerField("Region ID: ", [
        validators.DataRequired(message="Please enter region ID.")
    ])
    
    submit = SubmitField("Save")
    
    

class studentForm(FlaskForm):
    id = StringField("Student ID: ", [
        validators.DataRequired("Please enter student ID."),
        validators.Length(min=36, max=36, message="Student ID should be exactly 36 symbols")
    ])
    
    birth = IntegerField("Student birth (only year): ", [
        validators.DataRequired("Please enter student birth."),
        validators.NumberRange(min=1, max=3000, message="Student birth should be more than 1")
    ])
    
    sex = StringField("Student sex: ", [
        validators.Length(max=10, message="Student sex should be up to 10 symbols")
    ])
    
    status = StringField("Student status: ", [
        validators.Length(max=120, message="Student status should be up to 120 symbols")
    ])
    
    class_profile = StringField("Student class profile: ", [
        validators.Length(max=40, message="Student class profile should be up to 40 symbols")
    ])
    
    class_lang = StringField("Student class language: ", [
        validators.Length(max=10, message="Student class language should be up to 10 symbols")
    ])
    
    fk_student_reg = IntegerField("Student registration ID: ", [
        validators.DataRequired(message="Please enter student registration ID.")
    ])
    
    fk_eo = IntegerField("Student EO ID: ", [
        validators.DataRequired(message="Please enter student EO ID.")
    ])
    
    submit = SubmitField("Save")


class subjectForm(FlaskForm):
    id = StringField("Subject ID: ")
    
    name = StringField("Subject name: ", [
        validators.DataRequired(message="Please enter subject name."),
        validators.Length(min=1, max=20, message="Subject name should be from 1 to 20 symbols")
    ])
    
    submit = SubmitField("Save")

class marksForm(FlaskForm):
    fk_student_id = StringField("Student ID: ", [
        validators.DataRequired(message="Please enter student ID."),
        validators.Length(min=36, max=36, message="Student ID should be exactly 36 symbols")
    ])
    
    fk_subject = IntegerField("Subject ID: ", [
        validators.DataRequired(message="Please enter subject ID.")
    ])
    
    fk_pt = IntegerField("PT ID: ")
    
    test = StringField("Test: ", [
        validators.Length(max=30, message="Test should be up to 30 symbols")
    ])
    
    test_status = StringField("Test status: ", [
        validators.Length(max=20, message="Test status should be up to 20 symbols")
    ])
    
    ball100 = DecimalField("Ball100: ", [
        validators.NumberRange(min=0, max=200, message="Ball100 should not exceed 200")
    ])
    
    ball12 = IntegerField("Ball12: ", [
        validators.NumberRange(min=0, max=12, message="Ball12 should not exceed 12")
    ])
    
    ball = IntegerField("Ball: ", [
        validators.NumberRange(min=0, max=100, message="Ball should not exceed 100")
    ])
    
    adapt_scale = IntegerField("Adapt scale: ", [
        validators.NumberRange(min=0, max=100, message="Adapt scale should not exceed 100")
    ])
    
    lang = StringField("Language: ", [
        validators.Length(max=10, message="Language should be up to 10 symbols")
    ])
    
    dpa = StringField("DPA: ", [
        validators.Length(max=30, message="DPA information should be up to 30 symbols")
    ])
    
    submit = SubmitField("Save")
    
    
    
    
