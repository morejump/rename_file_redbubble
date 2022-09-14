import os
import sys
import threading
import re
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
            self.lblProcess.setText("")
            self.txtFolderPath.setText(folderNames[0])
        return


def removeDuplicate():
    mainWindow.lblProcess.setText("Processing")
    count = 0
    folderPath = mainWindow.txtFolderPath.text()
    images = [file for file in os.listdir(folderPath) if isfile(join(folderPath, file))]
    for image in images:
        print(image)
        fileName = image.split(".")[0]
        hasEndNumber = re.search(r"_\d$", fileName)
        hasCopyText = "- Copy" in image
        if hasEndNumber or hasCopyText:
            count += 1
            os.remove(f"{folderPath}/{image}")
    mainWindow.lblProcess.setText(f"Successfully removed {count} duplicate images")
    return


def processRemoveDuplicate():
    threading.Thread(target=removeDuplicate).start()
    return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Duplicate Remover v1.1")
    mainWindow.btnRemoveDuplicate.clicked.connect(processRemoveDuplicate)
    mainWindow.show()
    app.exec_()
