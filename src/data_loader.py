import os
import json
from pathlib import Path

class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.ensure_path()

    def ensure_path(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_path, exist_ok=True)

    def load_audio_files(self, directory=None):
        """Load all audio files from directory"""
        target_dir = directory or self.data_path
        audio_files = []

        if not os.path.exists(target_dir):
            return audio_files

        for file in os.listdir(target_dir):
            if file.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                audio_files.append(os.path.join(target_dir, file))

        return audio_files

    def load_transcriptions(self, metadata_file=None):
        """Load reference transcriptions from metadata file"""
        if metadata_file and os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return {}

    def save_metadata(self, metadata, output_file):
        """Save metadata to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def list_datasets(self):
        """List all available datasets"""
        datasets = []
        if os.path.exists(self.data_path):
            datasets = os.listdir(self.data_path)
        return datasets
