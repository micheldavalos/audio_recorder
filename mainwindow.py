from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
# from recorder import Recorder
from recorder_pyaudio import Recorder


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        self.recorder = Recorder()

        for device in self.recorder.devices():
            self.ui.comboBox.addItem(device.deviceName())


        self.ui.comboBox.currentIndexChanged.connect(self.update_rates)
        if self.recorder.count():
            self.ui.comboBox.setCurrentText(self.recorder.default().name)
            self.update_rates(0)

        #
        #
        # if self.ui.comboBox.count():
        #     self.ui.pushButton.setEnabled(True)
        #
        # self.ui.pushButton.clicked.connect(self.record)
        # self.ui.pushButton_2.clicked.connect(self.stop)

    def record(self, index):
        self.recorder.record()

    def stop(self):
        self.recorder.stop()

    @Slot(int)
    def update_rates(self, index):
        # pass
        self.ui.comboBox_2.clear()
        for rate in self.recorder.rates(index):
            self.ui.comboBox_2.addItem(str(rate))

        self.ui.comboBox_2.setCurrentText(self.ui.comboBox_2.itemText(self.ui.comboBox_2.count()-1))

