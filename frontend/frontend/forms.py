from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
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
    date_of_offence = DateField('Date of Offence', format="%Y-%m-%d")
    fir_no = IntegerField('FIR No.')
    date_of_report = DateField('Date of Report', format="%Y-%m-%d")
    case_status = StringField('Case Status')
    arrested = StringField('Arrested')
    challan_id = IntegerField('Challan ID')
    case_description = StringField('Case Description')

    ps_name = StringField('Police Station Name')
    address = StringField('Address')
    phone = IntegerField('Phone')

    o_name  = StringField('Officer Name')
    o_address = StringField('Officer Address')
    o_age = IntegerField('Officer Age') 
    o_aadhar = IntegerField('Officer Aadhar')
    o_gender = StringField('Officer Gender')
    o_phone = IntegerField('Officer Phone')
    o_email_id = StringField('Officer email')
    o_qualification = StringField('Qualification')
    
    c_name  = StringField('Complainer Name')
    c_address = StringField('Complainer Address')
    c_age = IntegerField('Complainer Age') 
    c_aadhar = IntegerField('Complainer Aadhar')
    c_gender = StringField('Complainer Gender')
    c_phone = IntegerField('Complainer Phone')

    w_name  = StringField('Witness Name')
    w_address = StringField('Witness Address')
    w_age = IntegerField('Witness Age') 
    w_aadhar = IntegerField('Witness Aadhar')
    w_gender = StringField('Witness Gender')
    w_phone = IntegerField('Witness Phone')

    a_name  = StringField('Accused Name')
    a_address = StringField('Accused Address')
    a_age = IntegerField('Accused Age') 
    a_aadhar = IntegerField('Accused Aadhar')
    a_gender = StringField('Accused Gender')
    a_phone = IntegerField('Accused Phone')

    v_name  = StringField('Victim Name')
    v_address = StringField('Victim Address')
    v_age = IntegerField('Victim Age') 
    v_aadhar = IntegerField('Victim Aadhar')
    v_gender = StringField('Victim Gender')
    v_phone = IntegerField('Victim Phone')

    s_id = StringField('Section id')
    s_desc = StringField('Section Description')

    submit = SubmitField('Submit')
