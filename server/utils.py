import pandas as pd
import pickle
import numpy as np
from config import Config

config = Config()

def load_and_preprocess_data(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)

    df = pd.DataFrame(data, columns=['filename', 'lyrics', 'mfcc', 'genre', 'genre_idx'])

    # Validate samples (keep only checks for MFCC/text validity)
    valid_samples = []
    for idx, row in df.iterrows():
        try:
            if (len(row['mfcc']) == config.AUDIO_INPUT_SHAPE and
                not np.isnan(row['mfcc']).any() and
                len(row['lyrics']) > 10):
                valid_samples.append(idx)
        except:
            continue

    df = df.iloc[valid_samples].copy()

    # Normalize MFCCs
    def normalize_mfcc(x):
        x = np.array(x)
        mean = np.mean(x)
        std = np.std(x)
        x = (x - mean) / (std + 1e-8)
        return np.clip(x, -3, 3)

    df['mfcc'] = df['mfcc'].apply(normalize_mfcc)

    # Clean lyrics
    df['lyrics'] = df['lyrics'].fillna('').astype(str).str.strip()
    df['lyrics'] = df['lyrics'].str.replace(r'\s+', ' ', regex=True)

    print(f"Loaded {len(df)} valid samples")
    return df