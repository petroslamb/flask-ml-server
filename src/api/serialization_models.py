from flask_restplus import Namespace, fields, reqparse


class TensorflowModels:
    api = Namespace(
        'models', description='Tensorflow models related operations'
    )
    parser = reqparse.RequestParser()
    parser.add_argument(
        'title', type=str, required=True,
        help='A sentence for which we want the Sentence Embedding.'
             'Truncated down to 20 words for bow-spanish model.'
    )
    parser.add_argument(
        'length', type=int, required=False, default=20,
        help='The length of the input sentence in words.'
             'Truncated down to 20 words for bow-spanish model.'
    )
    parser.add_argument(
        'title_dropout', type=float, required=False, default=1.0,
        help='A float that controls the model dropout.'
    )
    parser.add_argument(
        'dense_dropout', type=float, required=False, default=1.0,
        help='A float that controls the model dropout on the dense layer.'

    )
    response_model = api.model('PredictionResponse', {
        'tokenizedTitle': fields.List(fields.String),
        'modelName': fields.String,
        'modelPrediction': fields.List(fields.Float)
    })
