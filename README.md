# Simple TF model Service

A (hopefully) organized Flask powered Web REST API, to serve Tensorflow models.

Written in a hurry!

#### Features

The service tries to showcase production level organization, code and features. 

Included is, but not limited to:

- Supports multiple models, controls enabled ones from configuration.
- Checks, validates and serves only correct models.
- Works even if some of the models fail at runtime.
- Supports both v1, v2 versions of `Tensorflow` models , 
by using `Tensorflow 2.0` and running `v1` models with `tf.compat.v1`.
- Full support for `dev, test, prod` environments.
- Extended configuration, via environment variables.
- Environment files can be used as well.
- Logging support for file and console logs.
- Tries for well organized code.
- Tries for production level logging and error handling
- Swagger.


#### Limitations

Things are far from perfect:

- Due to time constraint, the model only supports the `bow-spanish` model.
- No support for a production WSGI server, due to time constraint.
- `TFv2` has been used as there was no suggestion for the model version, but this introduced a bug.
- Finally the models were found to be of `v1` and loaded by using compatibility mode with `v1`.
- Enpoints were not implemented exactly as requested, but in a fashion that is similar.
- Limited documentation and testing.
- Has many rough edges and unifished details as was written in a haste (~5days).
- There is known bug, in `development` mode.

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

### Env files usage

Edit `env` file to create a `.env` file, if you like to use it.

- Make sure to pinpoint to your models directory.

### Run the server

To run with a different env file use `dotenv`:

`dotenv -f .env_dev run python scripts/manage.py run`

To run with your created `.env`, use installed CLI:

`my-server-manage run`

- Access at `localhost:5000/api/v1` by default.
- If not `.env` file is present, defaults will be overriden by env vars.
- It is strogly recommended to use an env file, as testing was done with one.
- Use `FLASK_ENV=testing`, for better results.

### Configuration options

There are three operational modes:

- `development` with debugger, autoreload and console logs on at DEBUG level.
- `testing` with file log and console log, with logs at INFO level, no debugger, but flask testing on.
- `production` only file log, logs at WARNING level.

**ATTENTION:** `develompent` mode breaks with a known bug, description is in a relevant section of the Readme.

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

Bug appears during startup in `development` mode,  when the debugger mode is enabled.

```
ModuleNotFoundError: No module named 'tensorflow_core.keras' in Flask #34607
```

In an open bug:

https://github.com/tensorflow/tensorflow/issues/34607


Solution is to downgrade tensorflow to v1.

## Future Improvements

The following list was not implemented, for lack of time.

- Fix known bug, as trying for `TF2` is not a good idea yet.
- Second model to be introduced (`lstm-multilingual`).
- Support for production level WSGI server, like Gunicorn. https://gunicorn.org/
- More integration tests.
- Unit testing.
- Doc strings.
- Use private functions, members and properties in classes.
- General code cleanup and finish on TODO's.
- Fix many typos, and missing details,  because of haste.

## Extra Documentation

Answers to Bonus Questions.

### High Availability Setup

- Use multiple instances behind a load balancer.
- Use a multi-app deployment WSGI server like uWSGI Emperor for multiple worker support.
https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html

### Independent model loading

- Implemented, independence both at startup and runtime errors.

### Logging functionality

- Implemented, both file and console, with adjusted levels according to environment.

### Swagger support

- Implemented, tries for friendly messages.

### Repetitive requests with big model computation

The word is probably caching. There are three levels to be considered:

- At the web proxy (nginx) level, to send identical responses to identical requests
- In memory of the Flask application, keep a list of requested titles/docs and their responses
- With a separate caching server like Redis (https://redis.io/), to keep a list of requested titles/docs and their responses

### Server resource depletion

- Again multiple servers, but on different machines, behind a load balancer.

### Security concerns

- Might help to implement security tokens for access.
- Throttling for DOS attacks.
- Production level WSGI server
