import json
from tests.integration.common import TestCaseBase

def post_to_bow_spanish(self, payload):
    return self.client.post(
        '/api/v1/model/bow-spanish/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )


class TestModels(TestCaseBase):

    def test_post_valid_text_to_bow_spanish(self):
        with self.client:
            response = post_to_bow_spanish(self, dict(title='Arriba, abajo lento lento!'))
            self.assert_200(response)
            data = json.loads(response.data.decode())
            self.assertListEqual(
                data['ModelPrediction']['tokenizedTitle'],
                ['arriba', 'abajo', 'lento', 'lento']
            )
            self.assertEqual(
                data['ModelPrediction']['modelName'],
                'bow-spanish'
            )
            self.assertEqual(
                len(data['ModelPrediction']['modelPrediction']),
                300
            )
            for data_point in data['ModelPrediction']['modelPrediction']:
                self.assertIsInstance(data_point, float)
