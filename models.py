import bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Student, Lecture, Admin
    # Add more columns as needed
    def check_password(self, password):
       return bcrypt.check_password_hash(self.password, password)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    applications = db.Column(db.String(200), nullable=False)
    booked = db.Column(db.Boolean, default=False)
    # Add more columns as needed

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    # Add more columns as needed

    def __init__(self, student_id, computer_id, end_time, lecture_id=None):
        self.student_id = student_id
        self.computer_id = computer_id
        self.end_time = end_time
        self.lecture_id = lecture_id
