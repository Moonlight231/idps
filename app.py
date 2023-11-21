from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from sqlalchemy import and_, or_, not_

from datetime import datetime, date

from webforms import LoginForm, RegisterForm, UpdateForm, UpdateDoctorForm, UpdatePharmacyForm, NamerForm, PasswordForm, CustomerForm, PrescriptionForm
# Create Flask Instance
app = Flask(__name__)

#Session Config
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)
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
    stored_session = session.get("account_type")
    if stored_session == "Customer":
        return Customers.query.get(int(user_id))
    if stored_session == "Doctor":
        return Doctors.query.get(int(user_id))
    if stored_session == "Pharmacy":
        return Pharmacies.query.get(int(user_id))

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

#Create User Class
class Users(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
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

# Create Model
class Customers(Users, UserMixin):

    account_type = db.Column(db.String(200), default="Customer")
    
    first_name = db.Column(db.String(200))
    middle_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    birthdate = db.Column(db.Date)
    blood_type = db.Column(db.String(120))
    weight = db.Column(db.Float)
    weight_update = db.Column(db.Date)
    sex = db.Column(db.String(120))
    contact_number = db.Column(db.String(100))
    address = db.Column(db.String(500))
    emergency_person = db.Column(db.String(200))
    emergency_number = db.Column(db.String(200))
    emergency_email = db.Column(db.String(200))
    date_added = db.Column(db.Date, default=date.today)

    #Customers can have many prescriptions
    prescriptions = db.relationship('Prescriptions', backref='patient')
    
    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create Model
class Doctors(Users, UserMixin):
    account_type = db.Column(db.String(200), default="Doctor")

    first_name = db.Column(db.String(200))
    middle_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))

    ptr_number = db.Column(db.String(120))
    specialty = db.Column(db.String(200))
    birthdate = db.Column(db.Date)
    address = db.Column(db.String(500))

    contact_number = db.Column(db.String(100))

    prc_lic_number = db.Column(db.String(120))
    s2_lic_number = db.Column(db.String(120))

    date_added = db.Column(db.Date, default=date.today)

    #Doctors can have many prescribed prescriptions
    prescriptions = db.relationship('Prescriptions', backref='prescriber')
    
    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create Model
class Pharmacies(Users, UserMixin):
    account_type = db.Column(db.String(200), default="Pharmacy")
    
    company = db.Column(db.String(200))
    branch = db.Column(db.String(200))
    branch_code = db.Column(db.String(200))

    store_open = db.Column(db.Time)
    store_close = db.Column(db.Time)

    contact_number = db.Column(db.String(100))
    region = db.Column(db.String(500))
    province = db.Column(db.String(500))

    city = db.Column(db.String(500))
    brgy = db.Column(db.String(500))
    st_or_bldg = db.Column(db.String(500))

    date_added = db.Column(db.Date, default=date.today)
    
    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name
    
# Create Prescription Model
class Prescriptions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(255))
    content = db.Column(db.Text)
    instructions_pharmacy = db.Column(db.Text)
    instructions_customer = db.Column(db.Text)
    status = db.Column(db.String(255), default="Not Filled")
    hospital_name = db.Column(db.String(500))
    hospital_address = db.Column(db.String(500))
    #doctor = db.Column(db.String(255))
    date_added = db.Column(db.Date, default=date.today)
    #foreign key
    prescriber_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('customers.id'))


# Create a route decorator
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    form2 = RegisterForm()

    
    
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        doctor = Doctors.query.filter_by(email=form.email.data).first()
        pharmacy = Pharmacies.query.filter_by(email=form.email.data).first()
        if customer:
            #storing session
            session["account_type"] = customer.account_type
            #Check the hash
            if check_password_hash(customer.password_hash, form.password.data):
                login_user(customer)
                flash("Logged in successfully.")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password. Try Again.", "error")
        elif doctor:
            #storing session
            session["account_type"] = doctor.account_type
            #Check the hash
            if check_password_hash(doctor.password_hash, form.password.data):
                login_user(doctor)
                flash("Logged in successfully.")
                return redirect(url_for('doctor_dashboard'))
            else:
                flash("Wrong password. Try Again.", "error")
        elif pharmacy:
            #storing session
            session["account_type"] = pharmacy.account_type
            #Check the hash
            if check_password_hash(pharmacy.password_hash, form.password.data):
                login_user(pharmacy)
                flash("Logged in successfully.")
                return redirect(url_for('pharmacy_dashboard'))
            else:
                flash("Wrong password. Try Again.", "error")
        else:
            flash("That Email is not registered yet.")
    
    if form2.validate_on_submit():
        customer = Customers.query.filter_by(email=form2.email.data).first()
        doctors = Doctors.query.filter_by(email=form2.email.data).first()
        pharmacies = Pharmacies.query.filter_by(email=form2.email.data).first()
        if (customer is None) and (doctors is None) and (pharmacies is None):
            # Hash the password!
            hashed_pw = generate_password_hash(form2.password_hash.data, "pbkdf2")
            customer = Customers(email=form2.email.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
            form2.email.data = ''
            form2.password_hash = ''
            form2.password_hash2 = ''
            flash("Account Created Successfully!")
        else:
            form2.password_hash = ''
            form2.password_hash2 = ''
            flash("That Email is already in use.")
    return render_template('index.html', form=form, form2=RegisterForm())



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = UpdateForm()
    id = current_user.id
    name_to_update = Customers.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.first_name = request.form['first_name']
        name_to_update.middle_name = request.form['middle_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.birthdate = request.form['birthdate']
        name_to_update.blood_type = request.form['blood_type']
        name_to_update.weight = request.form['weight']
        name_to_update.weight_update = datetime.now()
        name_to_update.sex = request.form['sex']
        name_to_update.contact_number = request.form['contact_number']
        name_to_update.address = request.form['address']
        name_to_update.emergency_person = request.form['emergency_person']
        name_to_update.emergency_number = request.form['emergency_number']
        name_to_update.emergency_email = request.form['emergency_email']
        
        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)

@app.route('/doctor/dashboard', methods=['GET', 'POST'])
@login_required
def doctor_dashboard():
    form = UpdateDoctorForm()
    id = current_user.id
    name_to_update = Doctors.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.first_name = request.form['first_name']
        name_to_update.middle_name = request.form['middle_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.birthdate = request.form['birthdate']

        name_to_update.ptr_number = request.form['ptr_number']
        name_to_update.specialty = request.form['specialty']


        name_to_update.contact_number = request.form['contact_number']
        name_to_update.address = request.form['address']

        name_to_update.prc_lic_number = request.form['prc_lic_number']
        name_to_update.s2_lic_number = request.form['s2_lic_number']

        
        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("doctor_dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("doctor_dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("doctor_dashboard.html", form=form, name_to_update=name_to_update, id=id)
    

@app.route('/pharmacy/dashboard', methods=['GET', 'POST'])
@login_required
def pharmacy_dashboard():
    form = UpdatePharmacyForm()
    id = current_user.id
    name_to_update = Pharmacies.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.company = request.form['company']
        name_to_update.branch = request.form['branch']
        name_to_update.branch_code = request.form['branch_code']

        name_to_update.store_open = request.form['store_open']
        name_to_update.store_close = request.form['store_close']

        name_to_update.contact_number = request.form['contact_number']
        name_to_update.region = request.form['region']
        name_to_update.province = request.form['province']

        name_to_update.city = request.form['city']
        name_to_update.brgy = request.form['brgy']
        name_to_update.st_or_bldg = request.form['st_or_bldg']

        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("pharmacy_dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("pharmacy_dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("pharmacy_dashboard.html", form=form, name_to_update=name_to_update, id=id)


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

@app.route('/doctor/add', methods=['get', 'post'])
def add_doctor():
    form = RegisterForm()
    if form.validate_on_submit():
        doctor = Doctors.query.filter_by(email=form.email.data).first()
        customer = Customers.query.filter_by(email=form.email.data).first()
        if (doctor is None) and (customer is None):
            # Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2")
            doctor = Doctors(email=form.email.data, password_hash=hashed_pw)
            db.session.add(doctor)
            db.session.commit()
            form.email = ''
            form.password_hash = ''
            form.password_hash2 = ''
            flash("Doctor Added Successfully!")
        else:
            form.password_hash = ''
            form.password_hash2 = ''
            flash("That Email is already in use.")
    our_doctors = Doctors.query.order_by(Doctors.date_added)
    return render_template("add_doctor.html", form=RegisterForm(), our_doctors=our_doctors)

@app.route('/pharmacy/add', methods=['get', 'post'])
def add_pharmacy():
    form = RegisterForm()
    if form.validate_on_submit():
        doctor = Doctors.query.filter_by(email=form.email.data).first()
        customer = Customers.query.filter_by(email=form.email.data).first()
        pharmacy = Pharmacies.query.filter_by(email=form.email.data).first()
        if (doctor is None) and (customer is None) and (pharmacy is None):
            # Hash the password!
            hashed_pw = generate_password_hash(form.password_hash.data, "pbkdf2")
            pharmacy = Pharmacies(email=form.email.data, password_hash=hashed_pw)
            db.session.add(pharmacy)
            db.session.commit()
            form.email = ''
            form.password_hash = ''
            form.password_hash2 = ''
            flash("Pharmacy Added Successfully!")
        else:
            form.password_hash = ''
            form.password_hash2 = ''
            flash("That Email is already in use.")
    our_pharmacies = Pharmacies.query.order_by(Pharmacies.date_added)
    return render_template("add_pharmacy.html", form=RegisterForm(), our_pharmacies=our_pharmacies)


# Create Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateForm()
    name_to_update = Customers.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.first_name = request.form['first_name']
        name_to_update.middle_name = request.form['middle_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.birthdate = request.form['birthdate']
        name_to_update.blood_type = request.form['blood_type']
        name_to_update.weight = request.form['weight']
        name_to_update.weight_update = datetime.now()
        name_to_update.sex = request.form['sex']
        name_to_update.contact_number = request.form['contact_number']
        name_to_update.address = request.form['address']
        name_to_update.emergency_person = request.form['emergency_person']
        name_to_update.emergency_number = request.form['emergency_number']
        name_to_update.emergency_email = request.form['emergency_email']
        
        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

# Create Update Database Record
@app.route('/doctor_update/<int:id>', methods=['GET', 'POST'])
@login_required
def doctor_update(id):
    form = UpdateDoctorForm()
    name_to_update = Doctors.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.first_name = request.form['first_name']
        name_to_update.middle_name = request.form['middle_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.birthdate = request.form['birthdate']

        name_to_update.ptr_number = request.form['ptr_number']
        name_to_update.specialty = request.form['specialty']


        name_to_update.contact_number = request.form['contact_number']
        name_to_update.address = request.form['address']

        name_to_update.prc_lic_number = request.form['prc_lic_number']
        name_to_update.s2_lic_number = request.form['s2_lic_number']
        
        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("doctor_update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("doctor_update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("doctor_update.html", form=form, name_to_update=name_to_update, id=id)

# Create Update Database Record
@app.route('/pharmacy_update/<int:id>', methods=['GET', 'POST'])
@login_required
def pharmacy_update(id):
    form = UpdatePharmacyForm()
    name_to_update = Pharmacies.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.company = request.form['company']
        name_to_update.branch = request.form['branch']
        name_to_update.branch_code = request.form['branch_code']

        name_to_update.store_open = request.form['store_open']
        name_to_update.store_close = request.form['store_close']

        name_to_update.contact_number = request.form['contact_number']
        name_to_update.region = request.form['region']
        name_to_update.province = request.form['province']

        name_to_update.city = request.form['city']
        name_to_update.brgy = request.form['brgy']
        name_to_update.st_or_bldg = request.form['st_or_bldg']

        try:
            db.session.commit()
            flash("Update Successful")
            return render_template("pharmacy_update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there's a problem.")
            return render_template("pharmacy_update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("pharmacy_update.html", form=form, name_to_update=name_to_update, id=id)


'''# Create Update Database Record
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
'''

# Create Delete Records
@app.route('/delete/<int:id>')
def delete(id):
    form = CustomerForm()
    user_to_delete = Customers.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_customers = Customers.query.order_by(Customers.date_added)
        return render_template("add_customer.html", form=form, our_customers=our_customers)
    except:
        flash("Whoops! There was a problem deleting user, try again.")
        return render_template("add_customer.html", form=form, our_customers=our_customers)

# Delete Doctor Records
@app.route('/doctor/delete/<int:id>')
def delete_doctor(id):
    form = RegisterForm()
    user_to_delete = Doctors.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_doctors = Doctors.query.order_by(Doctors.date_added)
        return render_template("add_doctor.html", form=form, our_doctors=our_doctors)
    except:
        flash("Whoops! There was a problem deleting user, try again.")
        return render_template("add_doctor.html", form=form, our_doctors=our_doctors)
    

# Create Prescription Page
@app.route('/add-prescription', methods=['GET', 'POST'])
def add_prescription():
    form = PrescriptionForm()

    if form.validate_on_submit():
        prescriber = current_user.id
        prescription = Prescriptions(type=form.type.data, 
                                     content=form.content.data,
                                     instructions_pharmacy=form.instructions_pharmacy.data, 
                                     instructions_customer=form.instructions_customer.data,
                                     hospital_name=form.hospital_name.data, 
                                     hospital_address=form.hospital_address.data,   
                                     prescriber_id=prescriber)
        #Clear the form
        form.type.data = ''
        form.content.data = ''
        form.instructions_pharmacy.data = ''
        form.instructions_customer.data = ''
        form.hospital_name.data = ''
        form.hospital_address.data = ''

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
@login_required
def edit_prescription(id):
    prescription = Prescriptions.query.get_or_404(id)
    form = PrescriptionForm()
    if form.validate_on_submit():
        prescription.type = form.type.data
        prescription.content = form.content.data
        prescription.instructions_pharmacy = form.instructions_pharmacy.data
        prescription.instructions_customer = form.instructions_customer.data
        prescription.hospital_name = form.hospital_name.data
        prescription.hospital_address = form.hospital_address.data

        #Update database record
        db.session.add(prescription)
        db.session.commit()
        flash("Prescription has been updated.")
        return redirect(url_for('prescription', id=prescription.id))
    
    if current_user.id == prescription.prescriber_id:
        form.type.data = prescription.type
        form.content.data = prescription.content
        form.instructions_pharmacy.data = prescription.instructions_pharmacy
        form.instructions_customer.data = prescription.instructions_customer
        form.hospital_name.data = prescription.hospital_name
        form.hospital_address.data = prescription.hospital_address
        return render_template('edit_prescription.html', form=form, prescription=prescription)
    else:
        flash("You are not authorized to edit this prescription.")

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




