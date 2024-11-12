from flask  import Flask, render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'  # Database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings
db = SQLAlchemy(app)

class ServiceProfessional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One service professional can have many service requests
    requests = db.relationship('ServiceRequest',
                               backref='professional',
                               lazy=True)


# Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One customer can have many service requests
    requests = db.relationship('ServiceRequest', backref='customer', lazy=True)


# Service model
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer,
                              nullable=False)  # Time required in minutes

    # Relationship: One service can be requested many times
    requests = db.relationship('ServiceRequest', backref='service', lazy=True)


# Service Request model
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer,
                           db.ForeignKey('service.id'),
                           nullable=False)
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customer.id'),
                            nullable=False)
    professional_id = db.Column(db.Integer,
                                db.ForeignKey('service_professional.id'))
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(
        db.String(50), default='requested')  # requested, assigned, closed
    remarks = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials match
        if username == "1" and password == "1":
            return render_template('admin_dashboard.html')
        else:
            flash('Invalid username or password!') 
            return render_template('admin_login.html')
    return render_template('admin_login.html')

@app.route('/professional/login')
def professional_login():
    return render_template('professional_login.html')

@app.route('/customer/login')
def customer_login():
    return render_template('customer_login.html')

@app.route('/professional/register')
def professional_register():
    return render_template('professional_register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/customers')
def manage_customers():
    
    # Retrieve all customers with role "Customer"
    customers = Customer.query.all()
    return render_template('manage_customers.html', customers=customers)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
