import torch
import pickle
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.utils.logger import get_logger

logger = get_logger("intent_classifier")

class IntentClassifier:
    def __init__(self, model_path="models/voicebot_bert/voicebot_bert"):
        logger.info("Loading BERT intent classifier...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        with open(f"{model_path}/label_encoder.pkl", "rb") as f:
            self.le = pickle.load(f)
        logger.info("Model loaded successfully!")

    def predict(self, text: str) -> dict:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=64
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        confidence = probs.max().item()
        intent = self.le.inverse_transform([outputs.logits.argmax().item()])[0]
        logger.info(f"Intent: {intent}, Confidence: {confidence:.2f}")
        return {
            "intent": str(intent),
            "confidence": round(float(confidence), 2)
        }