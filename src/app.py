import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler

from src.config import config_by_name
from src.backend.model_service import ModelServer


def configure_logging(app):
    if app.config['LOG_FILE']:
        file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
        file_handler.formatter = default_handler.formatter
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
    if not app.config['CONSOLE_LOG']:
        app.logger.removeHandler(default_handler)


def create_app(script_info=None):
    
    # instantiate the app
    app = Flask(
        __name__,
    )

    # set config
    app_settings = os.getenv(
        "FLASK_ENV", "production"
    )
    app.config.from_object(config_by_name[app_settings])

    # configure app logging
    configure_logging(app)
    app.logger.info("Logging initialized")
    
    # register the API in Flask
    from src.api.blueprint import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.logger.info("API initialized")

    app.model_server = ModelServer()
    
    return app