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
bp = Blueprint("auth", __name__,url_prefix="/auth")

#TODO:Add to a common_func in db
def create_user(db,user):
    with db.connection() as conn:
        conn.execute("""
        INSERT INTO accounts (first_name,last_name,username, hashed_password, account_type,account_privileges)
VALUES (%(first_name)s,%(last_name)s,%(username)s,%(password)s,%(acc_type)s,%(acc_priv)s);""",{"first_name":user.first_name,"last_name":user.last_name,"username":user.username,"password":generate_password_hash(user.password.get_secret_value()),"acc_type":user.account_type,"acc_priv":user.account_privileges})

def get_user(db,username):
    with db.connection() as conn:
        with conn.cursor(row_factory=class_row(UserInDB)) as cur:
            cur.execute("""SELECT * FROM accounts WHERE username=%(username)s;""",{"username":username})
            user_in_db=cur.fetchone()
            return user_in_db
    


@bp.route('/register',methods =['POST'])
def register():
    try:
        user=UserCreate(**request.json)
        db = get_db()
        if get_user(db,user.username) is not None:
            return jsonify({"msg":"User already exist with the same username please try a different one.","error":"Username already exist"}),400
        print(get_user(db,user.username))
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

    return {"msg":"User registered"},201

@bp.route('/login',methods =['POST'])
def login():
    if 'username' not in request.json or 'password' not in request.json:
        return {"msg":"username and password required","error":"Invalid credentials"},400
    username=request.json['username']
    pwd=request.json['password']
    db = get_db()
    try:
        if not (user_in_db:=get_user(db,username)):
            return {"msg":"account doesn't exist","error":"Invalid credentials"},401
    except Error as e:
        return {"msg":str(e),"error":"Database Connection Error"},500
    if not check_password_hash(user_in_db.hashed_password.get_secret_value(),pwd):
        return {"msg":"invalid username/password combination","error":"Invalid credentials"},401
    
    token = jwt.encode({
            'account_id': int(user_in_db.account_id),
            'account_type':user_in_db.account_type.value,
            'account_privileges':user_in_db.account_privileges.value,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, current_app.config["SECRET_KEY"],algorithm=current_app.config["JWT_ALGO"])
    return {"msg":"Success","token":token},201
  

@bp.route('/admin-status',methods =['GET'])
@protected(role=UserRole.ADMIN)
def is_admin(user_id,access_level):
    return {"msg":f"{user_id} You have admin privileges and data access level of {access_level}"},200


@bp.route('/user-status',methods =['GET'])
@protected(role=UserRole.USER)
def is_user(user_id,access_level):
    return {"msg":f"{user_id} You have user privileges and data access level of {access_level}"},200

@bp.route('/viewer-status',methods =['GET'])
@protected(role=UserRole.VIEWER)
def is_viewer(user_id,access_level):
    return {"msg":f"{user_id} You have viewer privileges and data access level of {access_level}"},200


