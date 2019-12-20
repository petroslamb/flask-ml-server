from flask import Blueprint
from flask_restplus import Api
from src.api.resources import tf_api


api_blueprint = Blueprint('api', __name__)

api = Api(api_blueprint,
          title='Model Prediction Serving REST API ',
          version='1.0',
          description='A Flask web service that helps get predictions '
                      'from Tensoflow Sentence Embedding models'
          )

api.add_namespace(tf_api, path='/model')
