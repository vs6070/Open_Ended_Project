from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Course, Lesson, Enrollment

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor')

@instructor_bp.before_request
def check_instructor():
    if not current_user.is_authenticated or current_user.role not in ['instructor', 'admin']:
        flash('Instructor access required.', 'danger')
        return redirect(url_for('home'))

@instructor_bp.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    # Basic analytics: sum of enrollments
    total_students = sum([len(c.enrollments) for c in courses])
    return render_template('instructor/dashboard.html', courses=courses, total_students=total_students)

@instructor_bp.route('/course/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if title and description:
            course = Course(title=title, description=description, instructor_id=current_user.id)
            db.session.add(course)
            db.session.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('instructor.dashboard'))
        else:
            flash('Title and description are required.', 'danger')
            
    return render_template('instructor/manage_course.html', course=None)

@instructor_bp.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        flash('You can only edit your own courses.', 'danger')
        return redirect(url_for('instructor.dashboard'))
        
    if request.method == 'POST':
        course.title = request.form.get('title')
        course.description = request.form.get('description')
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('instructor.dashboard'))
        
    return render_template('instructor/manage_course.html', course=course)

@instructor_bp.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        flash('You can only delete your own courses.', 'danger')
        return redirect(url_for('instructor.dashboard'))
        
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('instructor.dashboard'))

@instructor_bp.route('/course/<int:course_id>/lessons', methods=['GET', 'POST'])
@login_required
def manage_lessons(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('instructor.dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        order_num = request.form.get('order_num', 0, type=int)
        
        if title and video_url:
            lesson = Lesson(title=title, video_url=video_url, course_id=course.id, order_num=order_num)
            db.session.add(lesson)
            db.session.commit()
            flash('Lesson added successfully!', 'success')
        else:
            flash('Title and Video URL are required.', 'danger')
            
    lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order_num).all()
    return render_template('instructor/manage_lessons.html', course=course, lessons=lessons)

@instructor_bp.route('/lesson/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('instructor.dashboard'))
        
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully!', 'success')
    return redirect(url_for('instructor.manage_lessons', course_id=course.id))
