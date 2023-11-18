from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime, date


# Create Flask Instance
app = Flask(__name__)
# Add MySQL Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/rxpress'

# Secret Key!
app.config['SECRET_KEY'] = "moonlight"

# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(int(user_id))

#Json Thing
@app.route('/date')
def get_current_date():
    #return {"Date": date.today()}
    blood_type = {
        "Geo": "O+",
        "Cam-cam": "AB-",
        "Noriel": "A+"
    }
    return blood_type

# Create Model
class Customers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(120), nullable=False, unique=True)
    blood_type = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Do some password hashing and verification!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create Prescription Model
class Prescriptions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(255))
    content = db.Column(db.Text)
    doctor = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Create a Prescription Form
class PrescriptionForm(FlaskForm):
    type = StringField("Prescription Type", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    doctor = StringField("Prescriber's Name", validators=[DataRequired()])
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








# Create a route decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    form2 = RegisterForm()
    
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer:
            #Check the hash
            if check_password_hash(customer.password_hash, form.password.data):
                login_user(customer)
                flash("Logged in successfully.")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password. Try Again.", "error")
        else:
            flash("That Email is not registered yet.")
    
    if form2.validate_on_submit():
        customer = Customers.query.filter_by(email=form2.email.data).first()
        if customer is None:
            # Hash the password!
            hashed_pw = generate_password_hash(form2.password_hash.data, "pbkdf2")
            customer = Customers(email=form2.email.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
        form2.email.data = ''
        form2.password_hash = ''
        form2.password_hash2 = ''
        flash("Account Created Successfully!")
    return render_template('index.html', form=form, form2=RegisterForm())



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

#Create Logout function
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))

@app.route('/regform')
def dashboard2():
    return render_template("registration form.html")

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html", name=name, form=form)

# Create passoword test page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()


    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        #Lookup Customer via Email address
        pw_to_check = Customers.query.filter_by(email=email).first()

        #Check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)


    return render_template("test_pw.html", email=email, password=password, pw_to_check=pw_to_check, passed=passed, form=form)

@app.route('/customer/add', methods=['get', 'post'])
def add_customer():
    name = None
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            # Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2")
            customer = Customers(name=form.name.data, email=form.email.data, blood_type=form.blood_type.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.blood_type.data = ''
        form.password_hash = ''
        flash("Customer Added Successfully!")
    our_customers = Customers.query.order_by(Customers.date_added)
    return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)

# Create Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = CustomerForm()
    name_to_update = Customers.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.blood_type = request.form['blood_type']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update,id=id)


# Create Delete Records
@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = CustomerForm()
    user_to_delete = Customers.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_customers = Customers.query.order_by(Customers.date_added)
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
    except:
        flash("Whoops! There was a problem deleting user, try again.")
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
    

# Create Prescription Page
@app.route('/add-prescription', methods=['GET', 'POST'])
def add_prescription():
    form = PrescriptionForm()

    if form.validate_on_submit():
        prescription = Prescriptions(type=form.type.data, content=form.content.data, doctor=form.doctor.data)
        #Clear the form
        form.type.data = ''
        form.content.data = ''
        form.doctor.data = ''

        #Add prescription to the database
        db.session.add(prescription)
        db.session.commit()

        #Return a message
        flash("Prescription Created Successfully")

    #Redirect to the webpage
    return render_template("add_prescription.html", form=form)

@app.route('/prescriptions')
def prescriptions():
    #Grab all prescriptions in the database
    prescriptions = Prescriptions.query.order_by(Prescriptions.date_added)
    return render_template("prescriptions.html", prescriptions=prescriptions)

@app.route('/prescriptions/<int:id>')
def prescription(id):
    prescription = Prescriptions.query.get_or_404(id)
    return render_template('prescription.html', prescription=prescription)

@app.route('/prescriptions/edit/<int:id>', methods=['GET', 'POST'])
def edit_prescription(id):
    prescription = Prescriptions.query.get_or_404(id)
    form = PrescriptionForm()
    if form.validate_on_submit():
        prescription.type = form.type.data
        prescription.doctor = form.doctor.data
        prescription.content = form.content.data

        #Update database record
        db.session.add(prescription)
        db.session.commit()
        flash("Prescription has been updated.")
        return redirect(url_for('prescription', id=prescription.id))
    
    form.type.data = prescription.type
    form.doctor.data = prescription.doctor
    form.content.data = prescription.content
    return render_template('edit_prescription.html', form=form, prescription=prescription)

@app.route('/prescriptions/delete/<int:id>')
def delete_prescription(id):
    prescription_to_delete = Prescriptions.query.get_or_404(id)

    try:
        db.session.delete(prescription_to_delete)
        db.session.commit()

        #Return a message
        flash("Prescription was deleted.")

        #Grab all prescriptions from the database
        prescriptions = Prescriptions.query.order_by(Prescriptions.date_added)
        return render_template("prescriptions.html", prescriptions=prescriptions)

    except:
        #return error message
        flash("There was a problem deleting prescription, try again.")
        #Grab all prescriptions from the database
        prescriptions = Prescriptions.query.order_by(Prescriptions.date_added)
        return render_template("prescriptions.html", prescriptions=prescriptions)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500




