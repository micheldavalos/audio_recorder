import pyaudio
import wave


class RecorderPyAudio:
    _devices = []
    _rec = None
    _recfile = None

    def __init__(self):
        pass

    def devices(self):
        p = pyaudio.PyAudio()

        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            # print((i, dev['name'], dev['maxInputChannels']))
            if dev['maxInputChannels'] >= 1:
                device = Device()
                device.name = dev['name']
                device.rate = dev['defaultSampleRate']
                device.index = i

                self._devices.append(device)

        return self._devices

    def rates(self, index):
        return [self._devices[index].rate]

    def count(self):
        return len(self._devices)

    def default(self):
        return self._devices[0]

    def start_recording(self, index):
        device = self._devices[index]

        self._rec = Recorder(channels=2, range = int(device.rate))

        with self._rec.open('output.wav', 'wb') as self._recfile:
            self._recfile.start_recording()

    def stop_recording(self, index):
        self._recfile.stop_recording()


class Device:
    def __init__(self):
        self.name = ''
        self.index = -1
        self.rate = 0

    def deviceName(self):
        return self.name


class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

