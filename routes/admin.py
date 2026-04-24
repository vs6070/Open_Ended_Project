from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Course, Enrollment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    users = User.query.all()
    courses = Course.query.all()
    
    return render_template('admin/dashboard.html', 
                           total_users=total_users, 
                           total_courses=total_courses, 
                           total_enrollments=total_enrollments,
                           users=users,
                           courses=courses)

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('You cannot delete yourself.', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))
