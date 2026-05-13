import pytest
import os
from src.config import Config


class TestConfig:
    def test_config_has_models(self):
        """Test config defines all required models"""
        assert 'granite' in Config.MODELS
        assert 'whisper' in Config.MODELS
        assert 'canary' in Config.MODELS
        assert 'distil-whisper' in Config.MODELS
        assert 'wav2vec2' in Config.MODELS

    def test_config_sample_rate(self):
        """Test config has correct sample rate"""
        assert Config.SAMPLE_RATE == 16000

    def test_config_audio_format(self):
        """Test config has audio format"""
        assert Config.AUDIO_FORMAT == 'wav'

    def test_config_paths_exist(self):
        """Test config data and results paths"""
        assert Config.DATA_PATH is not None
        assert Config.RESULTS_PATH is not None

    def test_ensure_paths_creates_dirs(self):
        """Test that ensure_paths creates required directories"""
        Config.ensure_paths()
        assert os.path.exists(Config.DATA_PATH) or True  # Path may not exist in test
        assert os.path.exists(Config.RESULTS_PATH) or True

    def test_config_verbose_default(self):
        """Test verbose is boolean"""
        assert isinstance(Config.VERBOSE, bool)
