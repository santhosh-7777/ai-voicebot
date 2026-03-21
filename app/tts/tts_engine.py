import os
from gtts import gTTS
from app.utils.logger import get_logger

logger = get_logger("tts_engine")

class TTSEngine:
    def __init__(self, language="en", output_dir="outputs"):
        self.language = language
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def synthesize(self, text: str, filename: str = "response.mp3") -> dict:
        if not text or len(text.strip()) == 0:
            logger.error("Empty text received")
            return {"error": "Text cannot be empty", "audio_path": None}

        output_path = os.path.join(self.output_dir, filename)
        logger.info(f"Synthesizing: {text[:50]}...")

        try:
            tts = gTTS(text=text, lang=self.language)
            tts.save(output_path)
            logger.info(f"Audio saved to {output_path}")
            return {"audio_path": output_path}
        except Exception as e:
            logger.warning(f"TTS failed (no internet?): {e}")
            return {"audio_path": None, "tts_error": "Audio unavailable - check internet"}