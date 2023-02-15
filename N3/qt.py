import sys
from PyQt5.QtWidgets import QApplication, QWidget

def GUI():
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(400, 400)
    w.setWindowTitle('OZRA NALOGA 3')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    GUI()
