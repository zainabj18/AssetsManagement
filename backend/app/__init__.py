from flask import Flask
from .core.config import settings
from app.api import bp as api_bp
    
def create_app(config_class=settings):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp)

    return app

