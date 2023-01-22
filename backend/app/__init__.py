from flask import Flask
from app.core.config import settings
from app.api import bp as api_bp
from flask import Flask, Response

class JSONResponse(Response):
    default_mimetype = 'application/json'

class FlaskAPI(Flask):
    response_class = JSONResponse


def create_app(config_class=settings):
    app = FlaskAPI(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp)
    return app

