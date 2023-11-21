from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField, FloatField, TimeField ,BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea


# Create a Prescription Form
class PrescriptionForm(FlaskForm):
    type = SelectField("Prescription Type", choices=["White", "Yellow"] , validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    instructions_pharmacy = StringField("Instructions for Pharmacist", widget=TextArea())
    instructions_customer = StringField("Instructions for Patient", widget=TextArea())
    hospital_name = StringField("Hospital / Clinic")
    hospital_address = StringField("Address")

    #doctor = StringField("Prescriber's Name")

    submit = SubmitField("Create")



# Create a User Form Class
class CustomerForm(FlaskForm):
    name = StringField("Name:",  validators=[DataRequired()])
    email = StringField("Email:",  validators=[DataRequired()])
    blood_type = StringField("Blood Type:")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match.')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    middle_name = StringField("Middle Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    birthdate = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    blood_type = SelectField("Blood Type", choices=["AB+","AB-","A+","A-","B+","B-","0+","O-"] , validators=[DataRequired()])
    weight = FloatField("Weight in kg", validators=[DataRequired()])
    sex = SelectField("Sex", choices=["Male", "Female"] , validators=[DataRequired()])
    contact_number = StringField("Contact Number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    emergency_person = StringField("Contact Person", validators=[DataRequired()])
    emergency_number = StringField("Contact Number", validators=[DataRequired()])
    emergency_email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateDoctorForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    middle_name = StringField("Middle Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    birthdate = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    ptr_number = StringField("PTR Number", validators=[DataRequired()])
    specialty = StringField("Specialization", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    contact_number = StringField("Contact Number", validators=[DataRequired()])
    prc_lic_number = StringField("PRC License Number", validators=[DataRequired()])
    s2_lic_number = StringField("S2 License Number")
    submit = SubmitField("Submit")

class UpdatePharmacyForm(FlaskForm):
    company = StringField("Company", validators=[DataRequired()])
    branch = StringField("Branch", validators=[DataRequired()])
    branch_code = StringField("Branch Code/ID")
    #business hours
    store_open = TimeField("Opening Time", validators=[DataRequired()])
    store_close = TimeField("Closing Time", validators=[DataRequired()])
   
    contact_number = StringField("Contact Number", validators=[DataRequired()])
    region = SelectField("Region", choices=["NCR","CAR","Region I","Region II","Region III","Region IV-A","MIMAROPA","Region V","Region VI","Region VII","Region VIII","Region IX","Region X","Region XI","Region XII","Region XIII","BARMM"] , validators=[DataRequired()])
    province = StringField("Province", validators=[DataRequired()])

    city = StringField("City", validators=[DataRequired()])
    brgy = StringField("Barangay", validators=[DataRequired()])
    st_or_bldg = StringField("Street or Building", validators=[DataRequired()])

    submit = SubmitField("Submit")





# Create a Name Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name",  validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Test Password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email",  validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password",  validators=[DataRequired()])
    submit = SubmitField("Submit")



    # BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	## Validators
	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf
