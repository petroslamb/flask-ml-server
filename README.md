# Simple TF model Service

## Installation

### VirtualEnv

### Setup

## Usage

### Configuration

### Environment files

### Run the Server

## Tests

`python -m unittest discover`


### Integration
Edit `test_env` to point `MODELS_BASE_DIR` to actual models.

`python -m unittest discover -s tests/integration/`

### Coverage

```
coverage run --source src -m unittest discover -s tests/integration/`
coverage report
coverage erase
```

### Unittests

`python -m unittest discover -s tests/unit`

### Linter

`flake8`

## Known Bugs

https://github.com/tensorflow/tensorflow/issues/34607

## Improvements

# Extra Documentation

## High Availability Setup

## Independent model loading

## Logging

## Repetitive requests

## Server resource depletion

## Security

