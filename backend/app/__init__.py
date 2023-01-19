from flask import Flask
from .core.config import Base

def create_app(config_class=None):
    app = Flask(__name__)
    config_class=config_class if config_class else Base()
    app.config.from_object(config_class)
    return app

