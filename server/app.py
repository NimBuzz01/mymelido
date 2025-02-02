from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import librosa
import nltk
from keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

# Load the saved model
print('Loading models...')
audio_model = load_model('audio_model.h5')
print('Audio model loaded')

# # Load the vectorizer (assuming you have saved it)
# vectorizer = CountVectorizer(tokenizer=tokenize_and_lemmatize, stop_words=nltk.corpus.stopwords.words('english'))

# # Function to preprocess audio
# def preprocess_audio(file_path, fixed_length=128):
#     y, sr = librosa.load(file_path, sr=16000)
#     y = librosa.util.normalize(y)  # Normalize audio signal
#     mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
#     mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)

#     # Pad or trim mel spectrogram
#     if mel_spect_db.shape[1] < fixed_length:
#         mel_spect_db = np.pad(mel_spect_db, ((0, 0), (0, fixed_length - mel_spect_db.shape[1])), mode='constant')
#     else:
#         mel_spect_db = mel_spect_db[:, :fixed_length]

#     return mel_spect_db

# # Tokenizer with lemmatization
# def tokenize_and_lemmatize(text):
#     lemmatizer = nltk.WordNetLemmatizer()
#     tokens = nltk.word_tokenize(text)
#     return [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha()]

# # Function to extract lyrics from audio
# def extract_lyrics(audio_path):
#     recognizer = sr.Recognizer()
#     audio = AudioSegment.from_file(audio_path)
#     audio.export("temp.wav", format="wav")  # Convert to WAV format

#     with sr.AudioFile("temp.wav") as source:
#         audio_data = recognizer.record(source)
#         try:
#             lyrics = recognizer.recognize_google(audio_data)  # Use Google Speech-to-Text
#             return lyrics
#         except sr.UnknownValueError:
#             return "Could not understand audio"
#         except sr.RequestError:
#             return "API unavailable"

@app.route('/api/predict', methods=['POST'])
def predict():
    # Get the uploaded file
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    # audio_file = request.files['audio']
    # audio_path = 'temp_audio.mp3'
    # audio_file.save(audio_path)

    # # Extract lyrics from the uploaded audio
    # lyrics = extract_lyrics(audio_path)
    # if "Could not understand audio" in lyrics or "API unavailable" in lyrics:
    #     return jsonify({"error": lyrics}), 400

    # # Preprocess the audio
    # audio_features = preprocess_audio(audio_path)
    # audio_features = np.expand_dims(audio_features, axis=-1)
    # audio_features = audio_features.flatten().reshape(1, -1)

    # # Predict using the audio model
    # audio_similarity = audio_model.predict(audio_features)

    # # Preprocess the lyrics
    # lyrics_vector = vectorizer.transform([lyrics])
    # lyrics_similarity = cosine_similarity(lyrics_vector, vectorizer.transform([lyrics]))

    # # Combine results (simple average for overall similarity)
    # overall_similarity = (audio_similarity[0][0] + lyrics_similarity[0][0]) / 2 * 100

    # # Get top 5 similar songs for audio and lyrics
    # audio_similarities = cosine_similarity(audio_features, X_audio.reshape(X_audio.shape[0], -1))
    # lyrics_similarities = cosine_similarity(lyrics_vector, lyrics_tfidf)

    # top_5_audio_indices = audio_similarities.argsort()[0][-5:][::-1]
    # top_5_lyrics_indices = lyrics_similarities.argsort()[0][-5:][::-1]

    # top_5_audio = [(list(audio_features.keys())[i], audio_similarities[0][i] * 100) for i in top_5_audio_indices]
    # top_5_lyrics = [(os.listdir(lyrics_folder)[i], lyrics_similarities[0][i] * 100) for i in top_5_lyrics_indices]

    # Return the results
    return jsonify({
    "most_potential_copyrighted_lyrics": {
        "song": "Blue Jeans",
        "overall_similarity": 100,
        "lyrics_similarity": 90,
        "copyright_status": "Potential Lyrical Infringement"
    },
    "most_potential_copyrighted_audio": {
        "song": "Twinkle Twinkle Little Star",
        "overall_similarity": 60,
        "audio_similarity": 70,
        "copyright_status": "Potential Audio Infringement"
    },
    "top_5_similar_songs_based_on_lyrics": [
        { "song": "Shape of You", "similarity": 92 },
        { "song": "Perfect", "similarity": 85 },
        { "song": "Thinking Out Loud", "similarity": 80 },
        { "song": "Castle on the Hill", "similarity": 78 },
        { "song": "Galway Girl", "similarity": 75 }
    ],
    "top_5_similar_songs_based_on_audio": [
        { "song": "Shape of You", "similarity": 92 },
        { "song": "Perfect", "similarity": 85 },
        { "song": "Thinking Out Loud", "similarity": 80 },
        { "song": "Castle on the Hill", "similarity": 78 },
        { "song": "Galway Girl", "similarity": 75 }
    ]
    })

if __name__ == '__main__':
    app.run(debug=True)