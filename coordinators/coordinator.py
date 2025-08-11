from connectors.openai_connector import detect_language_openai
from connectors.eleven_connector import detect_language_elevenlabs
from connectors.gemini_connector import detect_language_gemini
from connectors.sarvam_connectors import detect_language_sarvam
from utils.timing import (
    calculate_cost_metrics,
    get_fastest_provider,
    get_cheapest_provider,
)
import time


def run_all_providers(audio_file_path: str):
    """
    Orchestrates language detection across all providers.

    Args:
        audio_file_path (str): Path to the audio file to analyze

    Returns:
        list: Results from all providers with timing and cost information
    """
    results = []
    start_time = time.time()

    # List of all provider functions
    providers = [
        detect_language_openai,
        detect_language_gemini,
        detect_language_sarvam,
        detect_language_elevenlabs,
    ]

    # Execute each provider
    for provider_func in providers:
        try:
            result = provider_func(audio_file_path)
            results.append(result)
        except Exception as e:
            # Fallback error result if provider function fails completely
            results.append(
                {
                    "provider": provider_func.__name__.replace(
                        "detect_language_", ""
                    ).title(),
                    "language": None,
                    "time_seconds": 0,
                    "estimated_cost": 0,
                    "tokens_used": {},
                    "status": "critical_error",
                    "error_message": f"Provider function failed: {str(e)}",
                }
            )

    total_time = time.time() - start_time

    summary = {
        "total_execution_time": round(total_time, 2),
        "metrics": calculate_cost_metrics(results),
        "fastest_provider": get_fastest_provider(results),
        "cheapest_provider": get_cheapest_provider(results),
    }

    results.append(
        {"provider": "SUMMARY", "summary_metrics": summary, "status": "info"}
    )

    return results


def run_single_provider(provider_name: str, audio_file_path: str):
    """
    Run a single provider by name.

    Args:
        provider_name (str): Name of the provider ('openai', 'gemini', 'sarvam', 'elevenlabs')
        audio_file_path (str): Path to the audio file

    Returns:
        dict: Result from the specified provider
    """
    provider_map = {
        "openai": detect_language_openai,
        "gemini": detect_language_gemini,
        "sarvam": detect_language_sarvam,
        "elevenlabs": detect_language_elevenlabs,
    }

    provider_func = provider_map.get(provider_name.lower())
    if not provider_func:
        return {
            "provider": provider_name,
            "language": None,
            "time_seconds": 0,
            "estimated_cost": 0,
            "status": "error",
            "error_message": f"Unknown provider: {provider_name}",
        }

    return provider_func(audio_file_path)
