from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Course, Enrollment, Lesson
from sqlalchemy import or_

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
        
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    enrolled_courses = [e.course for e in enrollments]
    return render_template('student/dashboard.html', courses=enrolled_courses)

@student_bp.route('/courses')
@login_required
def courses():
    search_query = request.args.get('q', '')
    if search_query:
        all_courses = Course.query.filter(
            or_(Course.title.ilike(f'%{search_query}%'), 
                Course.description.ilike(f'%{search_query}%'))
        ).all()
    else:
        all_courses = Course.query.all()
        
    enrolled_course_ids = [e.course_id for e in Enrollment.query.filter_by(user_id=current_user.id).all()]
    
    return render_template('student/courses.html', courses=all_courses, enrolled_course_ids=enrolled_course_ids, search_query=search_query)

@student_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    if current_user.role != 'student':
        flash('Only students can enroll in courses.', 'danger')
        return redirect(url_for('student.courses'))
        
    course = Course.query.get_or_404(course_id)
    existing_enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    
    if not existing_enrollment:
        enrollment = Enrollment(user_id=current_user.id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()
        flash(f'Successfully enrolled in {course.title}!', 'success')
    else:
        flash('You are already enrolled in this course.', 'info')
        
    return redirect(url_for('student.dashboard'))

@student_bp.route('/course/<int:course_id>')
@login_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check if enrolled or is instructor of the course or admin
    is_enrolled = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first() is not None
    is_instructor = current_user.id == course.instructor_id
    is_admin = current_user.role == 'admin'
    
    if not (is_enrolled or is_instructor or is_admin):
        flash('You must enroll to view this course.', 'warning')
        return redirect(url_for('student.courses'))
        
    lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order_num).all()
    return render_template('student/course_details.html', course=course, lessons=lessons)
