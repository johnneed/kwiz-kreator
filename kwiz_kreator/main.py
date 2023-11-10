import sys

from PyQt5.QtWidgets import QApplication

from src import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec())
