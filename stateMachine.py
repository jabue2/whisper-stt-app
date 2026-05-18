import threading
from recorder import Recorder


class StateMachine:

    def __init__(self, recorder: Recorder, transcribe_func):
        self.recorder = recorder
        self.state = "IDLE"
        self.transcribe_func = transcribe_func

    def toggle_recording(self):
        if self.state == "IDLE":
            self.start_recording()
        elif self.state == "RECORDING":
            self.stop_recording()
        elif self.state == "TRANSCRIBING":
            print("Still transcribing...")

    def start_recording(self):
        self.state = "RECORDING"
        print("Started Recording...")
        self.recorder.start()

    def stop_recording(self):
        print("Stopped Recording...")
        self.start_transcribing(self.recorder.stop())

    def start_transcribing(self, frames):
        self.state = "TRANSCRIBING"
        print("Started Transcribing...")
        threading.Thread(target=self.finish_transcribing, args=(frames,), daemon=True).start()

    def finish_transcribing(self, frames):
        try:
            self.transcribe_func(frames)
        finally:
            self.state = "IDLE"

    def get_state(self):
        return self.state
