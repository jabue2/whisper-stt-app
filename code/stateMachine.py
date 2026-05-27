import threading
from notifier import notify
from recorder import Recorder
from enum import Enum
from threading import Lock


class AppState(Enum):
    IDLE = "IDLE"
    RECORDING = "RECORDING"
    TRANSCRIBING = "TRANSCRIBING"


class StateMachine:

    def __init__(self, recorder: Recorder, transcribe_func):
        self.recorder = recorder
        self.state = AppState.IDLE
        self.transcribe_func = transcribe_func
        self.lock = Lock()

    def toggle_recording(self):
        with self.lock:
            if self.state == AppState.IDLE:
                self.start_recording()
            elif self.state == AppState.RECORDING:
                self.stop_recording()
            elif self.state == AppState.TRANSCRIBING:
                print("Still transcribing...")

    def start_recording(self):
        self.state = AppState.RECORDING
        print("Started Recording...")
        notify("Transcription App", "Recording...")
        self.recorder.start()

    def stop_recording(self):
        print("Stopped Recording...")
        notify("Transcription App", "Stopped Recording...")
        self.start_transcribing(self.recorder.stop())

    def start_transcribing(self, frames):
        self.state = AppState.TRANSCRIBING
        print("Started Transcribing...")
        threading.Thread(target=self.finish_transcribing, args=(frames,), daemon=True).start()

    def finish_transcribing(self, frames):
        try:
            self.transcribe_func(frames)
        finally:
            with self.lock:
                self.state = AppState.IDLE

    def get_state(self):
        return self.state
