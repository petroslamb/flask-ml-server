from pathlib import Path
from dotenv import load_dotenv
from flask_testing import TestCase

env_path = Path('..') / '.test_env'
load_dotenv(dotenv_path=env_path)

from src.app import create_app as create_server_app


class TestCaseBase(TestCase):
    
    def create_app(self):
        app = create_server_app()
        return app
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

