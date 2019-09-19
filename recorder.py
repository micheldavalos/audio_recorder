from PySide2.QtMultimedia import QAudioDeviceInfo, QAudio


class Recorder:
    def __init__(self):
        self.devices = []
        self.default = ''

        self.interfaces()

    def interfaces(self):
        self.devices = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)
        self.default = QAudioDeviceInfo.defaultInputDevice()

    def rates(self, index):
        return self.devices[index].supportedSampleRates()

    def record(self, index, rate, location):
        pass