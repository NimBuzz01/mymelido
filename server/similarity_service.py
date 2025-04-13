import numpy as np
from transformers import BertTokenizer, TFBertModel
from tensorflow.keras.utils import register_keras_serializable
import tensorflow as tf
from tensorflow.keras import layers, backend as K
import keras
from config import Config
from audio_processor import AudioPreprocessor

config = Config()

# Define the custom layer with proper serialization
@register_keras_serializable(package="CustomLayers")
class AudioPreprocessLayer(layers.Layer):
    """Custom layer for audio preprocessing"""
    def __init__(self, target_shape, **kwargs):
        super().__init__(**kwargs)
        self.target_shape = target_shape
        # Calculate padding once during init
        self.pad_size = target_shape - config.AUDIO_INPUT_SHAPE
        # Precompute the full padding configuration
        self.paddings = tf.constant([[0, 0], [0, self.pad_size]])

    def call(self, inputs):
        # Convert to tensor explicitly
        if not isinstance(inputs, tf.Tensor):
            inputs = tf.convert_to_tensor(inputs)
        
        # Use tf.pad with the precomputed constant
        padded = tf.pad(inputs, self.paddings)
        
        # Reshape to target dimensions
        return tf.reshape(padded, [-1, 216, 256, 1])

    def get_config(self):
        return {'target_shape': self.target_shape}

@register_keras_serializable(package="CustomLayers")
class NormalizeEmbeddingLayer(layers.Layer):
    """Custom layer for L2 normalization"""
    def call(self, inputs):
        return tf.math.l2_normalize(inputs, axis=1)

@register_keras_serializable(package="CustomLayers")
class StackEmbeddingsLayer(layers.Layer):
    """Custom layer for stacking embeddings"""
    def call(self, inputs):
        anchor, positive, negative = inputs['anchor'], inputs['positive'], inputs['negative']
        return tf.stack([anchor, positive, negative], axis=1)
    
@register_keras_serializable(package="CustomLayers")
class BertEmbeddingLayer(layers.Layer):
    """Custom layer to properly integrate BERT with Keras"""
    def __init__(self, model_name='bert-base-uncased', **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.bert_model = None

    def build(self, input_shape):
        self.bert_model = TFBertModel.from_pretrained(self.model_name)
        # Freeze first 8 layers
        for layer in self.bert_model.layers[:8]:
            layer.trainable = False

    def call(self, inputs):
        input_ids, attention_mask = inputs
        outputs = self.bert_model(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.pooler_output

    def get_config(self):
        config = super().get_config()
        config.update({'model_name': self.model_name})
        return config

@register_keras_serializable(package="CustomLayers")
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

def triplet_loss(margin=0.5):
    """Triplet loss function"""
    def loss(y_true, y_pred):
        anchor, positive, negative = y_pred[:, 0, :], y_pred[:, 1, :], y_pred[:, 2, :]
        pos_dist = K.sum(K.square(anchor - positive), axis=-1)
        neg_dist = K.sum(K.square(anchor - negative), axis=-1)
        return K.mean(K.log(1 + K.exp(pos_dist - neg_dist + margin)))
    return loss

class SimilarityService:
    """End-to-end music similarity system with proper model loading"""
    def __init__(self):
        # Define custom objects for model loading
        self.custom_objects = {
            'AudioPreprocessLayer': AudioPreprocessLayer,
            'NormalizeEmbeddingLayer': NormalizeEmbeddingLayer,
            'StackEmbeddingsLayer': StackEmbeddingsLayer,
            'BertEmbeddingLayer': BertEmbeddingLayer,
            'TripletAccuracyMetric': TripletAccuracyMetric,
            'triplet_loss': triplet_loss(config.MARGIN)
        }

        # Load models
        self.audio_net = keras.models.load_model(
            config.AUDIO_MODEL_PATH,
            custom_objects=self.custom_objects
        )
        self.lyrics_net = keras.models.load_model(
            config.LYRICS_MODEL_PATH,
            custom_objects=self.custom_objects
        )
        self.embedding_model = keras.models.load_model(
            config.EMBEDDING_MODEL_PATH,
            custom_objects=self.custom_objects
        )

        # Load tokenizer and audio processor
        self.tokenizer = BertTokenizer.from_pretrained(config.TOKENIZER_PATH)
        self.audio_preprocessor = AudioPreprocessor()
        self.reference_embeddings = {}

    def add_reference_tracks(self, df):
        """Add reference tracks to the database"""
        print(f"Adding {len(df)} reference tracks...")
        for _, row in df.iterrows():
            self._add_track(row['filename'], row['mfcc'], row['lyrics'])

    def _add_track(self, track_id, mfcc, lyrics):
        """Add a single track to reference database"""
        tokens = self.tokenizer(
            lyrics,
            padding='max_length',
            truncation=True,
            max_length=config.MAX_SEQUENCE_LENGTH,
            return_tensors='tf'
        )

        embedding = self.embedding_model.predict(
            [np.array([mfcc]), tokens['input_ids'], tokens['attention_mask']],
            verbose=0
        )[0]

        self.reference_embeddings[track_id] = {
            'embedding': embedding,
            'lyrics': lyrics[:100] + '...' if len(lyrics) > 100 else lyrics
        }

    def get_song_embedding(self, audio_path, lyrics_text):
        """Process a new song for similarity search"""
        # Process audio
        mfcc = self.audio_preprocessor.process_audio(audio_path)
        if mfcc is None:
            return None

        # Process lyrics
        tokens = self.tokenizer(
            lyrics_text,
            padding='max_length',
            truncation=True,
            max_length=config.MAX_SEQUENCE_LENGTH,
            return_tensors='tf'
        )

        # Get embedding
        embedding = self.embedding_model.predict(
            [np.array([mfcc]), tokens['input_ids'], tokens['attention_mask']],
            verbose=0
        )[0]

        return embedding

    def find_similar_tracks(self, query_embedding, top_k=5):
        if not self.reference_embeddings:
            raise ValueError("No reference tracks in database")
        
        results = []
        for track_id, data in self.reference_embeddings.items():
            # Calculate angular distance instead of cosine similarity
            cosine_sim = np.dot(query_embedding, data['embedding'])
            angular_dist = np.arccos(np.clip(cosine_sim, -1, 1)) / np.pi
            similarity = 1 - angular_dist
            
            # Apply non-linear scaling
            similarity = np.power(similarity, 4)
            
            results.append({
                'track_id': track_id,
                'similarity': float(similarity),
                'is_match': similarity >= config.SIMILARITY_THRESHOLD,
                'lyrics_snippet': data['lyrics']
            })
        
        # Sort and return top_k
        sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
        
        # Apply relative scoring to top results
        if len(sorted_results) > 1:
            top_score = sorted_results[0]['similarity']
            for res in sorted_results[1:]:
                res['similarity'] = res['similarity'] * 0.9
        
        return sorted_results[:top_k]