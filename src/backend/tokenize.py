import json
from flask import current_app
from gensim.utils import simple_preprocess

f = open('../bow-spanish/word_mapping.json', 'r')
word_mapping = json.load(f)

oov_numeric = word_mapping.get(current_app['OOV_TOKEN'])

def tokenize(text):
    return simple_preprocess(text)


def prepare_tokens(tokenized_text, word_mapping, oov_numeric=None):
    prepared_input_with_nones = [
        oov_numeric if word_mapping.get(token) is None else word_mapping.get(token)
        for token in tokenized_text
    ]
    prepared_input = [
        token for token in prepared_input_with_nones
        if token is not None
    ]
    return prepared_input

def preprocess_input(text_input, word_mapping)

