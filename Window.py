import sys
from pydexarm import Dexarm
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Dexarm = Dexarm("COM3")
        self.resize(250, 250)
        self.setWindowTitle("CodersLegacy")

        self.Label = QLabel(self)
        self.Label.setText("Radius:")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.Label, 1, 0)

        self.input = QLineEdit()
        self.input.setFixedWidth(150)
        self.layout.addWidget(self.input, 1, 1)

        button = QPushButton("Set Radius")
        button.clicked.connect(self.get)
        self.layout.addWidget(button, 2, 0)

        button = QPushButton("Clear Text")
        button.clicked.connect(self.input.clear)
        self.layout.addWidget(button, 2, 1)

    def get(self):
        text = self.input.text()
        if text == int:
            self.Dexarm.circle(text)
        else:
            label = QLabel(self)
            label.setText("Vul een nummer in!")
            self.layout.addWidget(label, 0, 1)



