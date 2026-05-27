from pynput import keyboard

model_name = "distil-large-v3"
available_models = ["distil-large-v3", "distil-medium.en", "distil-small.en"]
toggle_key = keyboard.Key.f1
end_key = keyboard.Key.f7
samplerate = 44100
channels = 1
beam_size = 3
