from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from frontend.models import Admin

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class CrimeForm(FlaskForm):
    date_of_offence = DateField('Date of Offence', format="%Y-%m-%d", validators =[Optional()])
    fir_no = IntegerField('FIR No.', validators =[Optional()])
    date_of_report = DateField('Date of Report', format="%Y-%m-%d", validators = [Optional()])
    case_status = StringField('Case Status', validators =[Optional()])
    arrested = StringField('Arrested', validators =[Optional()])
    challan_id = IntegerField('Challan ID', validators =[Optional()])
    case_description = StringField('Case Description', validators =[Optional()])

    ps_name = StringField('Police Station Name', validators =[Optional()])
    ps_address = StringField('Address', validators =[Optional()])
    ps_phone = IntegerField('Phone', validators =[Optional()])

    o_name  = StringField('Officer Name', validators =[Optional()])
    o_address = StringField('Officer Address', validators =[Optional()])
    o_age = IntegerField('Officer Age', validators =[Optional()]) 
    o_aadhar = IntegerField('Officer Aadhar', validators =[Optional()])
    o_gender = StringField('Officer Gender', validators =[Optional()])
    o_phone = IntegerField('Officer Phone', validators =[Optional()])
    o_email_id = StringField('Officer email', validators =[Optional()])
    o_qualification = StringField('Qualification', validators =[Optional()])
    
    c_name  = StringField('Complainer Name', validators =[Optional()])
    c_address = StringField('Complainer Address', validators =[Optional()])
    c_age = IntegerField('Complainer Age', validators =[Optional()]) 
    c_aadhar = IntegerField('Complainer Aadhar', validators =[Optional()])
    c_gender = StringField('Complainer Gender', validators =[Optional()])
    c_phone = IntegerField('Complainer Phone', validators =[Optional()])

    w_name  = TextAreaField('Witness Name', validators =[Optional()])
    w_address = TextAreaField('Witness Address', validators =[Optional()])
    w_age = TextAreaField('Witness Age', validators =[Optional()]) 
    w_aadhar = TextAreaField('Witness Aadhar', validators =[Optional()])
    w_gender = TextAreaField('Witness Gender', validators =[Optional()])
    w_phone = TextAreaField('Witness Phone', validators =[Optional()])

    a_name  = TextAreaField('Accused Name', validators =[Optional()])
    a_address = TextAreaField('Accused Address', validators =[Optional()])
    a_age = TextAreaField('Accused Age', validators =[Optional()]) 
    a_aadhar = TextAreaField('Accused Aadhar', validators =[Optional()])
    a_gender = TextAreaField('Accused Gender', validators =[Optional()])
    a_phone = TextAreaField('Accused Phone', validators =[Optional()])

    v_name  = TextAreaField('Victim Name', validators=[Optional()])
    v_address = TextAreaField('Victim Address', validators=[Optional()])
    v_age = TextAreaField('Victim Age', validators=[Optional()]) 
    v_aadhar = TextAreaField('Victim Aadhar', validators=[Optional()])
    v_gender = TextAreaField('Victim Gender', validators=[Optional()])
    v_phone = TextAreaField('Victim Phone', validators=[Optional()])

    s_id = StringField('Section id', validators =[Optional()])
    s_desc = StringField('Section Description', validators =[Optional()])

    submit = SubmitField('Submit')
