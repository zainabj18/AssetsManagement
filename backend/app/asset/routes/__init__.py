from .crud import bp
from .comments import bp as comment_bp
from .related import bp as related_bp
from .log import bp as log_bp
from .filter import bp as filter_bp
bp.register_blueprint(comment_bp)
bp.register_blueprint(related_bp)
bp.register_blueprint(log_bp)
bp.register_blueprint(filter_bp)