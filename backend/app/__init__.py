from flask import Flask
from .core.config import Base

def create_app(config_class=Base()):
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app

