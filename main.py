import os
import sys
import threading
from tkinter import *
from tkinter import filedialog
from os.path import isfile, join
import shutil
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QFileDialog, QSystemTrayIcon
import layout


class MainWindow(QMainWindow, layout.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon_app.ico'))
        self.setupUi(self)
        self.btnBrowser.clicked.connect(self.openImagesFolder)
        return

    def openImagesFolder(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            folderNames = dlg.selectedFiles()
            self.txtFolderPath.setText(folderNames[0])
            self.lblMessage.setText("")
        return


def divideFolderImages():
    count = 0
    folder = mainWindow.txtFolderPath.text()
    onlyfiles = [file for file in os.listdir(folder) if isfile(join(folder, file))]
    print(onlyfiles)
    _numberImage = int(mainWindow.edtNumberImages.text())
    while len(onlyfiles) != 0:
        count += 1
        numberAddImage = 0
        if (len(onlyfiles)) < _numberImage:
            numberAddImage = len(onlyfiles)
        else:
            numberAddImage = _numberImage

        newDirectory = f"acc_{count}"
        path = os.path.join(folder, newDirectory)
        if not os.path.exists(path):
            os.makedirs(path)

        for index in range(numberAddImage):
            shutil.move(f"{folder}/{onlyfiles[index]}", f"{path}/{onlyfiles[index]}")
        onlyfiles = [file for file in os.listdir(folder) if isfile(join(folder, file))]
    mainWindow.lblMessage.setText("Successfully divided images")
    return


def undivideFolderImages():
    mainFolder = mainWindow.txtFolderPath.text()
    for path, subdirs, files in os.walk(mainFolder):
        for name in files:
            filePath = os.path.join(path, name)
            shutil.move(filePath, mainFolder)

    folders = list(os.walk(mainFolder))[1:]
    for folder in folders:
        if not folder[2]:
            os.rmdir(folder[0])
    mainWindow.lblMessage.setText("Successfully undivided images")
    return


def processDivideFolder():
    threading.Thread(target=divideFolderImages).start()
    return

def processUndivideFolder():
    threading.Thread(target=undivideFolderImages).start()
    return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Divide Folder v1.2")
    mainWindow.btnDivide.clicked.connect(processDivideFolder)
    mainWindow.btnUndivide.clicked.connect(processUndivideFolder)
    mainWindow.show()
    app.exec_()
