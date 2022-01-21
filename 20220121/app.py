import sys

from PyQt5 import QtWidgets


class MyWindow(object):
    def setupUi(self, main_window):
        main_window.setGeometry(200, 200, 300, 300)
        main_window.setWindowTitle('GUI Example')

        self.label = QtWidgets.QLabel(main_window)
        self.label.setText('Example Label')
        self.label.move(50, 50)

        self.button = QtWidgets.QPushButton(main_window)
        self.button.setText('Click Me')
        self.button.clicked.connect(self.clicked)


    def clicked(self):
        self.label.setText('You pressed button')
        self.update()

    def update(self):
        self.label.adjustSize()

def window():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    u1 = MyWindow()
    u1.setupUi(main_window)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()