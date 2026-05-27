import sounddevice as sd
import numpy as np
import config


class Recorder:
    def __init__(self):
        self.samplerate = config.samplerate
        self.channels = config.channels
        self._recording = False
        self._frames = []
        self._stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print("STATUS: ", status)
        if self._recording:
            self._frames.append(indata.flatten())

    def _input_device(self):
        default_input = sd.default.device[0]
        if default_input >= 0:
            return default_input

        for index, device in enumerate(sd.query_devices()):
            if device.get("max_input_channels", 0) > 0:
                return index

        raise RuntimeError("No microphone input device is available.")

    def init_audiostream(self):
        self._stream = sd.InputStream(
            device=self._input_device(),
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
