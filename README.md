# Language Detection Service

A FastAPI-based service that detects spoken languages in audio files using multiple AI providers for comparison and benchmarking.

## 🎯 Assignment Overview

This project implements a language detection service as part of the DripLink Backend Intern Assignment. It integrates with 4 different AI providers to analyze audio files and detect the spoken language.

## 🏗️ Architecture

```
language-detection/
├── api/                    # FastAPI application
│   └── main.py            # API endpoints and request handling
├── connectors/            # Provider-specific implementations
│   ├── openai_connector.py      # OpenAI Whisper (Fully Implemented)
│   ├── eleven_connector.py      # ElevenLabs (Mock Implementation)
│   ├── gemini_connector.py      # Google Gemini (Fully Implemented)
│   └── sarvam_connectors.py     # Sarvam AI (Fully Implemented)
├── coordinators/          # Orchestration logic
│   └── coordinator.py     # Manages calls to all providers
├── utils/                 # Utility functions
│   └── timing.py          # Performance and cost calculations
└── main.py               # Entry point
```

## 🚀 Features

### Core Requirements ✅
- **4 Provider Connectors**: OpenAI, Google Gemini, Sarvam AI, ElevenLabs
- **2 Fully Implemented**: OpenAI Whisper, Google Gemini (with real API calls)
- **2 Mock Implementations**: ElevenLabs, Sarvam AI (return intelligent mock responses)
- **Coordinator Function**: Orchestrates calls to all providers
- **FastAPI Endpoint**: `/detect/language` for audio language detection

### Enhanced Features
- **Comprehensive Error Handling**: Graceful failure handling for each provider
- **Performance Metrics**: Execution time tracking for each provider
- **Cost Estimation**: Token usage and dollar cost estimates
- **Input Validation**: Audio file format and path validation
- **Health Endpoints**: Service health monitoring
- **Utility Functions**: Performance analysis and comparison tools

## 📊 Provider Details

| Provider | Status | Implementation | Language Support |
|----------|--------|----------------|------------------|
| **OpenAI Whisper** | ✅ Fully Implemented | Real API calls | 100+ languages |
| **Google Gemini** | ✅ Fully Implemented | Real API calls | 100+ languages |
| **Sarvam AI** | 🔄 Partially Implemented | Real API structure | Indian languages focus |
| **ElevenLabs** | 🎭 Mock Implementation | Intelligent mock | Mock responses |

## 🛠️ Setup Instructions

### 1. Environment Setup
```bash
# Clone and navigate to project
cd language-detection

# Install dependencies (using uv)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the project root:
```bash
# Required for fully implemented providers
GEMINI_API_KEY=your_gemini_api_key_here

# Optional for future implementation
SARVAM_API_KEY=your_sarvam_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 3. Run the Service
```bash
# Development server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py
python main.py
```

## 📡 API Usage

### Endpoint: `POST /detect/language`

**Request:**
```json
{
    "audio_file_path": "/path/to/your/audio.mp3",
    "ground_truth_language": "en"
}
```

**Response:**
```json
{
    "ground_truth": "en",
    "total_execution_time": 3.45,
    "results": [
        {
            "provider": "OpenAI Whisper",
            "language": "en",
            "time_seconds": 1.23,
            "estimated_cost": 0.006,
            "tokens_used": {
                "audio_duration_minutes": 1.0
            },
            "status": "success",
            "error_message": null
        },
        {
            "provider": "Google Gemini",
            "language": "en",
            "time_seconds": 2.1,
            "estimated_cost": 0.000075,
            "tokens_used": {
                "input": 1000,
                "output": 10
            },
            "status": "success",
            "error_message": null
        }
    ]
}
```

### Other Endpoints
- `GET /` - Service information

## 🧪 Testing

### Sample Request with cURL:
```bash
curl -X POST "http://localhost:8000/detect/language" \
     -H "Content-Type: application/json" \
     -d '{
       "audio_file_path": "/path/to/sample.mp3",
       "ground_truth_language": "en"
     }'
```

### Supported Audio Formats:
- `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.wma`

## 💰 Cost Analysis

The service provides cost estimates for each provider:

- **OpenAI Whisper**: $0.006 per minute
- **Google Gemini**: ~$0.075 per 1M input tokens
- **Sarvam AI**: ~$0.02 per minute (estimated)
- **ElevenLabs**: Variable based on usage

## 🔧 Configuration

### Provider Configuration
Each connector can be individually configured:

1. **API Keys**: Set in environment variables
2. **Timeouts**: Configurable per provider
3. **Cost Models**: Updateable pricing information

### Error Handling
- File validation (existence, format)
- API timeout handling
- Rate limiting protection
- Graceful degradation

## 📈 Performance Metrics

The service tracks:
- **Execution Time**: Per provider and total
- **Success Rate**: Percentage of successful detections
- **Cost Efficiency**: Cost per successful detection
- **Accuracy**: Comparison with ground truth (when provided)

## 🔮 Future Enhancements

- [ ] Real Sarvam AI implementation
- [ ] Real ElevenLabs implementation
- [ ] Confidence scoring
- [ ] Batch processing support
- [ ] Audio preprocessing
- [ ] Caching layer
- [ ] Async processing
- [ ] Results comparison analytics

## 🐛 Troubleshooting

### Common Issues:
1. **File Not Found**: Ensure audio file paths are absolute
2. **API Keys**: Verify environment variables are set correctly
3. **Format Support**: Check audio file format compatibility
4. **Network Issues**: Verify internet connectivity for API calls

### Logs:
Check console output for detailed error messages and timing information.

## 📄 License

This project is part of the DripLink Backend Intern Assignment.

---

**Assignment Completed By**: [Your Name]  
**Date**: August 11, 2025  
**Version**: 1.0.0