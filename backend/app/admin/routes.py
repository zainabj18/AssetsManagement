from flask import Blueprint,request,jsonify
from app.schemas import UserCreate,UserInDB
from app.db import get_db,UserRole
from app.core.utils import protected
from pydantic.error_wrappers import ValidationError
from werkzeug.security import generate_password_hash,check_password_hash
from psycopg import Error
from flask import current_app
from datetime import timedelta,datetime
import jwt
from psycopg.rows import class_row
bp = Blueprint("admin", __name__,url_prefix="/admin")

@bp.route('/accountmanager',methods =['GET'])
def types():
    return {"msg":""},200
