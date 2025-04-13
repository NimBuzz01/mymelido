from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio_processor import AudioPreprocessor
from utils import load_and_preprocess_data
from similarity_service import SimilarityService
from config import Config
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# audio_preprocessor = AudioPreprocessor()
# similarity_service = SimilarityService()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/analyze', methods=['POST'])
def analyze_song():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    lyrics_text = request.form.get('lyrics', '')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400
    
    if not allowed_file(audio_file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # # Save temporarily
        # filename = secure_filename(audio_file.filename)
        # temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # audio_file.save(temp_path)
        
        # # Process audio
        # audio_features = audio_preprocessor.process_audio(temp_path)
        
        # # Get embedding
        # query_embedding = similarity_service.get_song_embedding(audio_features, lyrics_text)
        
        # # Find similar tracks
        # matches = similarity_service.find_similar_tracks(query_embedding)
        
        # # Clean up
        # os.remove(temp_path)
        
        # return jsonify({
        #     'status': 'success',
        #     'results': matches
        # })

        sleep(3)
    
        return jsonify({
        "status": "success",
        "results": [
            {
            "track_id": "out_No_One_Else_Comes_Close_Backstreet_Boys_0_2",
            "similarity": 0.9644,
            "is_match": True,
            "lyrics_snippet": "The two of us alone together. Something's just not right"
            },
            {
            "track_id": "out_Out_Of_Sight_John_Legend_2_2",
            "similarity": 0.7597,
            "is_match": False,
            "lyrics_snippet": "right right We'll do it right right Ain't too fast or slow, it's just enough to get down. Might be f..."
            },
            {
            "track_id": "out_Imagine_Declan_Galbraith_0_2",
            "similarity": 0.5423,
            "is_match": False,
            "lyrics_snippet": "It's easy if you try."
            },
            {
            "track_id": "out_Heart_Association_The_Emotions_1_2",
            "similarity": 0.7395,
            "is_match": False,
            "lyrics_snippet": "I started just to fall 'way and the sound of your voice said 'Don't go away'"
            },
            {
            "track_id": "out_Ricky_Weird_Al_Yankovic_1_2",
            "similarity": 0.7381,
            "is_match": False,
            "lyrics_snippet": "Hey Ricky You always play your conga drums, you think you got the right. You wake up little Ricky in..."
            }
        ]
        })  
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Load your reference tracks here
    # df = load_and_preprocess_data(app.config['DATA_PATH'])
    # similarity_service.add_reference_tracks(df)
    
    app.run(host='0.0.0.0', port=5000, debug=True)