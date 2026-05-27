import threading

import config
from recorder import Recorder
from enum import Enum
from threading import Lock

class AppState(Enum):
    IDLE = "IDLE"
    RECORDING = "RECORDING"
    TRANSCRIBING = "TRANSCRIBING"

class StateMachine:

    lock = Lock()

    def __init__(self, recorder: Recorder, transcribe_func):
        self.recorder = recorder
        self.state = AppState.IDLE
        self.transcribe_func = transcribe_func

    def toggle_recording(self, lock):
        lock.acquire()
        if self.state == AppState.IDLE:
            self.start_recording()
        elif self.state == AppState.RECORDING:
            self.stop_recording()
        elif self.state == AppState.TRANSCRIBING:
            print("Still transcribing...")
        lock.release()

    def start_recording(self):
        self.state = AppState.RECORDING
        print("Started Recording...")
        self.recorder.start()

    def stop_recording(self):
        print("Stopped Recording...")
        self.start_transcribing(self.recorder.stop())

    def start_transcribing(self, frames):
        self.state = AppState.TRANSCRIBING
        print("Started Transcribing...")
        threading.Thread(target=self.finish_transcribing, args=(frames,), daemon=True).start()

    def finish_transcribing(self, frames):
        try:
            self.transcribe_func(frames, config.model)
        finally:
            self.state = AppState.IDLE

    def get_state(self):
        return self.state
