from flask import Blueprint,request
from app.schemas import UserCreate
from pydantic.error_wrappers import ValidationError
bp = Blueprint("auth", __name__,url_prefix="/auth")

@bp.route('/register',methods =['POST'])
def login():
    try:
        UserCreate(**request.json)
    except ValidationError as e:
        return e.json(),400
    

    return {"msg":"auth"}