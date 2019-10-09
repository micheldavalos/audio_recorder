import pyaudio
import wave
from PySide2.QtCore import QThread

class RecorderPyAudio(QThread):
    _devices = []
    _rec = None
    _recfile = None
    _recording = False
    _index = 0
    _location = 'output.wav'

    def __init__(self):
        super(RecorderPyAudio, self).__init__()

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

    def start_recording(self, index, location='output.wav'):
        self._index = index
        self._location = location

        self.start()

        # self._rec = Recorder(channels=2, rate=int(device.rate), index=device.index)
        #
        # with self._rec.open('output.wav', 'wb') as self._recfile:
        #     self._recfile.start_recording()

    def stop_recording(self):
        self._recording = False

    def run(self):
        device = self._devices[self._index]

        self._rec = Recorder(channels=2, rate=int(device.rate), index=device.index)

        with self._rec.open(self._location, 'wb') as recfile:
            recfile.start_recording()

            self._recording = True

            while self._recording:
                self.msleep(1)
                # print('a')

            recfile.stop_recording()


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

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024, index=0):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.index = index

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer, self.index)

class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                rate, frames_per_buffer, index):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None
        self._index = index

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
                                        stream_callback=self.get_callback(),
                                     input_device_index=self._index)
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            print(frame_count, time_info, status)
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

