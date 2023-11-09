from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
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

# Create Model
class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a User Form Class
class CustomerForm(FlaskForm):
    name = StringField("Name:",  validators=[DataRequired()])
    email = StringField("Email:",  validators=[DataRequired()])
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

@app.route('/customer/add', methods=['get', 'post'])
def add_customer():
    name = None
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        if customer is None:
            customer = Customers(name=form.name.data, email=form.email.data)
            db.session.add(customer)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Customer Added Successfully!")
    our_customers = Customers.query.order_by(Customers.date_added)
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


