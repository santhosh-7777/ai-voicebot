import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class Config:
    WHISPER_MODEL_SIZE     = "base"
    MAX_AUDIO_DURATION_SEC = 30
    SUPPORTED_FORMATS      = {".wav", ".mp3", ".m4a"}
    BERT_BASE_MODEL        = "bert-base-uncased"
    MODEL_SAVE_PATH        = os.path.join(BASE_DIR, "models", "intent_model")
    MAX_SEQ_LENGTH         = 128
    NUM_LABELS             = 11
    CONFIDENCE_THRESHOLD   = 0.60
    TTS_LANGUAGE           = "en"
    TTS_OUTPUT_DIR         = os.path.join(BASE_DIR, "outputs")
    API_HOST               = "0.0.0.0"
    API_PORT               = 8000