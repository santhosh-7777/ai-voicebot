from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.asr.whisper_asr import WhisperASR
from app.nlp.intent_classifier import IntentClassifier
from app.nlp.response_generator import generate_response
from app.tts.tts_engine import TTSEngine
from app.utils.logger import get_logger
import shutil, os

logger = get_logger("main")
app = FastAPI(title="Voice Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

asr = WhisperASR()
clf = IntentClassifier()
tts = TTSEngine()

@app.get("/")
def root():
    return {"message": "Voice Bot API is running!"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    path = f"tests/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    result = asr.transcribe(path)
    return result

@app.post("/predict-intent")
def predict_intent(data: dict):
    text = data.get("text", "")
    return clf.predict(text)

@app.post("/generate-response")
def get_response(data: dict):
    intent = data.get("intent", "")
    confidence = data.get("confidence", 0.0)
    return generate_response(intent, confidence)

@app.post("/synthesize")
def synthesize(data: dict):
    text = data.get("text", "")
    result = tts.synthesize(text)
    if result.get("audio_path"):
        return FileResponse(result["audio_path"], media_type="audio/mpeg")
    return {"error": "TTS failed - check internet connection"}

@app.post("/voicebot")
async def voicebot(file: UploadFile = File(...)):
    path = f"tests/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    transcript = asr.transcribe(path)
    text = transcript.get("transcript", "")
    intent_result = clf.predict(text)
    response = generate_response(intent_result["intent"], intent_result["confidence"])
    audio = tts.synthesize(response["response"])
    return {
        "transcript": text,
        "intent": intent_result["intent"],
        "confidence": intent_result["confidence"],
        "response": response["response"],
        "audio_path": audio.get("audio_path"),
        "tts_status": "success" if audio.get("audio_path") else "failed - no internet"
    }