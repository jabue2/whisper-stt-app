import threading
import config
from transcriber import Transcriber
from key_listener import start_key_listener
from recorder import Recorder
from stateMachine import StateMachine


if __name__ == '__main__':
    recorder = Recorder()
    transcriber = Transcriber(config.model_name)
    SM = StateMachine(recorder, transcriber.transcribe)
    recorder.init_audiostream()
    t = threading.Thread(target=start_key_listener, args=(SM,))
    t.start()
    t.join()
    recorder.close()
