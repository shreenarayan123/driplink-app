import time
import requests
import os
from pathlib import Path


def detect_language_sarvam(audio_file_path: str):
    start_time = time.time()
    try:
        # Check if file exists
        if not Path(audio_file_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        api_key = os.getenv("SARVAM_API_KEY")
        if not api_key:
            raise ValueError("SARVAM_API_KEY environment variable not set")

        # Sarvam AI API endpoint for language detection
        url = "https://api.sarvam.ai/speech-to-text"

        headers = {
            "api-subscription-key": api_key,
        }

        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            files = {
                "file": audio_file,
                "model": (None, "saaras:v1"),  # Sarvam's multilingual model
                "language_detection": (None, "true"),  # Enable language detection
            }

            response = requests.post(url, headers=headers, files=files, timeout=30)

        if response.status_code == 200:
            result = response.json()
            detected_lang = result.get("detected_language", "unknown")

            # Convert to ISO 639-1 if needed
            lang_mapping = {
                "hindi": "hi",
                "english": "en",
                "tamil": "ta",
                "telugu": "te",
                "bengali": "bn",
                "marathi": "mr",
                "gujarati": "gu",
                "kannada": "kn",
                "malayalam": "ml",
                "punjabi": "pa",
                "urdu": "ur",
            }
            detected_lang = lang_mapping.get(detected_lang.lower(), detected_lang)

        else:
            raise Exception(
                f"Sarvam API error: {response.status_code} - {response.text}"
            )

        elapsed = time.time() - start_time

        # Rough estimate: $0.02 per minute of audio
        estimated_duration_minutes = 1  # Assume 1 minute for estimation
        estimated_cost = estimated_duration_minutes * 0.02

        return {
            "provider": "Sarvam AI",
            "language": detected_lang,
            "time_seconds": round(elapsed, 2),
            "estimated_cost": round(estimated_cost, 4),
            "tokens_used": {"audio_duration_minutes": estimated_duration_minutes},
            "status": "success",
            "error_message": None,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "provider": "Sarvam AI",
            "language": None,
            "time_seconds": round(elapsed, 2),
            "estimated_cost": 0,
            "tokens_used": {"audio_duration_minutes": 0},
            "status": "error",
            "error_message": str(e),
        }
