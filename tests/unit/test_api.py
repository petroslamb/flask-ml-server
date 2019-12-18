import json
from tests.unit.common import TestCaseBase


def post_to_bow_spanish(self, payload):
    return self.client.post(
        '/api/v1/model/bow_spanish/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )


class TestModels(TestCaseBase):

    def test_post_valid_text_to_bow_spanish(self):
        with self.client:
            response = post_to_bow_spanish(self, dict(title='Ariba!'))
            self.assert_200(response)
            print(response)
            data = json.loads(response.data.decode())
            print(data)
