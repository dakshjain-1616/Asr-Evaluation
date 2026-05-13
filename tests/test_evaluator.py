import pytest
from src.evaluator import Evaluator
from src.base_model import ASRModel


class MockModel(ASRModel):
    def load_model(self):
        self.initialized = True

    def transcribe(self, audio_path):
        return "transcribed text"


class TestEvaluator:
    def test_evaluator_initialization(self):
        """Test evaluator initialization"""
        model = MockModel('MockModel', 'mock/id')
        evaluator = Evaluator([model])
        assert len(evaluator.models) == 1

    def test_evaluate_single_model_no_reference(self):
        """Test evaluating single model without reference"""
        model = MockModel('MockModel', 'mock/id')
        model.load_model()
        evaluator = Evaluator([model])
        result = evaluator.evaluate_single_model(model, 'test.wav')
        assert 'model' in result
        assert 'audio_file' in result
        assert 'hypothesis' in result
        assert result['hypothesis'] == "transcribed text"

    def test_evaluate_single_model_with_reference(self):
        """Test evaluating single model with reference"""
        model = MockModel('MockModel', 'mock/id')
        model.load_model()
        evaluator = Evaluator([model])
        result = evaluator.evaluate_single_model(
            model,
            'test.wav',
            reference_text='transcribed text'
        )
        assert 'wer' in result
        assert 'cer' in result
        assert 'accuracy' in result
        assert result['wer'] == 0.0  # Perfect match

    def test_evaluate_all_models(self):
        """Test evaluating all models"""
        models = [
            MockModel('Model1', 'mock1'),
            MockModel('Model2', 'mock2'),
        ]
        for m in models:
            m.load_model()

        evaluator = Evaluator(models)
        audio_files = ['test1.wav', 'test2.wav']
        references = {'test1.wav': 'text one', 'test2.wav': 'text two'}

        results = evaluator.evaluate_all_models(audio_files, references)
        assert 'Model1' in results
        assert 'Model2' in results
        assert len(results['Model1']) == 2
        assert len(results['Model2']) == 2

    def test_get_aggregate_results(self):
        """Test aggregating results"""
        models = [MockModel('Model1', 'mock1')]
        evaluator = Evaluator(models)

        results = {
            'Model1': [
                {
                    'wer': 0.1,
                    'cer': 0.05,
                    'accuracy': 90.0,
                    'rtf': 0.1,
                },
                {
                    'wer': 0.2,
                    'cer': 0.1,
                    'accuracy': 80.0,
                    'rtf': 0.2,
                },
            ]
        }

        agg = evaluator.get_aggregate_results(results)
        assert 'Model1' in agg
        assert abs(agg['Model1']['mean_wer'] - 0.15) < 0.001
        assert abs(agg['Model1']['mean_accuracy'] - 85.0) < 0.001
