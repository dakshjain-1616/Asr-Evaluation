import numpy as np
from jiwer import wer, cer

class Metrics:
    @staticmethod
    def calculate_wer(reference, hypothesis):
        """Calculate Word Error Rate"""
        try:
            return wer(reference, hypothesis)
        except Exception:
            return 1.0

    @staticmethod
    def calculate_cer(reference, hypothesis):
        """Calculate Character Error Rate"""
        try:
            return cer(reference, hypothesis)
        except Exception:
            return 1.0

    @staticmethod
    def calculate_rtf(inference_time, audio_duration):
        """Calculate Real-Time Factor (inference_time / audio_duration)"""
        if audio_duration == 0:
            return 0.0
        return inference_time / audio_duration

    @staticmethod
    def calculate_accuracy(wer_score):
        """Convert WER to accuracy percentage"""
        return max(0, 1.0 - wer_score) * 100

    @staticmethod
    def aggregate_metrics(results):
        """Aggregate metrics from multiple evaluations"""
        if not results:
            return {}

        return {
            'mean_wer': np.mean([r['wer'] for r in results]),
            'mean_cer': np.mean([r['cer'] for r in results]),
            'mean_rtf': np.mean([r['rtf'] for r in results]),
            'mean_accuracy': np.mean([r['accuracy'] for r in results]),
            'std_wer': np.std([r['wer'] for r in results]),
            'std_rtf': np.std([r['rtf'] for r in results]),
        }
