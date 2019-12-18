import json

import tensorflow as tf

from src.backend.processors import SimpleProcessorWithOOVSupport

class BaseTensorflowModel:
    pass


class BOWSpanish(BaseTensorflowModel):
    def __init__(self, paths, model_name='bow-spanish'):
        self.model_name = model_name
        self.paths = paths[model_name]

        with self.paths[self.model_name]['word_mapping.json'].open(mode='r') as f:
            self.word_mapping = json.load(f)

        self.processor = SimpleProcessorWithOOVSupport(self.word_mapping)

        self.session = tf.compat.v1.Session()
        self.load_model(self.session)

    def load_model(self, session):
        new_saver = tf.compat.v1.train.import_meta_graph(
            self.paths['tensorflow_model.meta']
        )
        new_saver.restore(session, self.paths['tensorflow_model'])

    def create_empty_feed_dict_and_output(self):
        graph = tf.compat.v1.get_default_graph()

        title = graph.get_tensor_by_name('input/title:0')
        dense_dropout = graph.get_tensor_by_name("config/dense_dropout_keep_prob:0")
        title_dropout = graph.get_tensor_by_name("config/title_dropout_keep_prob:0")
        output = graph.get_tensor_by_name(
            'target-embedding/title_sub_network/clickability/'
            'add_title_emb/apply_title_to_vec_func/reduced_title_emb:0'
        )
        return dict.fromkeys([title, title_dropout, dense_dropout]), output


class LSTMMultilingual(BaseTensorflowModel):
    pass

available_models = [BOWSpanish, LSTMMultilingual]
