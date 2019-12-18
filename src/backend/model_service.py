from src.backend.validations import EnvironmentValidator, PathValidator
from src.backend.tf_models import available_models

class ModelServer:

    def __init__(self):

        self.env_validator = EnvironmentValidator()
        self.path_validator = PathValidator(self.env_validator)

        self.models = {
            model.model_name: model() for model in available_models
            if self.path_validator.is_model_valid(model.model_name)
        }

    @property
    def bow_spanish(self):
        self.models.get('bow_spanish')

    @property
    def lstm_multilingual(self):
        self.models.get('lstm_multilingual')
