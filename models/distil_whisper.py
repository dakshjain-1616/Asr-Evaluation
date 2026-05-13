import sys
sys.path.insert(0, '.')

from src.base_model import ASRModel
import librosa

class DistilWhisperModel(ASRModel):
    def __init__(self):
        super().__init__('Distil-Whisper', 'distilhuggingface/distil-whisper-base')
        self.model = None
        self.processor = None

    def load_model(self):
        """Load Distil-Whisper model"""
        try:
            from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
            self.processor = AutoProcessor.from_pretrained("distilhuggingface/distil-whisper-base")
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained("distilhuggingface/distil-whisper-base")
            self.initialized = True
        except Exception as e:
            print(f"Warning: Could not load {self.model_name}: {e}")
            self.initialized = False

    def transcribe(self, audio_path):
        """Transcribe audio using Distil-Whisper"""
        if not self.initialized:
            return ""

        try:
            audio, sr = librosa.load(audio_path, sr=16000)
            inputs = self.processor(audio, sampling_rate=16000, return_tensors="pt")

            with __import__('torch').no_grad():
                generated_ids = self.model.generate(inputs["input_features"])

            transcription = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return transcription
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
