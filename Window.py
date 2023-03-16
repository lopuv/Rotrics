import sys
from pydexarm import Dexarm
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Dexarm = Dexarm("COM5")
        self.resize(250, 250)
        self.setWindowTitle("CodersLegacy")

        self.Label = QLabel(self)
        self.Label.setText("Segments:")
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.Label, 1, 0)

        self.input = QLineEdit()
        self.input.setFixedWidth(150)
        self.layout.addWidget(self.input, 1, 1)

        self.Label1 = QLabel(self)
        self.Label1.setText("Radius:")
        self.layout.addWidget(self.Label, 2, 0)

        self.input1 = QLineEdit()
        self.input1.setFixedWidth(150)
        self.layout.addWidget(self.input1, 2, 1)

        button = QPushButton("Set Radius")
        button.clicked.connect(self.get)
        self.layout.addWidget(button, 3, 0)

        button = QPushButton("Clear Text")
        button.clicked.connect(self.input.clear)
        self.layout.addWidget(button, 3, 1)

    def get(self):
        text = int(self.input.text())
        segments = int(self.input1.text())
        self.Dexarm.circle(text, segments)




