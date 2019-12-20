from flask import abort
from flask_restplus import Resource, marshal_with_field, fields

import src.services
from src.api.serialization_models import TensorflowModels

tf_api = TensorflowModels.api
tf_request_parser = TensorflowModels.parser
tf_response_model = TensorflowModels.response_model


@tf_api.route('/<string:model_name>/predict')
@tf_api.param(
    'model_name', 'The tf model to use, '
    'try one of: bow-spanish, lstm-multiligual')
class ModelServer(Resource):
    """Serves a prediction from a selected model"""

    @tf_api.expect(tf_request_parser)
    @tf_api.marshal_with(tf_response_model, envelope='ModelPrediction')
    def post(self, model_name):
        """Send a title, sentence or short text, retrieve the Doc Embedding"""

        model_names = src.services.model_service.operational_models.keys()
        if model_name not in model_names:
            abort(404, 'Model not available: {}'.format(model_name))

        args = tf_request_parser.parse_args(strict=True)
        title = args.pop('title')
        length = args.pop('length')

        if not title:
            abort(422, description="Empty title")
        if length < 1 or length > 2000:
            abort(400, 'Parameter length should be positive and under 2000')

        model = src.services.model_service.operational_models[model_name]

        try:
            processed_title, numerified_title = \
                model.processor.preprocess_pipeline(title)
            title_input = model.prepare_input(
                numerified_title,
                max_length=length if 'bow-spanish' not in model.name else 20
            )

            feed_dict = model.create_feed_dict(title_input, **args)
            result = model.predict(feed_dict)

        except Exception:
            src.services.app_logger.exception(
                'Model failure while processing input'
            )
            abort(503, description='Service Unavailable')

        serializable_result = result.tolist()[0]

        return dict(
            tokenizedTitle=processed_title,
            modelName='bow-spanish',
            modelPrediction=serializable_result
        )

    @marshal_with_field(fields.String)
    def get(self, model_name):
        """
        A simple health check on the model,
        try one of: bow-spanish, lstm-multiligual
        """
        model_names = src.services.model_service.operational_models.keys()
        if model_name not in model_names:
            abort(404, 'Model not available, try one of: {}'.format(
                ", ".join(model_names)
            ))
        return 'Model is operational: {}'.format(model_name)
