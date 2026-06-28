from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Inicie sesión para acceder a esta página."
    login_manager.login_message_category = "info"

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .movie import movie_bp
    from .booking import booking_bp 

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(movie_bp, url_prefix='/movies')
    app.register_blueprint(booking_bp, url_prefix='/booking')


    from flask import redirect, url_for
    @app.route('/')
    def index():
        return redirect(url_for('movie.index'))

    return app

