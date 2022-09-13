# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(448, 303)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtFolderPath = QtWidgets.QLabel(self.centralwidget)
        self.txtFolderPath.setGeometry(QtCore.QRect(10, 30, 291, 16))
        self.txtFolderPath.setObjectName("txtFolderPath")
        self.edtNumberImages = QtWidgets.QLineEdit(self.centralwidget)
        self.edtNumberImages.setGeometry(QtCore.QRect(10, 50, 41, 20))
        self.edtNumberImages.setObjectName("edtNumberImages")
        self.lblNumberImage = QtWidgets.QLabel(self.centralwidget)
        self.lblNumberImage.setGeometry(QtCore.QRect(60, 50, 91, 16))
        self.lblNumberImage.setObjectName("lblNumberImage")
        self.btnDevide = QtWidgets.QPushButton(self.centralwidget)
        self.btnDevide.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.btnDevide.setObjectName("btnDevide")
        self.btnUndivide = QtWidgets.QPushButton(self.centralwidget)
        self.btnUndivide.setGeometry(QtCore.QRect(90, 80, 75, 23))
        self.btnUndivide.setObjectName("btnUndivide")
        self.lblMessage = QtWidgets.QLabel(self.centralwidget)
        self.lblMessage.setGeometry(QtCore.QRect(10, 110, 291, 16))
        self.lblMessage.setText("")
        self.lblMessage.setObjectName("lblMessage")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 117, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblFolder = QtWidgets.QLabel(self.widget)
        self.lblFolder.setObjectName("lblFolder")
        self.horizontalLayout.addWidget(self.lblFolder)
        self.btnBrowser = QtWidgets.QPushButton(self.widget)
        self.btnBrowser.setObjectName("btnBrowser")
        self.horizontalLayout.addWidget(self.btnBrowser)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 448, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.txtFolderPath.setText(_translate("MainWindow", "N/A"))
        self.lblNumberImage.setText(_translate("MainWindow", "images/folder"))
        self.btnDevide.setText(_translate("MainWindow", "Divide"))
        self.btnUndivide.setText(_translate("MainWindow", "UnDivide"))
        self.lblFolder.setText(_translate("MainWindow", "Folder:"))
        self.btnBrowser.setText(_translate("MainWindow", "Browser..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())