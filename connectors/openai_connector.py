import time
import whisper
import os
from pathlib import Path

model = None


def get_whisper_model():
    """Load Whisper model lazily"""
    global model
    if model is None:
        # Use base model - confirmed working
        model = whisper.load_model("base")
    return model


def detect_language_openai(audio_file_path: str):
    start_time = time.time()
    try:
        # Check if file exists
        if not Path(audio_file_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # Get the Whisper model
        whisper_model = get_whisper_model()

        # Load and process audio file
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio, n_mels=whisper_model.dims.n_mels).to(
            whisper_model.device
        )

        # Detect the spoken language
        _, probs = whisper_model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)
        confidence = probs[detected_lang]

        elapsed = time.time() - start_time

        # Estimate audio duration (rough calculation based on array length)
        audio_duration_seconds = len(audio) / whisper.audio.SAMPLE_RATE
        audio_duration_minutes = audio_duration_seconds / 60

        # Local Whisper is free, but estimate equivalent API cost for comparison
        estimated_cost = audio_duration_minutes * 0.006  # OpenAI API pricing

        return {
            "provider": "OpenAI Whisper (Local)",
            "language": detected_lang,
            "confidence": round(confidence, 3),
            "time_seconds": round(elapsed, 2),
            "estimated_cost": round(estimated_cost, 4),
            "tokens_used": {
                "audio_duration_minutes": round(audio_duration_minutes, 2),
                "audio_duration_seconds": round(audio_duration_seconds, 1),
            },
            "status": "success",
            "error_message": None,
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "provider": "OpenAI Whisper (Local)",
            "language": None,
            "confidence": 0.0,
            "time_seconds": round(elapsed, 2),
            "estimated_cost": 0,
            "tokens_used": {"audio_duration_minutes": 0, "audio_duration_seconds": 0},
            "status": "error",
            "error_message": str(e),
        }
