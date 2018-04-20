import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from scipy.io import wavfile
import numpy as np
import pylab as pl
from sklearn.decomposition import FastICA


class App(QWidget):

    audio1 = ""
    audio2 = ""

    def __init__(self):
        super().__init__()
        self.title = 'Blind Audio Seperation'
        self.left = 50
        self.top = 50
        self.width = 300
        self.height = 250
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button1 = QPushButton('Choose First Audio', self)
        button1.setToolTip('This is an example button')
        button1.move(40, 70)
        button1.clicked.connect(self.on_click1)

        button2 = QPushButton('Choose Second Audio', self)
        button2.setToolTip('This is an example button')
        button2.move(160, 70)
        button2.clicked.connect(self.on_click2)

        self.button3 = QPushButton('Start Processing', self)
        self.button3.setToolTip('This is an example button')
        self.button3.move(100, 150)
        self.button3.clicked.connect(self.on_click3)

        self.show()

    @pyqtSlot()
    def on_click1(self):
        self.audio1 = self.openChoose1()

    @pyqtSlot()
    def on_click2(self):
        self.audio2 = self.openChoose2()

    @pyqtSlot()
    def on_click3(self):
        if self.audio1 != "" and self.audio2 != "":
            self.button3.setEnabled(False)
            self.start_processing()
        else:
            btnMsg = QMessageBox.question(self, 'Alert!' , 'Path not Chosen!',QMessageBox.Ok)

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


    def start_processing(self):
        fs_1, voice_1 = wavfile.read(self.audio1)
        fs_2, voice_2 = wavfile.read(self.audio2)
        m, = voice_1.shape
        voice_2 = voice_2[:m]

        S = np.c_[voice_1, voice_2]
        A = np.array([[1, 1], [0.5, 2]])  # Mixing matrix
        X = np.dot(S, A.T)  # Generate observations
        # Compute ICA
        ica = FastICA()
        S_ = ica.fit(X).transform(X)  # Get the estimated sources
        A_ = ica.mixing_  # Get estimated mixing matrix
        np.allclose(X, np.dot(S_, A_.T))

        multiply_factor = 1000000;

        temp_output_1 = multiply_factor * S_[:, 0]
        temp_output_2 = multiply_factor * S_[:, 1]

        wavfile.write("Seperated_1" + ".wav", fs_2, temp_output_1.astype(np.int16))
        wavfile.write("Seperated_2" + ".wav", fs_2, temp_output_2.astype(np.int16))

        print("Done!")
        msgDone = QMessageBox.question(self, 'Alert!', 'Processing Done! Check File!', QMessageBox.Ok)
        self.button3.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())