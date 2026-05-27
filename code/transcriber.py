import numpy as np
import pyperclip
import torch
from faster_whisper import WhisperModel
from scipy.signal import resample_poly

import config
from notifier import notify


def load_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"[fastWhisper] Loading model '{model_name}' on {device}/{compute_type}")
    tts_model = WhisperModel(model_name, device=device, compute_type=compute_type)
    config.model = tts_model

def transcribe(frames, model: WhisperModel):
    if frames.size == 0:
        print("No audio detected")
        return
    frames_16k = resample_poly(frames, 16000, 44100).astype(np.float32)
    print(frames_16k.shape, frames_16k.dtype, frames_16k.size)
    try:
        segments, info = model.transcribe(frames_16k, beam_size=3, vad_filter=True)
        text = " ".join(seg.text.strip() for seg in segments).strip()
        print(text)
        pyperclip.copy(text)
        notify("Copied to clipboard!")
    except Exception as e:
        print(e)