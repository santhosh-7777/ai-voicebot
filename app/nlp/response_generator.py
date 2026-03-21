from app.utils.logger import get_logger

logger = get_logger("response_generator")

RESPONSES = {
    "track_order": "Your order is currently being tracked. Please share your order ID and I will get the latest status for you.",
    "cancel_order": "I can help you cancel your order. Please provide your order ID and I will process the cancellation immediately.",
    "refund_request": "I understand you want a refund. Please share your order ID and reason. Refunds are processed within 5-7 business days.",
    "complaint": "I am really sorry to hear that! Your complaint has been registered. Our team will contact you within 24 hours.",
    "business_hours": "Our customer support is available Monday to Saturday from 9 AM to 6 PM IST. We are closed on Sundays.",
    "payment_help": "We accept UPI, Credit Card, Debit Card, Net Banking and Cash on Delivery. Please let me know your specific payment issue.",
    "return_product": "You can return products within 7 days of delivery. I will help you schedule a pickup. Please share your order ID.",
    "human_agent": "Sure! Let me connect you to a live agent. Please wait for 2-3 minutes. Our agent will assist you shortly.",
    "product_inquiry": "We have a wide range of products. Please visit our website or tell me what category you are looking for.",
    "account_issue": "I can help with your account issue. Please verify your registered email or phone number to proceed.",
    "greeting": "Hello! Welcome to customer support. How can I help you today?",
    "farewell": "Thank you for contacting us. Have a wonderful day! Feel free to reach out anytime."
}

FALLBACK = "I am sorry, I did not understand that. Could you please rephrase your question?"

def generate_response(intent: str, confidence: float) -> dict:
    if confidence < 0.30:
        logger.warning(f"Low confidence: {confidence}")
        return {"response": FALLBACK, "intent": "unknown"}
    
    response = RESPONSES.get(intent, FALLBACK)
    logger.info(f"Response generated for intent: {intent}")
    return {"response": response, "intent": intent}