import os
import time
from pathlib import Path
from .metrics import Metrics
from .data_loader import DataLoader

class Evaluator:
    def __init__(self, models, metrics=None):
        self.models = models
        self.metrics = metrics or Metrics()
        self.results = {}

    def evaluate_single_model(self, model, audio_file, reference_text=None):
        """Evaluate a single model on an audio file"""
        try:
            result = model.inference_with_timing(audio_file)
            hypothesis = result['text']
            inference_time = result['inference_time']

            output = {
                'model': model.model_name,
                'audio_file': audio_file,
                'hypothesis': hypothesis,
                'inference_time': inference_time,
            }

            if reference_text:
                output['wer'] = self.metrics.calculate_wer(reference_text, hypothesis)
                output['cer'] = self.metrics.calculate_cer(reference_text, hypothesis)
                output['accuracy'] = self.metrics.calculate_accuracy(output['wer'])

            return output
        except Exception as e:
            return {
                'model': model.model_name,
                'audio_file': audio_file,
                'error': str(e),
            }

    def evaluate_all_models(self, audio_files, references=None):
        """Evaluate all models on a set of audio files"""
        results = {model.model_name: [] for model in self.models}

        for idx, audio_file in enumerate(audio_files):
            reference = references.get(audio_file) if references else None

            for model in self.models:
                if not model.health_check():
                    model.load_model()

                result = self.evaluate_single_model(model, audio_file, reference)
                results[model.model_name].append(result)

        return results

    def evaluate_accuracy(self, audio_files, references):
        """Run accuracy evaluation"""
        return self.evaluate_all_models(audio_files, references)

    def evaluate_speed(self, audio_files):
        """Run speed evaluation"""
        return self.evaluate_all_models(audio_files, references=None)

    def get_aggregate_results(self, results):
        """Get aggregated metrics from evaluation results"""
        aggregated = {}

        for model_name, model_results in results.items():
            if not model_results:
                continue

            valid_results = [r for r in model_results if 'wer' in r]
            if valid_results:
                aggregated[model_name] = self.metrics.aggregate_metrics(valid_results)

        return aggregated
