import threading
from key_listener import start_key_listener
from recorder import Recorder
from stateMachine import StateMachine
from transcriber import load_model, transcribe

if __name__ == '__main__':
    recorder = Recorder()
    load_model("distil-large-v3")
    SM = StateMachine(recorder, transcribe)
    recorder.init_audiostream()
    t = threading.Thread(target=start_key_listener, args=(SM,))
    t.start()
    t.join()
    recorder.close()