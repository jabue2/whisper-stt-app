import subprocess
import threading

import numpy as np
import torch
from faster_whisper import WhisperModel
from pynput import keyboard
from scipy.signal import resample_poly
import pyperclip
from recorder import Recorder
from stateMachine import StateMachine

recorder = Recorder()

def load_model(model_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"[fastWhisper] Loading model '{model_name}' on {device}/{compute_type}")
    tts_model = WhisperModel(model_name, device=device, compute_type=compute_type)
    return tts_model


def on_press(key):
    if key == keyboard.Key.f1:
        SM.toggle_recording()
    elif key == keyboard.Key.f7:
        print("Ending Session...")
        return False
    return None


def start_key_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def transcribe(frames):
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

def notify(text):
    subprocess.run(["osascript", "-e",
                    f'display notification "{text}" with title "Whisper"'])

if __name__ == '__main__':
    model = load_model("distil-large-v3")
    SM = StateMachine(recorder, transcribe)
    recorder.init_audiostream()
    t = threading.Thread(target=start_key_listener)
    t.start()
    t.join()
    recorder.close()


