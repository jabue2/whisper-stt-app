import sounddevice as sd
import numpy as np

class Recorder:
    def __init__(self, samplerate=44100, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self._recording = False
        self._frames = []
        self._stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print("STATUS: ", status)
        if self._recording:
            self._frames.append(indata.flatten())

    def init_audiostream(self):
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype="float32",
            callback=self._callback,
        )

    def start(self):
        self._frames = []
        self._recording = True
        self._stream.start()

    def stop(self):
        self._recording = False
        self._stream.stop()
        return np.concatenate(self._frames, axis=0) if self._frames else np.array([], dtype=np.float32)

    def close(self):
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
