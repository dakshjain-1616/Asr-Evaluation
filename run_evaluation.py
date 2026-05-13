#!/usr/bin/env python3
"""
ASR Evaluation Framework - Main Entry Point
Evaluates multiple ASR models across various test scenarios
"""

import argparse
import json
import csv
import os
from datetime import datetime
from pathlib import Path

from src.config import Config
from src.evaluator import Evaluator
from src.data_loader import DataLoader
from src.metrics import Metrics
from models.wav2vec2 import Wav2Vec2Model
from models.whisper import WhisperModel
from models.distil_whisper import DistilWhisperModel
from models.canary import CanaryModel
from models.granite import GraniteModel


def load_test_matrix(csv_file):
    """Load test matrix from CSV file"""
    test_matrix = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_matrix.append(row)
    return test_matrix


def initialize_models():
    """Initialize all ASR models"""
    models = [
        Wav2Vec2Model(),
        WhisperModel(),
        DistilWhisperModel(),
        CanaryModel(),
        GraniteModel(),
    ]
    return models


def generate_sample_data():
    """Generate sample audio metadata for testing"""
    sample_metadata = {
        "sample_1.wav": "this is a test recording",
        "sample_2.wav": "hello world speech recognition",
        "sample_3.wav": "automatic speech recognition evaluation",
    }
    return sample_metadata


def save_results(results, output_path, evaluation_type):
    """Save evaluation results to JSON file"""
    os.makedirs(output_path, exist_ok=True)

    output_data = {
        "evaluation_metadata": {
            "timestamp": datetime.now().isoformat(),
            "evaluator_version": "1.0.0",
            "models_tested": list(results.keys()),
            "test_scenarios": sum(len(v) for v in results.values()),
            "evaluation_type": evaluation_type,
        },
        "model_results": results,
        "summary": {
            "total_tests": sum(len(v) for v in results.values()),
            "evaluation_type": evaluation_type,
            "status": "completed",
        },
    }

    output_file = os.path.join(output_path, f"asr_eval_results_{evaluation_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    return output_file


def run_accuracy_evaluation(models, data_loader):
    """Run accuracy evaluation"""
    print("\n=== RUNNING ACCURACY EVALUATION ===\n")

    # Generate sample metadata
    references = generate_sample_data()

    # Load audio files or use sample references
    audio_files = list(references.keys())

    evaluator = Evaluator(models)
    results = {}

    for model in models:
        print(f"Evaluating {model.model_name}...")
        model_results = []

        for audio_file in audio_files:
            result = evaluator.evaluate_single_model(
                model,
                audio_file,
                references.get(audio_file)
            )
            model_results.append(result)

        aggregated = evaluator.metrics.aggregate_metrics(
            [r for r in model_results if 'wer' in r]
        )

        results[model.model_name] = {
            "model_name": model.model_name,
            "model_id": model.model_id,
            "initialized": model.initialized,
            "test_results": model_results,
            "aggregate_metrics": aggregated if aggregated else {},
        }

    return results


def run_speed_evaluation(models, data_loader):
    """Run speed evaluation"""
    print("\n=== RUNNING SPEED EVALUATION ===\n")

    audio_files = list(generate_sample_data().keys())

    evaluator = Evaluator(models)
    results = {}

    for model in models:
        print(f"Evaluating speed for {model.model_name}...")
        model_results = []

        for audio_file in audio_files:
            result = evaluator.evaluate_single_model(model, audio_file)
            model_results.append(result)

        # Calculate RTF for speed results
        speed_metrics = []
        for result in model_results:
            if 'inference_time' in result and not 'error' in result:
                speed_metrics.append({
                    'rtf': result['inference_time'] / 1.0,  # Assume ~1 second audio
                    'inference_time': result['inference_time'],
                })

        aggregated = evaluator.metrics.aggregate_metrics(speed_metrics) if speed_metrics else {}

        results[model.model_name] = {
            "model_name": model.model_name,
            "model_id": model.model_id,
            "initialized": model.initialized,
            "test_results": model_results,
            "aggregate_metrics": aggregated,
        }

    return results


def run_all_evaluation(models, data_loader):
    """Run complete evaluation (accuracy + speed)"""
    print("\n=== RUNNING COMPLETE EVALUATION (ACCURACY + SPEED) ===\n")

    accuracy_results = run_accuracy_evaluation(models, data_loader)
    speed_results = run_speed_evaluation(models, data_loader)

    # Merge results
    for model_name in accuracy_results:
        if model_name in speed_results:
            accuracy_results[model_name]["speed_metrics"] = speed_results[model_name]["aggregate_metrics"]

    return accuracy_results


def main():
    parser = argparse.ArgumentParser(
        description='ASR Evaluation Framework - Benchmark speech recognition models'
    )
    parser.add_argument(
        '--speed',
        action='store_true',
        help='Run speed/RTF evaluation'
    )
    parser.add_argument(
        '--accuracy',
        action='store_true',
        help='Run accuracy (WER/CER) evaluation'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run complete evaluation (accuracy + speed)'
    )
    parser.add_argument(
        '--data-path',
        default=Config.DATA_PATH,
        help='Path to audio data directory'
    )
    parser.add_argument(
        '--output-path',
        default=Config.RESULTS_PATH,
        help='Path to save results'
    )

    args = parser.parse_args()

    # Default to all if no specific evaluation type specified
    if not args.speed and not args.accuracy and not args.all:
        args.all = True

    # Initialize
    Config.ensure_paths()
    models = initialize_models()
    data_loader = DataLoader(args.data_path)

    print("=" * 60)
    print("ASR EVALUATION FRAMEWORK v1.0.0")
    print("=" * 60)

    results = None
    eval_type = None

    try:
        if args.accuracy:
            results = run_accuracy_evaluation(models, data_loader)
            eval_type = "accuracy"

        elif args.speed:
            results = run_speed_evaluation(models, data_loader)
            eval_type = "speed"

        elif args.all:
            results = run_all_evaluation(models, data_loader)
            eval_type = "all"

        if results:
            output_file = save_results(results, args.output_path, eval_type)
            print(f"\n✓ Results saved to: {output_file}\n")
            print("=" * 60)
            print("EVALUATION SUMMARY")
            print("=" * 60)
            for model_name, data in results.items():
                print(f"\nModel: {model_name}")
                print(f"  Status: {'✓ OK' if data['initialized'] else '✗ Failed'}")
                if data['aggregate_metrics']:
                    metrics = data['aggregate_metrics']
                    if 'mean_accuracy' in metrics:
                        print(f"  Mean Accuracy: {metrics['mean_accuracy']:.2f}%")
                    if 'mean_wer' in metrics:
                        print(f"  Mean WER: {metrics['mean_wer']:.4f}")

    except Exception as e:
        print(f"\n✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
