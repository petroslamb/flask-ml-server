import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = os.getenv("FLASK_APP", "Sentence Embeddings Server")
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'custom_env')
    DEBUG = os.getenv('DEBUG', False)
    LOG_FILE = os.getenv('LOG_FILE', 'api.log')
    LOG_LEVEL = os.getenv('LOG_LEVEL', logging.INFO)
    MODELS_BASE_DIR = os.getenv('MODELS_BASE_DIR', '../tf_models')
    MODEL_NAMES = os.getenv(
        'MODEL_NAMES', 'bow-spanish,lstm-multilingual'
    )
    MODEL_FILES = os.getenv(
        'MODEL_FILES',
        'tensorflow_model,net_config.json,'
        'tensorflow_model.meta,word_mapping.json'
    )
    CONSOLE_LOG = os.getenv('CONSOLE_LOG', True)


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    LOG_FILE = None
    LOG_LEVEL = os.getenv('LOG_LEVEL', logging.DEBUG)


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = False
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', logging.INFO)


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    CONSOLE_LOG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', logging.WARNING)


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    custom_env=Config
)

key = Config.SECRET_KEY
