import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    audio1 = ""
    audio2 = ""

    def __init__(self):
        super().__init__()
        self.title = 'Blind Audio Seperation'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Choose First Audio', self)
        button.setToolTip('This is an example button')
        button.move(40, 70)
        button.clicked.connect(self.on_click1)

        button = QPushButton('Choose Second Audio', self)
        button.setToolTip('This is an example button')
        button.move(160, 70)
        button.clicked.connect(self.on_click1)

        self.show()

    @pyqtSlot()
    def on_click1(self):
        self.audio1 = self.openChoose1()

    @pyqtSlot()
    def on_click2(self):
        self.audio2 = self.openChoose2()

    def openChoose1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose File 1", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            return fileName
        else:
            return ""

    def openChoose2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose File 2", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            return fileName
        else:
            return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())