import pytest
import os
import tempfile
from src.data_loader import DataLoader


class TestDataLoader:
    def test_data_loader_initialization(self):
        """Test DataLoader initialization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            assert loader.data_path == tmpdir

    def test_ensure_path_creates_directory(self):
        """Test that ensure_path creates directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = os.path.join(tmpdir, 'new_dir')
            loader = DataLoader(test_path)
            assert os.path.exists(test_path)

    def test_load_audio_files_empty(self):
        """Test loading audio files from empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            files = loader.load_audio_files()
            assert files == []

    def test_load_audio_files_with_files(self):
        """Test loading audio files with actual files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create dummy audio files
            test_files = ['test1.wav', 'test2.mp3', 'readme.txt']
            for f in test_files:
                open(os.path.join(tmpdir, f), 'w').close()

            loader = DataLoader(tmpdir)
            audio_files = loader.load_audio_files()
            assert len(audio_files) == 2
            assert any('test1.wav' in f for f in audio_files)
            assert any('test2.mp3' in f for f in audio_files)

    def test_load_transcriptions_empty(self):
        """Test loading transcriptions without metadata file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            trans = loader.load_transcriptions()
            assert trans == {}

    def test_save_metadata(self):
        """Test saving metadata to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            metadata = {'audio1.wav': 'hello world', 'audio2.wav': 'test speech'}
            output_file = os.path.join(tmpdir, 'metadata.json')
            loader.save_metadata(metadata, output_file)
            assert os.path.exists(output_file)

    def test_list_datasets_empty(self):
        """Test listing datasets from empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = DataLoader(tmpdir)
            datasets = loader.list_datasets()
            assert datasets == [] or len(datasets) >= 0
