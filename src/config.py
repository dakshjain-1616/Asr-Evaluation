import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    DATA_PATH = os.getenv('ASR_EVAL_DATA_PATH', './data')
    RESULTS_PATH = os.getenv('ASR_EVAL_RESULTS_PATH', './results')
    VERBOSE = os.getenv('VERBOSE', 'False').lower() == 'true'

    MODELS = {
        'granite': 'ibm/granite-34b-code-instruct',
        'whisper': 'openai/whisper-base',
        'canary': 'nvidia/canary-1b',
        'distil-whisper': 'distilhuggingface/distil-whisper-base',
        'wav2vec2': 'facebook/wav2vec2-base-960h',
    }

    SAMPLE_RATE = 16000
    AUDIO_FORMAT = 'wav'

    @classmethod
    def ensure_paths(cls):
        for path in [cls.DATA_PATH, cls.RESULTS_PATH]:
            os.makedirs(path, exist_ok=True)
