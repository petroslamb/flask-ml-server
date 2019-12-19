from gensim.utils import simple_preprocess

import src.services


class BaseProcessor:

    def tokenize_text(self, text):
        raise NotImplementedError()

    def filter_tokens(self, tokenized_text):
        raise NotImplementedError()

    def numerify_tokens(self, tokenized_text):
        raise NotImplementedError()

    def preprocess_pipeline(self, text_input):
        raise NotImplementedError()


class SimpleProcessorWithOOVSupport(BaseProcessor):

    def __init__(self, word_mapping):
        self.word_mapping = word_mapping
        self.oov = src.services.app_config.get('OOV_TOKEN')
        self.oov_numeric = word_mapping.get(self.oov)
        self.dictionary = list(self.word_mapping.keys())

    def tokenize_text(self, text):
        return simple_preprocess(text)

    def filter_tokens_with_oov(self, tokenized_text):
        return (
            self.oov if token not in self.dictionary
            else token for token in tokenized_text
        )

    def filter_tokens(self, tokenized_text):
        return (
            token for token in tokenized_text
            if token in self.dictionary
        )

    def numerify_tokens(self, filtered_tokens):
        return (
            self.word_mapping.get(token)
            for token in filtered_tokens
        )

    @staticmethod
    def _remove_none_and_empty_tokens(tokens):
        return (token for token in tokens if token)

    def preprocess_pipeline(self, text_input):
        if not text_input:
            raise ValueError('No text input provided: {}'.format(text_input))
        assert isinstance(text_input, str)

        tokenized_text = self.tokenize_text(text_input)

        if self.oov_numeric:
            filtered_tokens = self.filter_tokens_with_oov(tokenized_text)
        else:
            filtered_tokens = self.filter_tokens(tokenized_text)

        # Turn generators to be returned into lists, for ease of use
        prepared_tokens = list(
            self._remove_none_and_empty_tokens(filtered_tokens)
        )
        prepared_input = list(
            self.numerify_tokens(prepared_tokens)
        )
        return prepared_tokens, prepared_input
