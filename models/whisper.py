import sys
sys.path.insert(0, '.')

from src.base_model import ASRModel

class WhisperModel(ASRModel):
    def __init__(self):
        super().__init__('Whisper', 'openai/whisper-base')
        self.model = None

    def load_model(self):
        """Load OpenAI Whisper model"""
        try:
            import whisper
            self.model = whisper.load_model("base")
            self.initialized = True
        except Exception as e:
            print(f"Warning: Could not load {self.model_name}: {e}")
            self.initialized = False

    def transcribe(self, audio_path):
        """Transcribe audio using Whisper"""
        if not self.initialized:
            return ""

        try:
            result = self.model.transcribe(audio_path)
            return result['text'].strip()
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
