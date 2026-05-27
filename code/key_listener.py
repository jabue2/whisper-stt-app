from pynput import keyboard
from threading import Lock
from stateMachine import StateMachine

lock = Lock()

def start_key_listener(SM: StateMachine):
    def on_press(key):
        if key == keyboard.Key.f1:
            SM.toggle_recording(lock)
        elif key == keyboard.Key.f7:
            print("Ending Session...")
            return False
        return None

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()