import os
from pathlib import Path

from flask import Flask, render_template

from config import config_by_name
from .extensions import db, login_manager, mail, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(
        config_by_name[config_name or os.getenv("FLASK_ENV", "default")]
    )
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import models
    from .models import User

    # Create tables automatically (temporary for Render Free)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    register_blueprints(app)
    register_commands(app)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    return app


def register_blueprints(app: Flask) -> None:
    from .admin.routes import bp as admin_bp
    from .auth.routes import bp as auth_bp
    from .dashboard.routes import bp as dashboard_bp
    from .doctors.routes import bp as doctors_bp
    from .main.routes import bp as main_bp
    from .pets.routes import bp as pets_bp
    from .reviews.routes import bp as reviews_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(pets_bp, url_prefix="/pets")
    app.register_blueprint(doctors_bp, url_prefix="/specialists")
    app.register_blueprint(reviews_bp, url_prefix="/reviews")


def register_commands(app: Flask) -> None:
    from .services.seed import seed_demo_data

    @app.cli.command("seed")
    def seed_command():
        """Create database tables and demo data."""
        seed_demo_data()
        print("Demo data created. Login: owner@example.com / password123")