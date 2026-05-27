import config
from pynput import keyboard
from stateMachine import StateMachine


def start_key_listener(SM: StateMachine):
    def on_press(key):
        if key == config.toggle_key:
            SM.toggle_recording()
        elif key == config.end_key:
            print("Ending Session...")
            return False
        return None

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()
