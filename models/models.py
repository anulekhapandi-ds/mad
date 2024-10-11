from datetime import datetime
from main import db

# Service Professional model
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


# Create the tables in the database
db.create_all()
