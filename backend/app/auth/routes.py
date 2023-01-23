from flask import Blueprint,request,jsonify
from app.schemas import UserCreate
from app.db import get_db
from pydantic.error_wrappers import ValidationError
from werkzeug.security import generate_password_hash
from psycopg import Error
bp = Blueprint("auth", __name__,url_prefix="/auth")

#TODO:Add to a common_func in db
def create_user(db,user):
    with db.connection() as conn:
        conn.execute("""
        INSERT INTO accounts (first_name,last_name,username, hashed_password, account_type,account_privileges)
VALUES (%(first_name)s,%(last_name)s,%(username)s,%(password)s,%(acc_type)s,%(acc_priv)s);""",{"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"password":generate_password_hash(user.password.get_secret_value()),"acc_type":user.account_type,"acc_priv":user.account_privileges})

@bp.route('/register',methods =['POST'])
def register():
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
    except Error as e:
        #TODO:Add an error enum
        return {"msg":str(e),"error":"Database Connection Error"},500

    try:
        create_user(db,user)
    except Error as e:
        #TODO:Add an error enum
        return {"msg":str(e),"error":"Database Connection Error"},500

    return {"msg":"User registered"}

@bp.route('/login',methods =['POST'])
def login():
    if 'username' not in request.json or 'password' not in request.json:
        return {"msg":"username and password required","error":"Invalid credentials"},400
    username=request.json['username']
  
    db = get_db()
    user_in_db=None
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT hashed_password FROM accounts WHERE username=%(username)s;""",{"username":username})
            user_in_db=cur.fetchone()
    if not user_in_db:
        return {"msg":"account doesn't exist","error":"Invalid credentials"},400

