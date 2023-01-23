from flask import Blueprint,request,jsonify
from app.schemas import UserCreate
from app.db import get_db
from pydantic.error_wrappers import ValidationError
from werkzeug.security import generate_password_hash
bp = Blueprint("auth", __name__,url_prefix="/auth")

@bp.route('/register',methods =['POST'])
def login():
    try:
        user=UserCreate(**request.json)
        user_in_db=None
        db = get_db()
        with db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM accounts WHERE username=%(username)s;""",{"username":user.username})
                user_in_db=cur.fetchone()
        if user_in_db:
            return jsonify({"msg":"User already exist with the same username please try a different one.","error":"Username already exist"}),400
    except ValidationError as e:
        return jsonify({"msg":"Data provided is invalid","data":e.errors(),"error":"Failed to create user from on data provided"}),400

    with db.connection() as conn:
        conn.execute("""
        INSERT INTO accounts (first_name,last_name,username, hashed_password, account_type,account_privileges)
VALUES (%(first_name)s,%(last_name)s,%(username)s,%(password)s,%(acc_type)s,%(acc_priv)s);""",{"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"password":generate_password_hash(user.password.get_secret_value()),"acc_type":user.account_type,"acc_priv":user.account_privileges})


    return {"msg":"User registered"}