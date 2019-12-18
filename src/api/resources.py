from flask import current_app
from flask_restplus import Resource, marshal_with_field, fields

from src.api.serialization_models import TensorflowModels

tf_api = TensorflowModels.api
tf_request_parser = TensorflowModels.parser
tf_response_model = TensorflowModels.response_model


@tf_api.route('/bow_spanish/predict')
class ModelServer(Resource):
    """Serves a prediction from a selected model"""

    @tf_api.expect(tf_request_parser)
    @tf_api.marshal_with(tf_response_model, envelope='ModelPrediction')
    def post(self):
        """Send a title up to 20 words and retrieve the Sentence Embedding"""
        model = current_app.model_server.models['bow_spanish']


        return {'tokenizedTitle': ['the', 'some'], 'modelName': 'spanish bow', 'modelPrediction': [-1.1, 2.2]}

    @marshal_with_field(fields.String)
    def get(self):
        """A simple health check on the model"""
        return 'The model is operational'
