from pathlib import Path

from dotenv import load_dotenv
from flask_testing import TestCase

# Initialize environment
env_path = Path(__file__).resolve().parent / 'test_env'
load_dotenv(dotenv_path=env_path)

from src.app import create_app as create_server_app  # noqa


class TestCaseBase(TestCase):

    def create_app(self):
        app = create_server_app()
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
