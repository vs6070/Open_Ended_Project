from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from models import db, User

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.instructor import instructor_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    # Create DB tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
