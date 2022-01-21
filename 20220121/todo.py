import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(486, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonAdd = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_item())
        self.pushButtonAdd.setGeometry(QtCore.QRect(40, 80, 121, 31))
        self.pushButtonAdd.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(40, 130, 401, 391))
        self.listWidget.setObjectName("listWidget")
        self.pushButtonDelete = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_item())
        self.pushButtonDelete.setGeometry(QtCore.QRect(180, 80, 121, 31))
        self.pushButtonDelete.setObjectName("pushButton_2")
        self.pushButtonClear = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_list())
        self.pushButtonClear.setGeometry(QtCore.QRect(320, 80, 121, 31))
        self.pushButtonClear.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 20, 401, 31))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 486, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ToDo List"))
        self.pushButtonAdd.setText(_translate("MainWindow", "Add Task"))
        self.pushButtonDelete.setText(_translate("MainWindow", "Delete Task"))
        self.pushButtonClear.setText(_translate("MainWindow", "Clear List"))

    def add_item(self):

        item = self.lineEdit.text()
        if item != '':
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            print(item)
            c.execute('INSERT INTO todo_list (list_item) VALUES(?)', [item])
            conn.commit()
            conn.close()
            self.update_list()
            self.lineEdit.clear()

    def delete_item(self):
        clicked = self.listWidget.currentRow()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('DELETE FROM todo_list WHERE id = ?', [clicked])
        conn.commit()
        conn.close()
        self.update_list()

    def clear_list(self):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('DELETE FROM todo_list WHERE 1 = 1')
        conn.commit()
        conn.close()
        self.update_list()

    def update_list(self):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('SELECT * FROM todo_list')
        items = c.fetchall()
        conn.close()
        self.listWidget.clear()
        for item in items:
            self.listWidget.addItem(item[1])
        self.lineEdit.clear()
        self.listWidget.update()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
