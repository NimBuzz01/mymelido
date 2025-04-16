from flask import Flask, request, jsonify
from audio_service import AudioService
from lyrics_service import LyricsService
from similarity_service import SimilarityService
from file_handlers import FileHandler
from utils import load_and_preprocess_data
from config import Config
from flask_cors import CORS
import os
import tensorflow as tf

app = Flask(__name__)
CORS(app)

config = Config()

# Initialize services
file_handler = FileHandler()
audio_service = AudioService()
lyrics_service = LyricsService()
similarity_service = SimilarityService()

df = load_and_preprocess_data(f"{config.DATA_DIR}/LAG.pkl")
similarity_service.add_reference_tracks(df)

@app.route('/api/analyze', methods=['POST'])
def check_similarity():
    """Endpoint for checking song similarity"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    if not file_handler.is_allowed_file(audio_file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    temp_path = file_handler.save_temp_file(audio_file)
    if not temp_path:
        return jsonify({'error': 'File upload failed'}), 500
    
    try:
        # Process audio
        mfcc = audio_service.process_audio_file(temp_path)       
        # Extract lyrics
        lyrics = lyrics_service.extract_lyrics(temp_path)
        
        # Get embedding
        embedding = similarity_service.get_embedding(mfcc, lyrics)
        print(f"Embedding shape: {embedding.shape}")
        
        # Find similar tracks
        similar_tracks = similarity_service.find_similar_tracks(embedding)
        print(f"Similar tracks found: {similar_tracks}")
        
        # Prepare response
        response = {
            'status': 'success',
            'input_metadata': {
                'filename': audio_file.filename,
                'lyrics_snippet': lyrics[:100] + '...' if len(lyrics) > 100 else lyrics
            },
            'matches': similar_tracks
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        file_handler.cleanup_file(temp_path)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)