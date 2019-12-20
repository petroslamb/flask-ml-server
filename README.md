# Simple TF model Service

A well organized Flask powered Web REST API, to serve Tensorflow models.

#### Features

- Supports multiple models, controls enabled ones from configuration.
- Checks, validates and serves only correct models.
- Works even if some of the models fail at runtime.
- Full support for `dev, test, prod` environments.
- Extended configuration, via environment variables.
- Environment files can be used as well.
- Well organized code.
- Logging and error handling
- Swagger.

#### Limitations

- Due to time constraint, the model only supports the `bow-spanish` model.
- `TFv2` has been used, although the models were loaded by using compatibility mode with `v1`.
- Enpoints were not implemented exactly as requested, but in a fashion that is similar.
- Limited documentation and testing.

## Installation

Create a `virtualenv`, as is best practice first. From the base folder of the project run:

`pip install .`

### Setup the model files

You need to provide the location of the model files. Each model directory should have the name of the model.
Both model directories should be located under a base directory.

 - `MODEL_NAMES` is the env var to use for the model directories.
 - `MODELS_BASE_DIR` declares the base dir of the model directories.
 - `MODEL_FILES` declares the names of the files for each model.

## Usage


### Configuration options


Below is a list of most the configuration options:

```
   "FLASK_APP", "Sentence Embeddings Server"
   'SECRET_KEY', 'my_precious_secret_key'
   'FLASK_ENV', 'env_name'
   'DEBUG', False
   'LOG_FILE', 'api.log'
   'LOG_LEVEL', logging.INFO
   'MODELS_BASE_DIR', '../tf_models'
   'MODEL_NAMES', 'bow-spanish,lstm-multilingual'
   'MODEL_FILES', 'tensorflow_model,net_config.json,tensorflow_model.meta,word_mapping.json'
   'CONSOLE_LOG', True

```
- Most can be changed via env vars.
- Changing the `env_name` to `development`, `testing` or `production`,
will override certain options for safety or ease of use.

### Env files usage

Edit `env` file to create a `.env` file, if you like to use it.

- Make sure to pinpoint to your models directory.

### Run the server

To run with a different env file use `dotenv`:

`dotenv -f .env_dev run python scripts/manage.py run`

To run with your created `.env`, use installed CLI:

`my-server-manage run`

- If not `.env` file is present, defaults will be overriden by env vars.
- It is strogly recommended to use an env file, as testing was done with one.

## Tests

To run all tests:

`python -m unittest discover`

### Integration tests

Edit `test_env` to point `MODELS_BASE_DIR` to your actual models.

Alternatively add the model files in to the `tests/integration/data` folder.

`python -m unittest discover -s tests/integration/`

- There is a single integration test, inorder to showcase the functionality.
- Time constraint did not allow for more testing.

#### Test Coverage

To find the coverage, try:
```
coverage run --source src -m unittest discover -s tests/integration/`
coverage report
coverage erase
```

Example report from integration tests run (single test):

```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/__init__.py                       0      0   100%
src/api/__init__.py                   0      0   100%
src/api/blueprint.py                  6      0   100%
src/api/resources.py                 38     10    74%
src/api/serialization_models.py       9      0   100%
src/app.py                           47      1    98%
src/backend/__init__.py               0      0   100%
src/backend/model_service.py         26      4    85%
src/backend/processors.py            38      7    82%
src/backend/tf_models.py             49      2    96%
src/backend/validations.py           56     15    73%
src/config.py                        30      0   100%
src/services.py                       3      0   100%
-----------------------------------------------------
TOTAL                               302     39    87%

```

### Unit tests

To run unit tests:

`python -m unittest discover -s tests/unit`

- Unit tests have file placeholders, but have not been implemented.
- Time constraint did not allow for more testing.


### Linter usage

Run `flake8` to keep project linted.

## Known Bugs

Bug appens when DEBUG mode is enabled.

```
ModuleNotFoundError: No module named 'tensorflow_core.keras' in Flask #34607
```

In an open bug:

https://github.com/tensorflow/tensorflow/issues/34607


Solution is to downgrade tensorflow to v1.

## Improvements

The following list was not implemented, for lack of time.

- Second model to be introduced (`lstm-multilingual`)
- More integration tests
- Unit testing
- Doc strings
- Use private functions, members and properties in classes

# Extra Documentation

## High Availability Setup

## Independent model loading

## Logging functionality

## Swagger support

## Repetitive requests

## Server resource depletion

## Security concerns
