from flask import Blueprint, jsonify, request

from pydantic import ValidationError
from app.schemas import TagBase

bp = Blueprint("tag", __name__, url_prefix="/tag")



@bp.route("/", methods=["POST"])
def create():
    try:
       TagBase(**request.json)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": e.errors(),
                    "error": "Failed to create tag from the data provided",
                }
            ),
            400,
        )
