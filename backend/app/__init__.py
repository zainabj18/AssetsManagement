from flask import Flask
from .core.config import settings

def create_app(config_class=settings):
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app

