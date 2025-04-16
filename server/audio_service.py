import librosa
import numpy as np
from config import Config

class AudioService:
    def __init__(self):
        self.config = Config()
    
    def process_audio_file(self, file_path):
        """Process audio file into MFCC features"""
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=self.config.SAMPLE_RATE)
            
            # Extract MFCCs
            mfcc = librosa.feature.mfcc(
                y=y,
                sr=sr,
                n_mfcc=self.config.N_MFCC,
                hop_length=self.config.HOP_LENGTH,
                n_fft=self.config.N_FFT
            )
            
            # Flatten and pad
            mfcc_flat = mfcc.flatten()
            if len(mfcc_flat) > self.config.AUDIO_INPUT_SHAPE:
                mfcc_flat = mfcc_flat[:self.config.AUDIO_INPUT_SHAPE]
            else:
                mfcc_flat = np.pad(
                    mfcc_flat,
                    (0, self.config.AUDIO_INPUT_SHAPE - len(mfcc_flat)),
                    'constant'
                )
            
            # Normalize
            mfcc_flat = (mfcc_flat - np.mean(mfcc_flat)) / (np.std(mfcc_flat) + 1e-8)
            return np.clip(mfcc_flat, -3, 3)
        
        except Exception as e:
            print(f"Audio processing error: {str(e)}")
            raise