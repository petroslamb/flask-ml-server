import json

import tensorflow as tf

from src.backend.processors import SimpleProcessorWithOOVSupport


class BaseTensorflowModel:
    name = None

    def __init__(self, model_paths):
        self.paths = model_paths

        with self.paths['word_mapping.json'].open(mode='r') as f:
            self.word_mapping = json.load(f)

        self.processor = SimpleProcessorWithOOVSupport(
            self.word_mapping
        )
        self.session = tf.compat.v1.Session()
        self.load_model(self.session)
        inputs_output = self.create_model_inputs_outputs()
        self.inputs = inputs_output.get('inputs')
        self.output = inputs_output.get('output')

    def load_model(self, session):
        tf.compat.v1.disable_eager_execution()
        new_saver = tf.compat.v1.train.import_meta_graph(
            self.paths['tensorflow_model.meta'].as_posix()
        )
        new_saver.restore(
            session, self.paths['tensorflow_model'].as_posix()
        )

    def prepare_input(self, numerified_input, max_length=20):
        numerified_seqs = [list(numerified_input)]
        input_seqs = tf.keras.preprocessing.sequence.pad_sequences(
            numerified_seqs,
            maxlen=max_length,
            dtype='float32',
            padding='post',
            value=0.0
        )
        return input_seqs

    def create_empty_feed_dict(self):
        return dict.fromkeys(list(self.inputs.values()))

    def predict(self, feed_dict):
        return self.session.run(self.output, feed_dict)

    def create_model_inputs_outputs(self):
        raise NotImplementedError()

    def create_feed_dict(self, *args, **kwargs):
        raise NotImplementedError()


class BOWSpanish(BaseTensorflowModel):

    name = 'bow-spanish'

    def create_model_inputs_outputs(self):

        graph = tf.compat.v1.get_default_graph()

        title = graph.get_tensor_by_name('input/title:0')
        dense_dropout = graph.get_tensor_by_name(
            "config/dense_dropout_keep_prob:0"
        )
        title_dropout = graph.get_tensor_by_name(
            "config/title_dropout_keep_prob:0"
        )
        output = graph.get_tensor_by_name(
            'target-embedding/title_sub_network/clickability/'
            'add_title_emb/apply_title_to_vec_func/reduced_title_emb:0'
        )
        return dict(
            inputs=dict(
                title=title,
                dense_dropout=dense_dropout,
                title_dropout=title_dropout,
            ),
            output=output)

    def create_feed_dict(self, prepared_input, **kwargs):
        feed_dict = self.create_empty_feed_dict()
        feed_dict[self.inputs['title']] = prepared_input
        feed_dict[self.inputs['title_dropout']] = kwargs.get(
            'title_dropout', 1.0
        )
        feed_dict[self.inputs['dense_dropout']] = kwargs.get(
            'dense_dropout', 1.0
        )
        return feed_dict


class LSTMMultilingual(BaseTensorflowModel):
    name = 'lstm-multilingual'


available_model_classes = [BOWSpanish, LSTMMultilingual]
