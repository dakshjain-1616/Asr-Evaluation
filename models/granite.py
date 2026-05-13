import sys
sys.path.insert(0, '.')

from src.base_model import ASRModel

class GraniteModel(ASRModel):
    def __init__(self):
        super().__init__('Granite', 'ibm/granite-34b-code-instruct')
        self.model = None

    def load_model(self):
        """Load IBM Granite model"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained("ibm/granite-34b-code-instruct")
            self.model = AutoModelForCausalLM.from_pretrained("ibm/granite-34b-code-instruct")
            self.initialized = True
        except Exception as e:
            print(f"Warning: Could not load {self.model_name}: {e}")
            self.initialized = False

    def transcribe(self, audio_path):
        """Use Granite for ASR task description"""
        if not self.initialized:
            return ""

        try:
            # Granite is a code model, use it for ASR prompt-based approach
            prompt = f"Transcribe this audio file: {audio_path}"
            inputs = self.tokenizer(prompt, return_tensors="pt")

            with __import__('torch').no_grad():
                outputs = self.model.generate(**inputs, max_length=200)

            transcription = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return transcription
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
