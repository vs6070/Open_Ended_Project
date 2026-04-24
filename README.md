# UPES LMS

A complete full-stack Learning Management System (LMS) built with Python Flask, SQLAlchemy, HTML, Tailwind CSS, and JavaScript.

## Features

- **User Authentication**: Secure register and login system using Flask-Bcrypt and Flask-Login.
- **Roles**: Three distinct roles: Student, Instructor, and Admin.
- **Student Dashboard**: View enrolled courses, search the course catalog, and watch lessons.
- **Instructor Dashboard**: Create, edit, and delete courses; add and manage video lessons; view student enrollments.
- **Admin Dashboard**: Overview of all users and courses across the platform, with the ability to delete users.
- **Modern UI**: Built with Tailwind CSS and custom glassmorphism effects for a stunning, responsive user experience.

## Prerequisites

- Python 3.8+

## How to Run Locally

1. **Clone or Download** the project repository.
2. **Navigate** to the project directory:
   ```bash
   cd path/to/Major_Project
   ```
3. **(Optional but recommended)** Create and activate a virtual environment:
   - Windows: `python -m venv venv` and `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` and `source venv/bin/activate`
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Application**:
   ```bash
   python app.py
   ```
6. **Access the platform**:
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Admin Setup

You can create an Admin user directly from the registration page by selecting "Admin" as your role during sign-up. Once registered and logged in, you will have access to the Admin Dashboard.

## Project Structure

- `app.py`: Application entry point and database initialization.
- `models.py`: SQLAlchemy database models.
- `config.py`: Application configuration settings.
- `forms.py`: Flask-WTF form definitions.
- `routes/`: Modular Flask blueprints for auth, student, instructor, and admin.
- `templates/`: HTML templates utilizing Jinja2 and Tailwind CSS.
- `static/`: Custom CSS styling and JavaScript.
