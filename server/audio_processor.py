import librosa
import numpy as np
from config import Config

config = Config()

class AudioPreprocessor:
    def __init__(self):
        self.sample_rate = config.SAMPLE_RATE
        self.n_mfcc = config.N_MFCC
        self.hop_length = config.HOP_LENGTH
        self.n_fft = config.N_FFT

    def process_audio(self, filepath, duration=30):
        """Process a single audio file"""
        try:
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sample_rate, duration=duration)

            # Extract MFCCs
            mfcc = librosa.feature.mfcc(
                y=y,
                sr=sr,
                n_mfcc=self.n_mfcc,
                hop_length=self.hop_length,
                n_fft=self.n_fft
            )

            # Flatten and pad
            mfcc_flat = mfcc.flatten()
            if len(mfcc_flat) > config.AUDIO_INPUT_SHAPE:
                mfcc_flat = mfcc_flat[:config.AUDIO_INPUT_SHAPE]
            else:
                mfcc_flat = np.pad(
                    mfcc_flat,
                    (0, config.AUDIO_INPUT_SHAPE - len(mfcc_flat)),
                    'constant'
                )

            # Normalize
            mfcc_flat = (mfcc_flat - np.mean(mfcc_flat)) / (np.std(mfcc_flat) + 1e-8)
            return np.clip(mfcc_flat, -3, 3)
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            return None