from PySide2.QtWidgets import QApplication
import sys
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())