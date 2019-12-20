from src.backend.validations import EnvironmentValidator, PathValidator
from src.backend.tf_models import available_model_classes
import src.services


class ModelService:

    def __init__(self, enabled_model_names=None):

        self.env_validator = EnvironmentValidator()
        self.path_validator = PathValidator(self.env_validator)
        self.filepaths = self.path_validator.model_filepaths
        self.enabled_classes = self.get_enabled_model_classes(
            enabled_model_names
        )
        self.valid_classes = self.get_valid_model_classes()
        self.operational_models = self.get_operational_models()

    def get_operational_models(self):
        operational_models = {}
        for model_name, model_class in self.valid_classes.items():
            try:
                model_obj = model_class(
                    self.filepaths.get(model_name)
                )
                operational_models[model_name] = model_obj
            except Exception:
                src.services.app_logger.exception(
                    'Model initialization failed: {}'.format(
                        model_name
                    )
                )
                src.services.app_logger.warning(
                    'Model unavailable: {}'.format(model_name)
                )
                operational_models[model_name] = None
        return operational_models

    def get_enabled_model_classes(self, enabled_model_names):
        return [
            model_class for model_class in available_model_classes
            if model_class.name in enabled_model_names
        ]

    def get_valid_model_classes(self):
        return {
            model_class.name: model_class
            for model_class in self.enabled_classes
            if self.path_validator.is_model_valid(model_class.name)
        }
