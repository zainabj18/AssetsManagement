from app.api import bp as api_bp
from app.core.config import settings
from app.db import close_db, init_db_command
from flask import Flask, Response
from flask_cors import CORS


class JSONResponse(Response):
    default_mimetype = "application/json"


class FlaskAPI(Flask):
    response_class = JSONResponse


def create_app(config_class=settings):
    app = FlaskAPI(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    return app
