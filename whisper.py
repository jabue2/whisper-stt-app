import subprocess
import threading

import numpy as np
import torch
from faster_whisper import WhisperModel
from pynput import keyboard
from scipy.signal import resample_poly
import pyperclip
from recorder import Recorder

global is_on, is_recording
recorder = Recorder()
is_on, is_recording = False, False
model = None

def load_model(model_name):
    #device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    device = "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"[fastWhisper] Loading model '{model_name}' on {device}/{compute_type}")
    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    return model


def on_press(key):
    global is_on, is_recording
    if key == keyboard.Key.f1 and is_on and not is_recording:
        is_recording = True
        start_recording()
    elif key == keyboard.Key.f1 and is_on and is_recording:
        print("Stop recording...")
        is_recording = False
        transcribe(recorder.stop())
    elif key == keyboard.Key.f7:
        print("Ending Session...")
        is_on = False
        return False
    return None


def start_key_listener():
    global is_on
    listener = keyboard.Listener(on_press=on_press)
    if listener.running and is_on == False:
        listener.stop()
    elif not listener.running and is_on == False:
        listener.start()
        is_on = True
        while is_on:
            pass

def start_recording():
    print("Start Recording...")
    recorder.start()

def transcribe(frames):
    frames_16k = resample_poly(frames, 16000, 44100).astype(np.float32)
    print(frames_16k.shape, frames_16k.dtype, frames_16k.size)
    try:
        segments, info = model.transcribe(frames_16k, beam_size=3)
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

    recorder.open()
    try:
        t = threading.Thread(target=start_key_listener)
        t.start()
        while t.is_alive():
            pass
    finally:
        recorder.close()


