from app.api import bp as api_bp
from app.core.config import settings
from app.db import close_db, init_db_command,build_assets_command
from flask import Flask, Response
from flasgger import Swagger
from flask_cors import CORS
def create_app(config_class=settings):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp)
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(build_assets_command)
    CORS(app)
    return app
