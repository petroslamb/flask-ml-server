from pathlib import Path
from flask import current_app


class EnvironmentValidator:

    def __init__(self):

        self.models_base_path = current_app.config.get('MODELS_BASE_DIR')
        self.model_names = current_app.config.get('MODEL_NAMES')
        self.model_file_names = current_app.get('MODEL_FILE_NAMES')

        self.validate_environment()

    def validate_environment(self):
        if not self.models_base_path:
            current_app.logger.error('No models base directory found in configuration')
            raise EnvironmentError('No models base directory')

        if self.model_names:
            self.model_names = self.model_names.split(',')
        else:
            current_app.logger.error('No model names found in configuration')
            raise EnvironmentError('No model names')

        if self.model_file_names:
            self.model_file_names = self.model_file_names.split(',')
        else:
            current_app.logger.error('No model file names found in configuration')
            raise EnvironmentError('No model file names')


class PathValidator:

    def __init__(self, env_validator):

        self.operational_models = {
            model_name: True for model_name in env_validator.model_names
        }
        self.models_base_path = self.validate_base_path(
            env_validator.models_base_path
        )
        self.model_filepaths = self.validate_model_filepaths(
            env_validator.model_file_names
        )

    def is_model_valid(self, model_name):
        if self.operational_models.get(model_name):
            return True
        return False

    def validate_base_path(self, models_base_pathname):

        models_base_path = Path(models_base_pathname)
        if not self.check_dirpath(models_base_path):
            current_app.logger.error(
                'Provided models base dir does not exist:{}'.format(
                    models_base_path
                )
            )
            raise OSError('Directory does not exist: {}'.format(
                models_base_path
            ))
        return models_base_path

    def validate_model_filepaths(self, model_filenames):

        model_filepaths = {}
        for model_name in self.operational_models.keys():
            model_filepaths.update({model_name: {}})

            for filename in model_filenames:
                file_path = \
                    self.models_base_path / model_name / filename

                model_filepaths[model_name].update(
                    {filename: file_path}
                )
                if not self.check_filepath(file_path):
                    self.operational_models[model_name] = False
                    model_filepaths[model_name][filename] = None

                    current_app.logger.error(
                        'Provided file path does not exist:{}'.format(
                            file_path
                        )
                    )
                    current_app.logger.warning(
                        '{} is not operational'.format(model_name)
                    )
        return model_filepaths

    @staticmethod
    def check_dirpath(path):
            if path.exists() and path.isdir():
                return True
            return False

    @staticmethod
    def check_filepath(path):
        if path.exists() and path.isfile():
            return True
        return False
