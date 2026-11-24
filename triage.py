from huggingface_hub import InferenceClient
import re

# Initialize the client (you can get a free token from huggingface.co/settings/tokens)
client = InferenceClient(model="facebook/bart-large-mnli", token="YOUR_HF_TOKEN")

def analyze_scam_message(text):
    text_lower = text.lower()
    detected_flags = []
    
    # --- Layer 1: Fast Heuristic Rules (Your existing logic) ---
    pillars = {
        'Authority': [r'\bcbi\b', r'\bpolice\b', r'\bbank\b', r'\bofficer\b'],
        'Urgency': [r'\burgent\b', r'\barrest\b', r'\bblock\b', r'\bwarrant\b'],
        'Isolation': [r'\bdon\'t tell\b', r'\bsecret\b', r'\bconfidential\b'],
        'Extraction': [r'\botp\b', r'\btransfer\b', r'\bpayment\b', r'\brs\.?\b']
    }
    
    for pillar, patterns in pillars.items():
        if any(re.search(pattern, text_lower) for pattern in patterns):
            detected_flags.append(pillar)
    
    # --- Layer 2: AI-Powered Analysis via Hugging Face ---
    # Use zero-shot classification to see if the text matches a scam pattern
    candidate_labels = ["a scam or phishing attempt", "a legitimate message"]
    
    try:
        # The API call
        ai_result = client.zero_shot_classification(
            text, 
            candidate_labels=candidate_labels,
            hypothesis_template="This text is {}."
        )
        
        # Extract the top prediction
        top_prediction = ai_result['labels'][0]
        confidence = ai_result['scores'][0]
        
        is_scam = top_prediction == candidate_labels[0]
        
    except Exception as e:
        print(f"AI API Error: {e}")
        # Fallback if the API fails
        is_scam = len(detected_flags) >= 2
        confidence = 0.5

    # --- Combine Results for Final Verdict ---
    if is_scam and confidence > 0.7:
        risk_level = "Critical"
        explanation = "🚨 STOP. Our AI analysis indicates this message is highly likely a scam. It uses tactics matching known fraud patterns."
        color = "darkred"
    elif is_scam or len(detected_flags) >= 2:
        risk_level = "High"
        explanation = "Warning: This message shows suspicious signs and may be a scam."
        color = "red"
    elif len(detected_flags) == 1:
        risk_level = "Medium"
        explanation = "This message has some suspicious elements. Proceed with caution."
        color = "orange"
    else:
        risk_level = "Low"
        explanation = "We didn't find common scam patterns, but always stay cautious with unknown senders."
        color = "green"

    return {
        'score': int(confidence * 100) if is_scam else 100 - int(confidence * 100),
        'risk_level': risk_level,
        'explanation': explanation,
        'color': color,
        'detected_pillars': detected_flags
    }
