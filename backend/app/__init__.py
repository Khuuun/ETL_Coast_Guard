from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)

    # Register blueprints here
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/api/users")

    from .routes.file_routes import file_bp
    app.register_blueprint(file_bp, url_prefix="/api/files")

    @app.route("/")
    def home():
        return "Connected to PostgreSQL using .env!"

    return app
