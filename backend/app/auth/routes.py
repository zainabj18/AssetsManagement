from flask import Blueprint,request,jsonify
from app.schemas import UserCreate
from app.db import get_db
from pydantic.error_wrappers import ValidationError
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
            return jsonify({"msg":"User already exist with the same username please try a different one."}),400

    except ValidationError as e:
        return e.json(),400
    

    return {"msg":"auth"}