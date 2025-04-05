import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
import keras

keras.config.enable_unsafe_deserialization()

app = Flask(__name__)
CORS(app)

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    # Add a 2-second delay to simulate processing
    time.sleep(2)

    # Return the dummy results with delay
    return jsonify({
        "Query Track": "out_Sedative_God_Paradise_Lost_1_2",
        "Genre": "metal",
        "Lyrics": "To feel constrained is always there for me...",
        "Top Matches": [
            {
                "Track ID": "out_Sedative_God_Paradise_Lost_1_2",
                "Similarity": 1.0000,
                "Match": "YES",
                "Lyrics": "To feel constrained is always there for me"
            },
            {
                "Track ID": "out_Where_the_Light_has_Failed_Skeletonwitch_2_2",
                "Similarity": 0.9851,
                "Match": "YES",
                "Lyrics": "Where the light has failed, darkness now prevails"
            },
            {
                "Track ID": "out_Space_Beer_Tankard_2_2",
                "Similarity": 0.9778,
                "Match": "YES",
                "Lyrics": "A drink of healing cures your ills. A new idea - great innovation"
            },
            {
                "Track ID": "out_Let_It_Burn_Tygers_Of_Pan_Tang_0_2",
                "Similarity": 0.9774,
                "Match": "YES",
                "Lyrics": ""
            },
            {
                "Track ID": "out_We_Gave_It_Hell_36_Crazyfists_2_2",
                "Similarity": 0.9584,
                "Match": "YES",
                "Lyrics": "Ones of reminder and things that just won't heal and in time we will"
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)