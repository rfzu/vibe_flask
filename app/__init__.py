"""Application factory."""
from flask import Flask

from app.config import config


def create_app(config_name="default"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("404.html"), 404

    return app
