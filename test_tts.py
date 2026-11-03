import os
import sys
import base64
from dotenv import load_dotenv

# Ensure Windows SSL certificate store is trusted
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

# Ensure UTF-8 output for Indian language text in Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from sarvamai import SarvamAI

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    raise ValueError("SARVAM_API_KEY environment variable is not set")

# Initialize client using environment variable
client = SarvamAI(api_subscription_key=api_key)

# Make first call to Sarvam Text-to-Speech API
text_input = "नमस्ते! मैं बोलो बडी हूँ। आज हम मिलकर पढ़ेंगे।"
print(f"Synthesizing text: '{text_input}'...")

response = client.text_to_speech.convert(
    text=text_input,
    language_code="hi-IN",
    model="bulbul:v3"
)

# Save the generated audio to a file
output_file = "output.wav"
if response.audios and len(response.audios) > 0:
    audio_bytes = base64.b64decode(response.audios[0])
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    print(f"Success! Audio saved to: {output_file} ({len(audio_bytes)} bytes)")
    print(f"Request ID: {response.request_id}")
else:
    print("No audio received in response.")
