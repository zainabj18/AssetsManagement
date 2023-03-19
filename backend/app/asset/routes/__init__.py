from .crud import bp
from .comments import bp as comment_bp
from .related import bp as related_bp
bp.register_blueprint(comment_bp)
bp.register_blueprint(related_bp)