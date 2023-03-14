from PyQt6.QtWidgets import QApplication, QWidget
import sys
import Window

app = QApplication(sys.argv)

window = Window.MainWindow()
window.show()

sys.exit(app.exec())
