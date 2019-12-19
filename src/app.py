import os
import copy
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler


def configure_logging(app):
    if app.config['LOG_FILE']:
        file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000, backupCount=1)
        file_handler.formatter = default_handler.formatter
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
    if not app.config['CONSOLE_LOG']:
        app.logger.removeHandler(default_handler)
    return app


def create_app(script_info=None):
    
    # Instantiate the app
    app = Flask(__name__,)

    app = initialize_configuration(app)
    app = initialize_logging(app)
    app = register_blueprints(app)
    app = initialize_services(app)
    return app


def initialize_configuration(app):
    # internal imports to allow early mocking
    from src.config import config_by_name
    app_environment = os.getenv("FLASK_ENV", "production")
    app.config.from_object(config_by_name[app_environment])
    app.logger.info('Configuration initialized')
    return app


def initialize_logging(app):
    app_environment = os.getenv("FLASK_ENV", "production")
    app = configure_logging(app)
    app.logger.info("Logging initialized")
    app.logger.info(
        "Application environment is set to: {}".format(
            app_environment
        )
    )
    return app


def register_blueprints(app):
    # internal imports to allow early mocking
    from src.api.blueprint import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.logger.info("API initialized")
    return app


def initialize_services(app):
    # internal imports to allow early mocking
    from src import services
    from src.backend.model_service import ModelService
    services.app_logger = app.logger
    services.app_config = copy.deepcopy(app.config)
    services.model_service = ModelService(
        app.config.get('MODEL_NAMES')
    )
    app.logger.info("Services intitialized")
    return app
