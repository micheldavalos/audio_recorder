from PySide2.QtMultimedia import QAudioDeviceInfo, QAudio, QAudioRecorder, QAudioEncoderSettings, QMultimedia
from PySide2.QtCore import QUrl

class Recorder:
    def __init__(self):
        self.devices = []
        self.default = ''

        self.interfaces()

        self.audioRecorder = QAudioRecorder()

    def interfaces(self):
        self.devices = QAudioDeviceInfo.availableDevices(QAudio.AudioInput)
        self.default = QAudioDeviceInfo.defaultInputDevice()
        print(self.default.supportedCodecs())


    def rates(self, index):
        return self.devices[index].supportedSampleRates()

    def record(self):
        settings = QAudioEncoderSettings()
        settings.setCodec('audio/x-flac')
        settings.setQuality(QMultimedia.HighQuality)

        self.audioRecorder.setEncodingSettings(settings)
        self.audioRecorder.setAudioInput(self.default.deviceName())

        print(self.audioRecorder.supportedAudioCodecs())

        self.audioRecorder.setOutputLocation(QUrl.fromLocalFile("test.flac"))
        self.audioRecorder.record()

    def stop(self):
        self.audioRecorder.stop()
