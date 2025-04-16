class Config:
    # Audio Processing
    AUDIO_INPUT_SHAPE = 54656
    SAMPLE_RATE = 22050
    N_MFCC = 16
    HOP_LENGTH = 512
    N_FFT = 16
    MARGIN = 0.5
    
    # Model Config
    MAX_SEQUENCE_LENGTH = 64
    EMBEDDING_DIM = 128
    SIMILARITY_THRESHOLD = 0.7
    BERT_MODEL_NAME = 'bert-base-uncased'
    
    # File Uploads
    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Paths
    MODEL_DIR = 'models'
    TOKENIZER_DIR = 'models/bert_tokenizer'
    DATA_DIR = 'data'
