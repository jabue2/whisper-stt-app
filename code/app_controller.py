from transcriber import Transcriber
from stateMachine import StateMachine, AppState
from recorder import Recorder
import config
from threading import Lock


class AppController:
    def __init__(self):
        self.recorder = Recorder()
        self.transcriber = None
        self.state_machine = None
        self.model_name = config.model_name
        self.history = []
        self.history_lock = Lock()
        self.available_models = config.available_models

    def start(self):
        self.recorder.init_audiostream()
        self.load_model(self.model_name)
        self.state_machine = StateMachine(self.recorder, self.transcribe_and_store)

    def transcribe_and_store(self, frames):
        text = self.transcriber.transcribe(frames)
        if text:
            with self._get_history_lock():
                self.history.insert(0, text)
                self.history = self.history[:10]
        return text

    def _get_history_lock(self):
        if not hasattr(self, "history_lock"):
            self.history_lock = Lock()
        return self.history_lock

    def get_history(self):
        with self._get_history_lock():
            return list(self.history)

    def clear_history(self):
        with self._get_history_lock():
            self.history = []

    def get_status_text(self):
        if self.state_machine is None:
            return "Starting"
        return self.state_machine.get_state().value

    def load_model(self, model_name):
        self.model_name = model_name
        self.transcriber = Transcriber(model_name)

    def set_model(self, model_name):
        if self.state_machine is not None and self.state_machine.get_state() != AppState.IDLE:
            return False
        self.load_model(model_name)
        return True

    def close(self):
        self.recorder.close()
