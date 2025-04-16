import numpy as np
from transformers import BertTokenizer
import keras
from config import Config
from custom_layers import (
    AudioPreprocessLayer,
    NormalizeEmbeddingLayer, StackEmbeddingsLayer,
    BertEmbeddingLayer, TripletAccuracyMetric, triplet_loss)
import os
import pandas as pd

class SimilarityService:
    def __init__(self):
        self.config = Config()
        self.tokenizer = BertTokenizer.from_pretrained(self.config.TOKENIZER_DIR)
        
        # Register custom objects
        self.custom_objects = {
            'AudioPreprocessLayer': AudioPreprocessLayer,
            'NormalizeEmbeddingLayer': NormalizeEmbeddingLayer,
            'StackEmbeddingsLayer': StackEmbeddingsLayer,
            'BertEmbeddingLayer': BertEmbeddingLayer,
            'TripletAccuracyMetric': TripletAccuracyMetric,
            'triplet_loss': triplet_loss(self.config.MARGIN)
        }

        # Initialize models
        self.audio_model = None
        self.lyrics_model = None 
        self.embedding_model = None
        
        self._load_models()
        self.reference_embeddings = {}

    def _load_models(self):
        """Safely load all models with error handling"""
        try:
            # Verify model files exist
            for model_file in ['audio_model.keras', 'lyrics_model.keras', 'music_similarity_model.keras']:
                if not os.path.exists(f"{self.config.MODEL_DIR}/{model_file}"):
                    raise FileNotFoundError(f"Model file not found: {model_file}")
            
            # Load models
            self.audio_model = keras.models.load_model(
                f"{self.config.MODEL_DIR}/audio_model.keras",
                custom_objects=self.custom_objects
            )
            
            self.lyrics_model = keras.models.load_model(
                f"{self.config.MODEL_DIR}/lyrics_model.keras",
                custom_objects=self.custom_objects
            )
            
            self.embedding_model = keras.models.load_model(
                f"{self.config.MODEL_DIR}/music_similarity_model.keras",
                custom_objects=self.custom_objects
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to load models: {str(e)}")

    def add_reference_tracks(self, df, batch_size=32):
        """Add reference tracks in batches for efficiency"""
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
            
        # Process in batches
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            self._process_batch(batch)

    def _process_batch(self, batch_df):
        """Process a batch of tracks"""
        try:
            # Prepare batch inputs
            mfccs = np.array(batch_df['mfcc'].tolist())
            
            # Tokenize lyrics
            lyrics_texts = batch_df['lyrics'].tolist()
            tokens = self.tokenizer(
                lyrics_texts,
                padding='max_length',
                truncation=True,
                max_length=self.config.MAX_SEQUENCE_LENGTH,
                return_tensors='tf'
            )
            
            # Get embeddings
            embeddings = self.embedding_model.predict(
                [mfccs, tokens['input_ids'], tokens['attention_mask']],
                verbose=0
            )
            
            # Store results
            for idx, (_, row) in enumerate(batch_df.iterrows()):
                self.reference_embeddings[row['filename']] = {
                    'embedding': embeddings[idx],
                    'lyrics': row['lyrics'][:100] + '...' if len(row['lyrics']) > 100 else row['lyrics'],
                    'metadata': {
                        'artist': row.get('artist', ''),
                        'title': row.get('title', '')
                    }
                }
                
        except Exception as e:
            print(f"Error processing batch: {e}")

    def get_embedding(self, mfcc, lyrics):
        """Get embedding for new track with validation"""
        if not isinstance(mfcc, np.ndarray) or mfcc.shape != (self.config.AUDIO_INPUT_SHAPE,):
            raise ValueError(f"MFCC must be numpy array with shape ({self.config.AUDIO_INPUT_SHAPE},)")
            
        try:
            # Process lyrics
            tokens = self.tokenizer(
                lyrics,
                padding='max_length',
                truncation=True,
                max_length=self.config.MAX_SEQUENCE_LENGTH,
                return_tensors='tf'
            )
            
            # Get embedding
            embedding = self.embedding_model.predict(
                [np.array([mfcc]), tokens['input_ids'], tokens['attention_mask']],
                verbose=0
            )
            
            return embedding[0]  # Return first (and only) embedding
            
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def find_similar_tracks(self, query_embedding, top_k=5, threshold=None):
        """Find similar tracks with improved similarity calculation"""
        if query_embedding is None:
            return []
            
        threshold = threshold or self.config.SIMILARITY_THRESHOLD
        results = []
        
        for track_id, data in self.reference_embeddings.items():
            try:
                # Normalized dot product similarity
                norm_query = query_embedding / np.linalg.norm(query_embedding)
                norm_ref = data['embedding'] / np.linalg.norm(data['embedding'])
                cosine_sim = np.dot(norm_query, norm_ref)
                angular_sim = 1 - (np.arccos(np.clip(cosine_sim, -1, 1)) / np.pi)

                normalized = np.clip((angular_sim - 0.7) / 0.3, 0, 1)
                similarity = np.power(normalized, 4)
                
                results.append({
                    'track_id': track_id,
                    'similarity': float(similarity),
                    'is_match': similarity >= threshold,
                    'metadata': data.get('metadata', {})
                })
            except Exception as e:
                print(f"Error comparing with {track_id}: {e}")
                continue
                
        return sorted(results, key=lambda x: x['similarity'], reverse=True)[:top_k]