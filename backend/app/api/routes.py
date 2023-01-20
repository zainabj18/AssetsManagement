from app.api import bp
from app.core.config import settings
@bp.route('/')
def index():
    return {"msg":"Hello World!","version":settings.API_VERSION,"url":settings.APPLICATION_ROOT_URL}