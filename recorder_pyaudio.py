import pyaudio

class Recorder:
    _devices = []

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


class Device:
    def __init__(self):
        self.name = ''
        self.index = -1
        self.rate = 0

    def deviceName(self):
        return self.name

