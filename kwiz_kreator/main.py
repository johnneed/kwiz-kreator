import sys

from PyQt5.QtWidgets import QApplication

from kwiz_kreator.src.app import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())
