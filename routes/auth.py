from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import db, User
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_role_dashboard(current_user.role)
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_role_dashboard(current_user.role)
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect_role_dashboard(user.role)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def redirect_role_dashboard(role):
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'instructor':
        return redirect(url_for('instructor.dashboard'))
    else:
        return redirect(url_for('student.dashboard'))
