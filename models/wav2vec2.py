import sys
sys.path.insert(0, '.')

from src.base_model import ASRModel
import librosa
import numpy as np

class Wav2Vec2Model(ASRModel):
    def __init__(self):
        super().__init__('Wav2Vec2', 'facebook/wav2vec2-base-960h')
        self.model = None
        self.processor = None

    def load_model(self):
        """Load Wav2Vec2 model and processor"""
        try:
            from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
            self.processor = Wav2Vec2Processor.from_pretrained(self.model_id)
            self.model = Wav2Vec2ForCTC.from_pretrained(self.model_id)
            self.initialized = True
        except Exception as e:
            print(f"Warning: Could not load {self.model_name}: {e}")
            self.initialized = False

    def transcribe(self, audio_path):
        """Transcribe audio using Wav2Vec2"""
        if not self.initialized:
            return ""

        try:
            audio, sr = librosa.load(audio_path, sr=16000)
            inputs = self.processor(audio, sampling_rate=16000, return_tensors="pt")

            with __import__('torch').no_grad():
                logits = self.model(**inputs).logits

            predicted_ids = __import__('torch').argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
            return transcription
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
