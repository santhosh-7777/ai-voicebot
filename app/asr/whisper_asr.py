import whisper
import os
from app.utils.logger import get_logger

logger = get_logger("whisper_asr")

class WhisperASR:
    def __init__(self, model_size="base"):
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        logger.info("Whisper model loaded successfully!")

    def transcribe(self, audio_path: str) -> dict:
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return {"error": "Audio file not found"}

        logger.info(f"Transcribing: {audio_path}")
        result = self.model.transcribe(audio_path)
        transcript = result["text"].strip()
        logger.info(f"Transcript: {transcript}")

        return {"transcript": transcript}