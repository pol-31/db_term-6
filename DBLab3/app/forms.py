from flask_wtf import Form
from wtforms import StringField, IntegerField, DecimalField, SubmitField, HiddenField
from wtforms import validators


class regionForm(Form):
   
   region_id = HiddenField()

   region_reg = StringField("Region name: ",[
                                    validators.DataRequired("Please enter region name."),
                                    validators.Length(0, 30, "Region name should be up to 30 symbols")
                                 ])

   region_area = StringField("Area name: ", [
                                   validators.DataRequired("Please enter area name."),
                                   validators.Length(0, 50, "Area name should be up to 50 symbols")
                               ])

   region_ter = StringField("Territory name: ", [
                                   validators.DataRequired("Please enter territory name."),
                                   validators.Length(0, 40, "Territory name should be up to 40 symbols")
                               ])

   submit = SubmitField("Save")



class regRegionForm(Form):

   reg_region_id = HiddenField()
   
   reg_region_ter_type = StringField("Territory type: ",[
                                    validators.DataRequired("Please enter territory type."),
                                    validators.Length(0, 5, "Territory type should be up to 5 symbols")
                                 ])

   reg_region_fk_region = IntegerField("Region id: ",[
                                    validators.DataRequired("Please enter region ID.")
                                 ])
                                 
   submit = SubmitField("Save")



class eoForm(Form):

   eo_id = HiddenField()
   
   eo_name = StringField("EO name: ",[
                                    validators.DataRequired("Please enter EO name."),
                                    validators.Length(0, 300, "EO name should be up to 300 symbols")
                                 ])

   eo_type = StringField("EO type: ", [
                                   validators.DataRequired("Please enter EO type."),
                                   validators.Length(0, 60, "EO type should be up to 60 symbols")
                               ])

   eo_parent = StringField("EO parent: ", [
                                   validators.DataRequired("Please enter EO parent."),
                                   validators.Length(0, 300, "EO parent should be up to 300 symbols")
                               ])

   eo_fk_region = IntegerField("Region id: ",[
                                    validators.DataRequired("Please enter region ID.")
                                 ])
                                 
   submit = SubmitField("Save")



class ptForm(Form):

   pt_id = HiddenField()


   pt_name = StringField("PT name: ", [
                                   validators.DataRequired("Please enter PT name."),
                                   validators.Length(0, 300, "PT name should be up to 300 symbols")
                               ])

   pt_fk_region = IntegerField("Region id: ",[
                                    validators.DataRequired("Please enter region ID.")
                                 ])
                                 
   submit = SubmitField("Save")



class studentForm(Form):
   
   student_id = StringField("Student ID: ",[
                                    validators.DataRequired("Please enter student ID."),
                                    validators.Length(36, 36, "Student ID should be exactly 36 symbols")
                                 ])

   student_birth = IntegerField("Student birth (only year): ",[
                                    validators.DataRequired("Please enter student birth."),
                                    validators.number_range(1, 3000, "Student birth should be more than 1")
                                 ])

   student_sex = StringField("Student sex: ",[
                                    validators.DataRequired("Please enter student sex."),
                                    validators.Length(0, 10, "Student sex should be up to 10 symbols")
                                 ])

   student_status = StringField("Student status: ",[
                                    validators.DataRequired("Please enter student status."),
                                    validators.Length(0, 120, "Student status should be up to 120 symbols")
                                 ])

   student_class_profile = StringField("Student class profile: ", [
                                   validators.DataRequired("Please enter student class profile."),
                                   validators.Length(0, 40, "Student class profile should be up to 40 symbols")
                               ])

   student_class_lang = StringField("Student class language: ", [
                                   validators.DataRequired("Please enter student class language."),
                                   validators.Length(0, 10, "Student class language should be up to 10 symbols")
                               ])     

   student_fk_student_reg = IntegerField("Student registration ID: ",[
                                    validators.DataRequired("Please enter student registration ID.")
                                 ])
                                 
                                 
   student_fk_eo = IntegerField("Student EO ID: ",[
                                    validators.DataRequired("Please enter student EO ID.")
                                 ])
                                 
   submit = SubmitField("Save")



class subjectForm(Form):

   subject_id = HiddenField()
   
   subject_name = StringField("Subject name: ",[
                                    validators.DataRequired("Please enter subject name."),
                                    validators.Length(1, 20, "Subject name should be from 1 to 20 symbols")
                                 ])
                                 
   submit = SubmitField("Save")



class marksForm(Form):
   
   marks_fk_student_id = StringField("Student ID: ",[
                                    validators.DataRequired("Please enter student ID."),
                                    validators.Length(36, 36, "Student ID should be exactly 36 symbols")
                                 ])
   
   marks_fk_subject = IntegerField("Subject ID: ",[
                                    validators.DataRequired("Please enter subject ID.")
                                 ])

   marks_fk_pt = IntegerField("PT ID: ",[
                                    validators.DataRequired("Please enter PT ID.")
                                 ])
   
   marks_test = StringField("Test: ",[
                                    validators.DataRequired("Please enter test score."),
                                    validators.Length(0, 30, "Test should be up to 30 symbols")
                                 ])
   
   marks_test_status = StringField("Test status: ",[
                                    validators.DataRequired("Please enter test status."),
                                    validators.Length(0, 20, "Test status should be up to 20 symbols")
                                 ])
  
   marks_ball100 = DecimalField("Ball100: ",[
                                    validators.DataRequired("Please enter ball100 score."),
                                    validators.number_range(0, 200, "Ball100 should not exceed 200")
                                 ])

   marks_ball12 = IntegerField("Ball12: ",[
                                    validators.DataRequired("Please enter ball12 score."),
                                    validators.number_range(0, 12, "Ball12 should not exceed 12")
                                 ])

   marks_ball = IntegerField("Ball: ",[
                                    validators.DataRequired("Please enter ball score."),
                                    validators.number_range(0, 100, "Ball should not exceed 100")
                                 ])

   marks_adapt_scale = IntegerField("Adapt scale: ",[
                                    validators.DataRequired("Please enter adapt scale."),
                                    validators.number_range(0, 100, "Adapt scale should not exceed 100")
                                 ])
  
   marks_lang = StringField("Language: ",[
                                    validators.DataRequired("Please enter language."),
                                    validators.Length(0, 10, "Language should be up to 10 symbols")
                                 ])
   
   marks_dpa = StringField("DPA: ",[
                                    validators.DataRequired("Please enter DPA information."),
                                    validators.Length(0, 30, "DPA information should be up to 30 symbols")
                                 ])
                                 
   submit = SubmitField("Save")


