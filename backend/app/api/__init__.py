from flask import Blueprint
from app.core.config import settings
bp = Blueprint("api", __name__,url_prefix=settings.APPLICATION_ROOT_URL)
from app.api import routes