from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime


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

# Create Model
class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
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

# Create a User Form Class
class CustomerForm(FlaskForm):
    name = StringField("Name:",  validators=[DataRequired()])
    email = StringField("Email:",  validators=[DataRequired()])
    blood_type = StringField("Blood Type:")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match.')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name",  validators=[DataRequired()])
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
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

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
@app.route('/update/<int:customer_id>', methods=['GET', 'POST'])
def update(customer_id):
    form = CustomerForm()
    name_to_update = Customers.query.get_or_404(customer_id)
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
        return render_template("update.html", form=form, name_to_update=name_to_update,customer_id=customer_id)


# Create Delete Records
@app.route('/delete/<int:customer_id>')
def delete(customer_id):
    name = None
    form = CustomerForm()
    user_to_delete = Customers.query.get_or_404(customer_id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_customers = Customers.query.order_by(Customers.date_added)
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
    except:
        flash("Whoops! There was a problem deleting user, try again.")
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500




