from flask import Blueprint,request,jsonify
from pydantic import ValidationError
from app.schemas import AssetBase
bp = Blueprint("asset", __name__,url_prefix="/asset")

@bp.route('/new',methods =['POST'])
def create():
    try:
        try:
            
            print(AssetBase(**request.json))
        except ValidationError as e:
            return jsonify({"msg":"Data provided is invalid","data":e.errors(),"error":"Failed to create asset from the data provided"}),400
    except Exception as e:
        return jsonify({"msg":"Data provided is invalid","data":None,"error":"Failed to create asset from the data provided"}),400
   

