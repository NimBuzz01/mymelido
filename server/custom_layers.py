import tensorflow as tf
from tensorflow.keras import layers, backend as K
import keras
from transformers import TFBertModel
import warnings
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
warnings.filterwarnings('ignore')
from config import Config

config = Config()

@keras.saving.register_keras_serializable(package="CustomLayers")
class AudioPreprocessLayer(layers.Layer):
    """Custom layer for audio preprocessing"""
    def __init__(self, target_shape, **kwargs):
        super().__init__(**kwargs)
        self.target_shape = target_shape
        self.pad_size = target_shape - config.AUDIO_INPUT_SHAPE

    def call(self, inputs):
        x = tf.pad(inputs, [[0, 0], [0, self.pad_size]])
        return tf.reshape(x, [-1, 216, 256, 1])

    def get_config(self):
        return {'target_shape': self.target_shape}

@keras.saving.register_keras_serializable(package="CustomLayers")
class NormalizeEmbeddingLayer(layers.Layer):
    """Custom layer for L2 normalization"""
    def call(self, inputs):
        return tf.math.l2_normalize(inputs, axis=1)

@keras.saving.register_keras_serializable(package="CustomLayers")
class StackEmbeddingsLayer(layers.Layer):
    """Custom layer for stacking embeddings"""
    def call(self, inputs):
        anchor, positive, negative = inputs['anchor'], inputs['positive'], inputs['negative']
        return tf.stack([anchor, positive, negative], axis=1)
    
@keras.saving.register_keras_serializable(package="CustomLayers")
class BertEmbeddingLayer(layers.Layer):
    def __init__(self, model_name='bert-base-uncased', **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.bert_model = None

    def build(self, input_shape):
        self.bert_model = TFBertModel.from_pretrained(self.model_name)
        for layer in self.bert_model.layers[:8]:
            layer.trainable = False

    def call(self, inputs):
        input_ids, attention_mask = inputs
        outputs = self.bert_model(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.pooler_output

    def get_config(self):
        config = super().get_config()
        config.update({
            'model_name': self.model_name,
            'dtype': self.dtype.name 
        })
        return config

    @classmethod
    def from_config(cls, config):
        if 'dtype' in config and isinstance(config['dtype'], dict):
            config['dtype'] = config['dtype'].get('config', {}).get('name', 'float32')
        return cls(**config)
    
@keras.saving.register_keras_serializable(package="CustomLayers")
class TripletAccuracyMetric(tf.keras.metrics.Metric):
    def __init__(self, name='triplet_accuracy', **kwargs):
        super().__init__(name=name, **kwargs)
        self.correct = self.add_weight(name='correct', initializer='zeros')
        self.total = self.add_weight(name='total', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        anchor, positive, negative = y_pred[:, 0, :], y_pred[:, 1, :], y_pred[:, 2, :]
        pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
        neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
        correct = tf.cast(pos_dist < neg_dist, tf.float32)
        self.correct.assign_add(tf.reduce_sum(correct))
        self.total.assign_add(tf.cast(tf.size(correct), tf.float32))

    def result(self):
        return self.correct / self.total

    def reset_state(self):
        self.correct.assign(0.)
        self.total.assign(0.)
    
@keras.saving.register_keras_serializable(package="CustomLayers")
def triplet_loss(margin=0.3):
    def loss(y_true, y_pred):
        anchor, positive, negative = y_pred[:, 0, :], y_pred[:, 1, :], y_pred[:, 2, :]
        pos_dist = K.sum(K.square(anchor - positive), axis=-1)
        neg_dist = K.sum(K.square(anchor - negative), axis=-1)
        return K.mean(K.log(1 + K.exp(pos_dist - neg_dist + margin)))
    return loss