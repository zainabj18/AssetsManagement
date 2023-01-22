from flask import Flask
from app.core.config import settings
from app.api import bp as api_bp
from flask import Flask, Response
from app.db import db

class JSONResponse(Response):
    default_mimetype = 'application/json'

class FlaskAPI(Flask):
    response_class = JSONResponse


def create_app(config_class=settings):
    app = FlaskAPI(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp)
    app.teardown_appcontext(db.close_db)
    return app

