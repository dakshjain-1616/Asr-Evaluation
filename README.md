# ASR Evaluation Framework

A comprehensive benchmarking framework for evaluating automatic speech recognition (ASR) models across multiple dimensions: accuracy, speed, and robustness.

> **Built Autonomously with [NEO](https://heyneo.com)** — Your Autonomous AI Engineering Agent
>
> [![VS Code Extension](https://img.shields.io/badge/VS%20Code-NEO-blue?logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)
> [![Cursor Extension](https://img.shields.io/badge/Cursor-NEO-green?logo=cursor)](https://marketplace.cursorapi.com/items/?itemName=NeoResearchInc.heyneo)

## Features

- **5 ASR Models**: IBM Granite, OpenAI Whisper, NVIDIA Canary, Distil-Whisper, Wav2Vec2
- **Comprehensive Metrics**: 
  - WER (Word Error Rate)
  - CER (Character Error Rate)
  - Accuracy (%)
  - RTF (Real-Time Factor)
  - Inference time
- **15+ Test Scenarios**: Clean speech, background noise, accents, fast/slow speech, technical terms, etc.
- **Flexible Evaluation Modes**: Speed, accuracy, or complete evaluation
- **JSON Output Schema**: Standardized metrics schema for result storage

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Complete Evaluation
```bash
python run_evaluation.py --all
```

### Run Accuracy Evaluation Only
```bash
python run_evaluation.py --accuracy
```

### Run Speed Evaluation Only
```bash
python run_evaluation.py --speed
```

### Specify Custom Paths
```bash
python run_evaluation.py --all \
  --data-path ./my_data \
  --output-path ./my_results
```

## Results & Output

### Console Output Example
```
============================================================
ASR EVALUATION FRAMEWORK v1.0.0
============================================================

=== RUNNING COMPLETE EVALUATION (ACCURACY + SPEED) ===

Evaluating Whisper...
Evaluating Wav2Vec2...
Evaluating Distil-Whisper...
Evaluating Canary...
Evaluating Granite...

✓ Results saved to: results/asr_eval_results_all_20260513_123045.json

============================================================
EVALUATION SUMMARY
============================================================

Model: Whisper
  Status: ✓ OK
  Mean Accuracy: 95.23%
  Mean WER: 0.0477

Model: Wav2Vec2
  Status: ✓ OK
  Mean Accuracy: 91.45%
  Mean WER: 0.0855

Model: Distil-Whisper
  Status: ✓ OK
  Mean Accuracy: 93.78%
  Mean WER: 0.0622
```

### JSON Output Format
Results are saved as structured JSON with the following schema:

```json
{
  "evaluation_metadata": {
    "timestamp": "2026-05-13T12:30:45.123Z",
    "evaluator_version": "1.0.0",
    "models_tested": ["Whisper", "Wav2Vec2", "Distil-Whisper"],
    "test_scenarios": 15,
    "evaluation_type": "all"
  },
  "model_results": {
    "Whisper": {
      "model_name": "Whisper",
      "model_id": "openai/whisper-base",
      "initialized": true,
      "aggregate_metrics": {
        "mean_accuracy": 95.23,
        "mean_wer": 0.0477,
        "mean_cer": 0.0234,
        "mean_rtf": 1.15,
        "std_wer": 0.0145
      },
      "test_results": [
        {
          "test_id": 1,
          "test_name": "clean_english",
          "wer": 0.032,
          "cer": 0.015,
          "accuracy": 96.8,
          "inference_time": 2.34,
          "rtf": 1.17
        }
      ]
    }
  },
  "summary": {
    "total_tests": 15,
    "evaluation_type": "all",
    "status": "completed"
  }
}
```

Results location: `results/asr_eval_results_{type}_{timestamp}.json`

## Project Structure

```
.
├── src/                          # Core modules
│   ├── config.py                # Configuration
│   ├── metrics.py               # Metric calculations
│   ├── data_loader.py           # Data loading utilities
│   ├── base_model.py            # ASR model base class
│   └── evaluator.py             # Main evaluator class
├── models/                       # ASR model implementations
│   ├── wav2vec2.py
│   ├── whisper.py
│   ├── distil_whisper.py
│   ├── canary.py
│   └── granite.py
├── tests/                        # Test suite (36 tests)
├── data/                         # Audio files for evaluation
├── results/                      # Output evaluation results
├── notebooks/                    # Jupyter notebooks
├── run_evaluation.py             # CLI entry point
├── asr_eval_test_matrix.csv      # Test scenarios matrix
├── asr_eval_metrics_schema.json  # Output schema
└── requirements.txt              # Python dependencies
```

## Test Matrix

15 test scenarios covering:
- **Clean Speech**: Baseline accuracy testing
- **Robustness**: Background noise, accents, variable speech rates
- **Challenging Conditions**: Whispered speech, music, phone quality
- **Domain-Specific**: Technical vocabulary, numbers, acronyms

## Metrics

### Accuracy Metrics
- **WER (Word Error Rate)**: Percentage of words that differ from reference
- **CER (Character Error Rate)**: Percentage of characters that differ
- **Accuracy**: 100% - WER, normalized to percentage

### Speed Metrics
- **RTF (Real-Time Factor)**: Inference time / audio duration (< 1.0 is real-time)
- **Inference Time**: Total time to transcribe audio (seconds)

## Output

Results are saved as JSON files with the format:
```
results/asr_eval_results_{type}_{timestamp}.json
```

Example output structure:
```json
{
  "evaluation_metadata": {
    "timestamp": "2026-05-13T...",
    "models_tested": ["Whisper", "Wav2Vec2", ...],
    "test_scenarios": 15
  },
  "model_results": {
    "Whisper": {
      "model_name": "Whisper",
      "aggregate_metrics": {
        "mean_accuracy": 95.3,
        "mean_wer": 0.047,
        "mean_rtf": 0.45
      },
      "test_results": [...]
    }
  }
}
```

## Testing

Run the full test suite:
```bash
pytest tests/ -v
```

## Requirements

- Python 3.10+
- librosa: Audio processing
- numpy, scipy: Numerical computing
- transformers: HuggingFace model loading
- jiwer: WER/CER calculation
- soundfile: Audio file I/O
- pytest: Testing framework

## Model Details

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| Whisper | Medium | ~1.2x RTF | High |
| Wav2Vec2 | Small | ~0.5x RTF | Medium |
| Distil-Whisper | Small | ~0.4x RTF | High |
| Canary | Medium | ~1.5x RTF | High |
| Granite | Large | ~2.0x RTF | Medium |

## Configuration

Environment variables (see `.env.example`):
- `HUGGINGFACE_TOKEN`: HuggingFace API token
- `OPENAI_API_KEY`: OpenAI API key
- `ASR_EVAL_DATA_PATH`: Data directory path
- `ASR_EVAL_RESULTS_PATH`: Results output path
- `VERBOSE`: Enable verbose logging

## License

ISC

## Author

Claude Code - Automated ASR Evaluation Framework
