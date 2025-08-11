from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from coordinators.coordinator import run_all_providers
import time

app = FastAPI(
    title="Language Detection Service",
    description="A service that detects spoken language in audio files using multiple AI providers",
    version="1.0.0",
)


class DetectRequest(BaseModel):
    audio_file_path: str = Field(..., description="Path to the audio file to analyze")
    ground_truth_language: str = Field(
        ...,
        description="Expected language code for comparison (e.g., 'en', 'hi', 'es')",
    )


class DetectResponse(BaseModel):
    ground_truth: str
    total_execution_time: float
    results: list


@app.get("/")
def read_root():
    return {
        "message": "Language Detection Service",
        "version": "1.0.0",
        "endpoints": {
            "detect": "/detect/language (POST)",
            "test_files": "/test-files (GET)",
            "docs": "/docs (GET)",
        },
    }


@app.get("/test-files")
def list_test_files():
    """List available test audio files"""
    test_files_dir = Path(__file__).parent.parent / "test_files"

    if not test_files_dir.exists():
        return {"test_files": [], "message": "No test_files directory found"}

    audio_files = []
    for file_path in test_files_dir.glob("*.mp3"):
        audio_files.append(
            {
                "filename": file_path.name,
                "path": str(file_path),
                "size_mb": round(file_path.stat().st_size / (1024 * 1024), 2),
            }
        )

    return {
        "test_files": audio_files,
        "count": len(audio_files),
        "directory": str(test_files_dir),
    }


@app.post("/detect/language", response_model=DetectResponse)
def detect_language(req: DetectRequest):
    """
    Detect the spoken language in an audio file using multiple AI providers.

    - **audio_file_path**: Path to the audio file (supports common formats like .mp3, .wav, .m4a)
    - **ground_truth_language**: Expected language code for comparison purposes

    Returns results from all configured providers with timing and cost information.
    """
    start_time = time.time()

    # Validate audio file exists
    if not Path(req.audio_file_path).exists():
        raise HTTPException(
            status_code=404, detail=f"Audio file not found: {req.audio_file_path}"
        )

    # Validate file extension
    valid_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma"}
    file_extension = Path(req.audio_file_path).suffix.lower()
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {file_extension}. Supported formats: {', '.join(valid_extensions)}",
        )

    try:
        # Run all providers
        results = run_all_providers(req.audio_file_path)
        total_time = time.time() - start_time

        return {
            "ground_truth": req.ground_truth_language,
            "total_execution_time": round(total_time, 2),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
