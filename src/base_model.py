from abc import ABC, abstractmethod
import time

class ASRModel(ABC):
    def __init__(self, model_name, model_id):
        self.model_name = model_name
        self.model_id = model_id
        self.initialized = False

    @abstractmethod
    def load_model(self):
        """Load the model"""
        pass

    @abstractmethod
    def transcribe(self, audio_path):
        """Transcribe audio file and return text"""
        pass

    def inference_with_timing(self, audio_path):
        """Transcribe with timing information"""
        start_time = time.time()
        result = self.transcribe(audio_path)
        inference_time = time.time() - start_time
        return {
            'text': result,
            'inference_time': inference_time,
        }

    def health_check(self):
        """Verify model is working"""
        return self.initialized

    def __repr__(self):
        return f"ASRModel({self.model_name}, initialized={self.initialized})"
