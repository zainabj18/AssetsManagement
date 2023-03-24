from .comments import bp as comment_bp
from .crud import bp
from .filter import bp as filter_bp
from .log import bp as log_bp
from .related import bp as related_bp

# add assets sub blueprints to the main asset blueprint
bp.register_blueprint(comment_bp)
bp.register_blueprint(related_bp)
bp.register_blueprint(log_bp)
bp.register_blueprint(filter_bp)
