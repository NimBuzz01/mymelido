import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from config import Config

class LyricsService:
    def __init__(self):
        self.config = Config()
        self.MIN_SILENCE_LEN = 500  # milliseconds
        self.SILENCE_THRESH = 14    # dB below average
        self.KEEP_SILENCE = 500
        self.recognizer = sr.Recognizer()
        self.chunks_dir = os.path.join(os.getcwd(), "audio_chunks")
        os.makedirs(self.chunks_dir, exist_ok=True)

    def _transcribe_audio_chunk(self, chunk_path):
        """Helper function to transcribe a single audio chunk"""
        try:
            with sr.AudioFile(chunk_path) as source:
                audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print(f"Could not understand audio in chunk {chunk_path}")
            return ""
        except sr.RequestError as e:
            print(f"API request failed for chunk {chunk_path}: {e}")
            return ""

    def _cleanup_chunks(self):
        """Remove temporary chunk files"""
        for filename in os.listdir(self.chunks_dir):
            file_path = os.path.join(self.chunks_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    def extract_lyrics(self, audio_path, use_chunks=True):
        """
        Extract lyrics from audio file
        :param audio_path: Path to audio file
        :param use_chunks: Whether to split audio into chunks for better recognition
        :return: Extracted lyrics text
        """
        try:
            if not use_chunks:
                # Simple single-file transcription
                return self._transcribe_audio_chunk(audio_path)
            
            # Load audio file
            audio = AudioSegment.from_file(audio_path)
            
            # Split audio on silence
            chunks = split_on_silence(
                audio,
                min_silence_len=self.MIN_SILENCE_LEN,  # 500ms
                silence_thresh=audio.dBFS - self.SILENCE_THRESH,  # -14dB
                keep_silence=self.KEEP_SILENCE  # 500ms
            )
            
            lyrics = []
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(self.chunks_dir, f"chunk_{i}.wav")
                chunk.export(chunk_path, format="wav")
                
                text = self._transcribe_audio_chunk(chunk_path)
                if text:
                    lyrics.append(text.capitalize())
            
            # Clean up chunk files
            self._cleanup_chunks()
            
            return ". ".join(lyrics) + ("." if lyrics else "")
            # return "The two of us alone together. Something's just not right"
            
        except Exception as e:
            print(f"Error processing audio file: {e}")
            self._cleanup_chunks()
            return ""