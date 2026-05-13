import pytest
from src.metrics import Metrics


class TestMetrics:
    def test_calculate_wer_identical(self):
        """Test WER when hypothesis matches reference"""
        m = Metrics()
        wer = m.calculate_wer("hello world", "hello world")
        assert wer == 0.0

    def test_calculate_wer_different(self):
        """Test WER with different text"""
        m = Metrics()
        wer = m.calculate_wer("hello world", "goodbye world")
        assert 0 < wer <= 1.0

    def test_calculate_cer_identical(self):
        """Test CER when hypothesis matches reference"""
        m = Metrics()
        cer = m.calculate_cer("hello", "hello")
        assert cer == 0.0

    def test_calculate_cer_different(self):
        """Test CER with different text"""
        m = Metrics()
        cer = m.calculate_cer("hello", "hallo")
        assert 0 < cer <= 1.0

    def test_calculate_rtf(self):
        """Test Real-Time Factor calculation"""
        m = Metrics()
        rtf = m.calculate_rtf(0.5, 10.0)
        assert rtf == 0.05

    def test_calculate_rtf_zero_duration(self):
        """Test RTF with zero audio duration"""
        m = Metrics()
        rtf = m.calculate_rtf(1.0, 0.0)
        assert rtf == 0.0

    def test_calculate_accuracy(self):
        """Test accuracy calculation from WER"""
        m = Metrics()
        accuracy = m.calculate_accuracy(0.1)
        assert accuracy == 90.0

    def test_calculate_accuracy_perfect(self):
        """Test accuracy with perfect transcription"""
        m = Metrics()
        accuracy = m.calculate_accuracy(0.0)
        assert accuracy == 100.0

    def test_calculate_accuracy_negative(self):
        """Test accuracy with high WER doesn't go below 0"""
        m = Metrics()
        accuracy = m.calculate_accuracy(1.5)
        assert accuracy == 0.0

    def test_aggregate_metrics_empty(self):
        """Test aggregation with empty results"""
        m = Metrics()
        result = m.aggregate_metrics([])
        assert result == {}

    def test_aggregate_metrics_single(self):
        """Test aggregation with single result"""
        m = Metrics()
        results = [
            {'wer': 0.1, 'cer': 0.05, 'rtf': 0.1, 'accuracy': 90.0}
        ]
        agg = m.aggregate_metrics(results)
        assert agg['mean_wer'] == 0.1
        assert agg['mean_accuracy'] == 90.0

    def test_aggregate_metrics_multiple(self):
        """Test aggregation with multiple results"""
        m = Metrics()
        results = [
            {'wer': 0.1, 'cer': 0.05, 'rtf': 0.1, 'accuracy': 90.0},
            {'wer': 0.2, 'cer': 0.1, 'rtf': 0.2, 'accuracy': 80.0},
        ]
        agg = m.aggregate_metrics(results)
        assert abs(agg['mean_wer'] - 0.15) < 0.001
        assert abs(agg['mean_accuracy'] - 85.0) < 0.001
