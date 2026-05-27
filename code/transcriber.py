import numpy as np
import pyperclip
import torch
from faster_whisper import WhisperModel
from scipy.signal import resample_poly

import config
from notifier import notify


class Transcriber:
    def __init__(self, model_name):
        self.model = self.load_model(model_name)

    def load_model(self, model_name):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        print(f"[fastWhisper] Loading model '{model_name}' on {device}/{compute_type}")
        tts_model = WhisperModel(model_name, device=device, compute_type=compute_type)
        return tts_model

    def transcribe(self, frames):
        if frames.size == 0:
            print("No audio detected")
            return
        frames_16k = resample_poly(frames, 16000, config.samplerate).astype(np.float32)
        print(frames_16k.shape, frames_16k.dtype, frames_16k.size)
        try:
            segments, info = self.model.transcribe(frames_16k, beam_size=config.beam_size, vad_filter=True)
            text = " ".join(seg.text.strip() for seg in segments).strip()
            print(text)
            pyperclip.copy(text)
            notify("Transcription App", "Copied to clipboard!")
            return text
        except Exception as e:
            print(e)
            return None
