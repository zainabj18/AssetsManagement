from app.core.config import settings
from flask import Blueprint
from app.auth.routes import bp as auth_bp

bp = Blueprint("api", __name__,url_prefix=settings.APPLICATION_ROOT_URL)
@bp.route('/')
def index():
    return {"msg":"Hello World!","version":settings.API_VERSION,"url":settings.APPLICATION_ROOT_URL}
bp.register_blueprint(auth_bp)

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/assets/<int:asset_id>/comments', methods=['POST'])
def create_comment(asset_id):
    data = request.json
    if not data or not isinstance(data.get('username'), str) or not isinstance(data.get('content'), str):
        raise BadRequest('Invalid request data')

    comment = Comment(asset_id=asset_id, username=data['username'], content=data['content'])
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201
