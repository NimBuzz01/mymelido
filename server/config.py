class Config:
    # Audio configuration
    AUDIO_INPUT_SHAPE = 54656
    TARGET_AUDIO_SHAPE = 55296
    SAMPLE_RATE = 22050
    N_MFCC = 2048
    HOP_LENGTH = 512
    N_FFT = 2048
    MARGIN = 0.3
    
    # Lyrics processing
    MAX_SEQUENCE_LENGTH = 64
    SIMILARITY_THRESHOLD = 0.8

    DATA_PATH = "data/LAG.pkl"
    
    # Model paths
    MODEL_DIR = "models/"
    AUDIO_MODEL_PATH = MODEL_DIR + "audio_model.keras"
    LYRICS_MODEL_PATH = MODEL_DIR + "lyrics_model.keras"
    EMBEDDING_MODEL_PATH = MODEL_DIR + "music_similarity_model.keras"
    TOKENIZER_PATH = MODEL_DIR + "bert_tokenizer"
    
    # API settings
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = '/tmp'