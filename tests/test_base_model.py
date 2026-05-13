import pytest
from src.base_model import ASRModel


class MockModel(ASRModel):
    """Mock ASR model for testing"""
    def load_model(self):
        self.initialized = True

    def transcribe(self, audio_path):
        return "test transcription"


class TestASRModel:
    def test_model_initialization(self):
        """Test model initialization"""
        model = MockModel('TestModel', 'test/model-id')
        assert model.model_name == 'TestModel'
        assert model.model_id == 'test/model-id'
        assert model.initialized == False

    def test_load_model(self):
        """Test loading model"""
        model = MockModel('TestModel', 'test/model-id')
        model.load_model()
        assert model.initialized == True

    def test_transcribe(self):
        """Test transcription"""
        model = MockModel('TestModel', 'test/model-id')
        result = model.transcribe('dummy.wav')
        assert result == "test transcription"

    def test_inference_with_timing(self):
        """Test inference with timing"""
        model = MockModel('TestModel', 'test/model-id')
        result = model.inference_with_timing('dummy.wav')
        assert 'text' in result
        assert 'inference_time' in result
        assert result['text'] == "test transcription"
        assert result['inference_time'] >= 0

    def test_health_check(self):
        """Test health check"""
        model = MockModel('TestModel', 'test/model-id')
        assert model.health_check() == False
        model.load_model()
        assert model.health_check() == True

    def test_model_repr(self):
        """Test model representation"""
        model = MockModel('TestModel', 'test/model-id')
        repr_str = repr(model)
        assert 'TestModel' in repr_str
        assert 'initialized=False' in repr_str
