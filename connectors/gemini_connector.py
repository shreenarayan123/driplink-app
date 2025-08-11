import time
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def detect_language_gemini(audio_file_path: str):
    start_time = time.time()
    try:
        # Check if file exists
        if not Path(audio_file_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # Initialize the model
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Upload the audio file
        audio_file = genai.upload_file(audio_file_path)

        prompt = """
        Please analyze this audio file and detect the primary language being spoken.
        Return only the ISO 639-1 language code (e.g., 'en' for English, 'hi' for Hindi, 'es' for Spanish, etc.).
        If you cannot determine the language, return 'unknown'.
        """

        response = model.generate_content([prompt, audio_file])
        detected_lang = response.text.strip().lower()

        # Clean up the uploaded file
        genai.delete_file(audio_file.name)

        elapsed = time.time() - start_time

        # Estimate cost (Gemini 2.0 Flash)
        estimated_input_tokens = 1000  # Rough estimate for audio processing
        estimated_output_tokens = 10

        estimated_cost = (
            estimated_input_tokens * 0.0375 + estimated_output_tokens * 0.15
        ) / 1000000

        return {
            "provider": "Google Gemini",
            "language": detected_lang,
            "time_seconds": round(elapsed, 2),
            "estimated_cost": round(estimated_cost, 6),
            "tokens_used": {
                "input": estimated_input_tokens,
                "output": estimated_output_tokens,
            },
            "status": "success",
            "error_message": None,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "provider": "Google Gemini",
            "language": None,
            "time_seconds": round(elapsed, 2),
            "estimated_cost": 0,
            "tokens_used": {"input": 0, "output": 0},
            "status": "error",
            "error_message": str(e),
        }
