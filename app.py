import os
import secrets
from datetime import datetime, timedelta
from functools import wraps
from templates import index_template,login_template,student_dashboard_template,admin_panel_template,register_template,view_computers_student_template,view_applications_template,add_lab_template,add_computer_template,view_computers_template,remove_computer_template,error_template,error_404_template,error_403_template,error_500_template,admin_bookings_view,add_computer_admin,edit_computer_template
from flask import Flask, redirect, render_template, render_template_string, url_for, request, flash
from flask_login import current_user, LoginManager, UserMixin, login_user, logout_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_bcrypt import Bcrypt
from flask import jsonify
from flask import request, redirect, url_for, flash


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'viewLabsDB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16) 

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LabForm(FlaskForm):
    name = StringField('Lab Name', validators=[DataRequired(), Length(min=2, max=50)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Submit')

class AddLabForm(FlaskForm):
    name = StringField('Lab Name', validators=[DataRequired(), Length(min=2, max=50)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Submit')
class AddComputerForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired()])
    applications = StringField('Applications', validators=[DataRequired()])
    submit = SubmitField('Add Computer')
class SearchForm(FlaskForm):
    application = StringField('Application', validators=[DataRequired()])
    submit = SubmitField('Search')
class ComputerForm(FlaskForm):
    number = IntegerField('Computer Number', validators=[DataRequired()])
    applications = StringField('Applications', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submit')

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    applications = db.Column(db.String(200), nullable=False)
    booked = db.Column(db.Boolean, default=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    
    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('student_bookings', lazy=True))
    lecture = db.relationship('User', foreign_keys=[lecture_id], backref=db.backref('lecture_bookings', lazy=True))
    computer = db.relationship('Computer', backref=db.backref('bookings', lazy=True))


    def __init__(self, student_id, computer_id, end_time, lecture_id=None):
        self.student_id = student_id
        self.computer_id = computer_id
        self.end_time = end_time
        self.lecture_id = lecture_id

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    existing_admin = User.query.filter_by(role='admin').first()
    if existing_admin:
        flash('Admin account already exists.', 'warning')
        return redirect(url_for('index'))

    admin_username = "admin"
    admin_email = "admin44@example.com"
    admin_password = "nozulu"

    new_admin = User(username=admin_username, email=admin_email, role='admin')
    new_admin.set_password(admin_password)
    db.session.add(new_admin)
    db.session.commit()

    flash('Admin account created successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    form = LoginForm()
    return render_template_string(index_template, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template_string(login_template, form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'), role='student')
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now login.', 'success')
        return render_template_string(login_template, form=form)
    return render_template_string(register_template, form=form)

@app.route('/labs/<int:lab_id>/computers', methods=['GET'])
@login_required
def view_computers(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_student_template, lab=lab, computers=computers)

@app.route('/applications/<int:computer_id>')
@login_required
def view_applications(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    applications = computer.applications.split(', ')
    return render_template_string(view_applications_template, computer_name=computer.number, applications=applications)

@app.route('/make_computers_available', methods=['POST'])
@login_required
@admin_required
def make_computers_available():
    try:
        Computer.query.update({Computer.booked: False})
        db.session.commit()
        return jsonify({'message': 'All computers are now available.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/view_computers/<int:lab_id>', methods=['GET'])
@login_required
def view_computers_student(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    search = request.args.get('search', '')
    if search:
        computers = Computer.query.filter(
            Computer.lab_id == lab_id,
            Computer.applications.ilike(f'%{search}%')
        ).all()
    else:
        computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_student_template, lab=lab, computers=computers)
@app.route('/admin_computers/<int:lab_id>')
@login_required
def admin_computers(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_template, lab=lab, computers=computers)
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    labs = Lab.query.all()
    if labs:
        for lab in labs:
            print(f"Lab ID: {lab.id}, Name: {lab.name}, Location: {lab.location}")  # Debugging line
    else:
        print("No labs found")  # Debugging line
    return render_template_string(student_dashboard_template, labs=labs)

@app.route('/admin_panel')
@login_required
@admin_required  # Ensure this decorator is correctly implemented
def admin_panel():
    labs = Lab.query.all()
    computers = Computer.query.all()
    return render_template_string(admin_panel_template, labs=labs, computers=computers)
@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if current_user.role != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))
    bookings = Booking.query.all()
    return render_template_string(admin_bookings_view, bookings=bookings)
@app.route('/book_computer/<int:computer_id>', methods=['POST'])
@login_required
def book_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    if computer.booked:
        flash('Computer is already booked', 'danger')
        return redirect(url_for('view_computers_student', lab_id=computer.lab_id))

    end_time = datetime.utcnow() + timedelta(hours=1)
    booking = Booking(student_id=current_user.id, computer_id=computer_id, end_time=end_time)
    db.session.add(booking)

    computer.booked = True
    db.session.commit()

    flash('Computer booked successfully', 'success')
    return redirect(url_for('view_computers_student', lab_id=computer.lab_id))

@app.route('/add_lab', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lab():
    form = AddLabForm()
    if form.validate_on_submit():
        lab = Lab(name=form.name.data, location=form.location.data)
        db.session.add(lab)
        db.session.commit()
        flash('Lab added successfully', 'success')
        return redirect(url_for('admin_panel'))
    return render_template_string(add_lab_template, form=form)

@app.route('/add_computer/<int:lab_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_computer(lab_id):
    lab = Lab.query.get(lab_id)
    if not lab:
        flash('Lab does not exist.', 'danger')
        return redirect(url_for('admin_panel'))
    
    form = AddComputerForm()
    if form.validate_on_submit():
        # Debugging line to ensure lab_id is correctly passed
        print(f"Adding computer to lab: {lab.name} (ID: {lab.id})")
        
        computer = Computer(
            lab_id=lab.id,
            number=form.number.data,
            applications=form.applications.data,
            booked=False
        )
        
        db.session.add(computer)
        db.session.commit()
        
        flash('Computer added successfully', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template_string(add_computer_template, form=form, lab=lab)



@app.route('/admin/computers/edit/<int:computer_id>', methods=['GET', 'POST'])
@login_required
def edit_computer(computer_id):
    if current_user.role != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))
    
    computer = Computer.query.get_or_404(computer_id)
    
    if request.method == 'POST':
        computer.details = request.form['details']
        db.session.commit()
        flash('Computer details updated successfully!', 'success')
        return redirect(url_for("edit", lab_id=computer.lab_id))
    
    return render_template_string(edit_computer_template, computer=computer)

@app.route('/admin/computers/delete/<int:computer_id>', methods=['POST'])
@login_required
def delete_computer(computer_id):
    if current_user.role != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))
    
    computer = Computer.query.get_or_404(computer_id)
    lab_id = computer.lab_id
    db.session.delete(computer)
    db.session.commit()
    flash('Computer deleted successfully!', 'success')
    return redirect(url_for('view_computers_template', lab_id=lab_id))

@app.route('/remove_lab/<int:lab_id>', methods=['POST'])
@login_required
@admin_required
def remove_lab(lab_id):
    lab = Lab.query.get(lab_id)
    if lab:
        computers = Computer.query.filter_by(lab_id=lab_id).all()
        for computer in computers:
            db.session.delete(computer)
        db.session.delete(lab)
        db.session.commit()
        flash('Lab removed successfully', 'success')
    else:
        flash('Lab not found', 'danger')
    return redirect(url_for('admin_panel'))

@app.route('/remove_computer/<int:lab_id>/<int:computer_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def remove_computer(lab_id, computer_id):
    lab = Lab.query.get_or_404(lab_id)
    computer = Computer.query.get_or_404(computer_id)
    if request.method == 'POST':
        db.session.delete(computer)
        db.session.commit()
        flash('Computer removed successfully', 'success')
        return redirect(url_for('view_computers_student', lab_id=lab.id))
    return render_template_string(remove_computer_template, lab=lab, computer=computer)

@app.route('/check_login')
def check_login():
    if current_user.is_authenticated:
        return f"Logged in as {current_user.username} with role {current_user.role}"
    else:
        return "Not logged in"

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return render_template_string(error_template, error_message="Sorry, something went wrong. Please try again later."), 500

@app.errorhandler(404)
def handle_not_found_error(e):
    return render_template_string(error_404_template), 404

@app.errorhandler(403)
def handle_forbidden_error(e):
    return render_template_string(error_403_template), 403

@app.errorhandler(500)
def handle_internal_server_error(e):
    return render_template_string(error_500_template), 500

if __name__ == "__main__":
    app.run(debug=True)