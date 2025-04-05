import time
from flask import Flask, request, jsonify
from flask_cors import CORS
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
        "query_track": "out_Sedative_God_Paradise_Lost_1_2",
        "genre": "metal",
        "lyrics": "To feel constrained is always there for me...",
        "top_matches": [
            {
                "track_id": "out_Sedative_God_Paradise_Lost_1_2",
                "similarity": 1.0000,
                "match": "YES",
                "lyrics": "To feel constrained is always there for me"
            },
            {
                "track_id": "out_Where_the_Light_has_Failed_Skeletonwitch_2_2",
                "similarity": 0.6851,
                "match": "NO",
                "lyrics": "Where the light has failed, darkness now prevails"
            },
            {
                "track_id": "out_Space_Beer_Tankard_2_2",
                "similarity": 0.4778,
                "match": "NO",
                "lyrics": "A drink of healing cures your ills. A new idea - great innovation"
            },
            {
                "track_id": "out_Let_It_Burn_Tygers_Of_Pan_Tang_0_2",
                "similarity": 0.5774,
                "match": "NO",
                "lyrics": ""
            },
            {
                "track_id": "out_We_Gave_It_Hell_36_Crazyfists_2_2",
                "similarity": 0.8584,
                "match": "YES",
                "lyrics": "Ones of reminder and things that just won't heal and in time we will"
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)