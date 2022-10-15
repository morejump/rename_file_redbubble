import shutil
import logging
import PyQt5
from getmac import get_mac_address as gma
from active_dialog import Ui_Dialog
from PyQt5 import QtGui, QtWidgets
import requests
from config import DEPLOY_LINK
import threading
import layout
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QFileDialog, QSystemTrayIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, QRunnable, QThreadPool
from PIL import Image
import sys
import os
import dbm
import dbm.dumb


def resizeBaseWith(image, filename):
    print(f"Resizing {filename}")
    basewidth = MAX_WITH
    wpercent = (basewidth / float(image.size[0]))
    hsize = min(int((float(image.size[1]) * float(wpercent))), MAX_HEIGHT)
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    backgroundTrans = Image.open("true_size_transparent.png")
    xBasis = int((backgroundTrans.size[0] - image.size[0]) / 2)
    yBasis = int((backgroundTrans.size[1] - image.size[1]) / 2)
    backgroundTrans.paste(image, (xBasis, yBasis))
    resizeFolder = resizeEntry.get()
    backgroundTrans.save(f"{resizeFolder}/{filename}")
    print(f"Complete resize {filename}")
    return


def resizeBaseHeight(image, filename):
    print(f"Resizing {filename}")
    baseheight = MAX_HEIGHT
    hpercent = (baseheight / float(image.size[1]))
    wsize = min(int((float(image.size[0]) * float(hpercent))), MAX_WITH)
    image = image.resize((wsize, baseheight), Image.ANTIALIAS)
    backgroundTrans = Image.open("true_size_transparent.png")
    xBasis = int((backgroundTrans.size[0] - image.size[0]) / 2)
    yBasis = int((backgroundTrans.size[1] - image.size[1]) / 2)
    backgroundTrans.paste(image, (xBasis, yBasis))
    resizeFolder = resizeEntry.get()
    backgroundTrans.save(f"{resizeFolder}/{filename}")
    print(f"Complete resize {filename}")
    return


def onStart():
    threading.Thread(target=resizeImages).start()
    return


def resizeImages():
    processLabel.configure(text="Processing")
    features = []
    executor = ThreadPoolExecutor(int(threadEntry.get()))
    folder = originalEntry.get()
    for filename in os.listdir(folder):
        filepath = f"{folder}/{filename}"
        feature = executor.submit(resizeImage, filepath, filename)
        features.append(feature)
    wait(features)

    totalImage = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
    resizeFolder = resizeEntry.get()
    successImage = len([name for name in os.listdir(resizeFolder) if os.path.isfile(os.path.join(resizeFolder, name))])
    errorFolder = f'{folder}/error_images'
    failImage = 0
    if os.path.exists(errorFolder):
        failImage = len([name for name in os.listdir(errorFolder) if os.path.isfile(os.path.join(errorFolder, name))])
    processLabel.configure(text=f"Resize {totalImage} images: {successImage} succeed, {failImage} failed ")
    print("ALL DONE")
    return


def resizeImage(filePath, filename):
    try:
        print(f"starting crop {filename}")
        originalImage = Image.open(filePath)
        cropImage = originalImage.crop(originalImage.getbbox())
        if cropImage.size[0] >= cropImage.size[1]:
            resizeBaseWith(cropImage, filename)
        else:
            resizeBaseHeight(cropImage, filename)
    except Exception as ex:
        print(f"Image {filename}: {ex}")
        currentFolder = originalEntry.get()
        errorFolder = f'{currentFolder}/error_images'
        if not os.path.exists(errorFolder):
            os.makedirs(errorFolder)
        shutil.copy(filePath, errorFolder)
    finally:
        originalImage.close()
        cropImage.close()
    return


class MainWindow(QMainWindow, layout.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon_app.ico'))
        self.setupUi(self)
        self.btnBrowserOriginal.clicked.connect(self.openOriginalFolder)

    def openOriginalFolder(self):
        folderPath = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QtGui.QFileDialog.ShowDirsOnly)
        if folderPath:
            self.edtOriginalFolder.setText(folderPath[0])
        return


def handleActiveKey(key: str):
    if checkActiveKey(key):
        db[KEY_ACTIVE_KEY] = key
        activeKeyDialog.hide()
        mainWindow.show()
    else:
        activeKeyDialogUI.lblMessage.setText("ERROR: Check your key or internet connection")
    return


def checkActiveKey(key: str):
    if key == "":
        return False
    try:
        response = requests.get(DEPLOY_LINK)
        if response.status_code == 200:
            data = response.json()
            keyCMSLink = data["link"]
            print(keyCMSLink)
            mac = gma()
            print(mac)
            payload = {'dataRequest': 'ResizeKey', 'activeKeyUser': key, 'macUser': mac}
            response = requests.get(keyCMSLink, params=payload)
            if response.status_code == 200:
                data = response.json()
                status = data["status"]
                print(status)
                if status == "OK":
                    return True
    except Exception as ex:
        print(ex)
    return False


class QTextEditLogger(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        msg = self.format(record)
        logSignal.emitData(msg)
        return


class LogSignal(QObject):
    signal = pyqtSignal(str)

    def emitData(self, message):
        self.signal.emit(message)


def displayMessage(msg: str):
    global displayMsgNumber
    print(msg)
    displayMsgNumber += 1
    if "Successfully" in msg:
        formatColor = '<span style="color:green;">{}</span>'
        mainWindow.edtLogs.appendHtml(formatColor.format(msg))
    else:
        mainWindow.edtLogs.appendPlainText(msg)

    mainWindow.edtLogs.appendPlainText("")
    mainWindow.edtLogs.verticalScrollBar().setValue(mainWindow.edtLogs.verticalScrollBar().maximum())
    if displayMsgNumber == 300:
        mainWindow.edtLogs.clear()
        displayMsgNumber = 0
    return


def savePreferences():
    db[PARALLEL_HANDLING_KEY] = mainWindow.edtParallelHandling.text()
    db[RESIZE_FOLDER_PATH_KEY] = mainWindow.edtResizeFolder.text()
    db[ORIGINAL_FOLDER_PATH_KEY] = mainWindow.edtOriginalFolder.text()
    db.close()
    return


if __name__ == '__main__':

    db = dbm.open('mydb', 'c')
    displayMsgNumber = 0
    KEY_ACTIVE_KEY = "KEY_ACTIVE_KEY"
    ORIGINAL_FOLDER_PATH_KEY = "ORIGINAL_FOLDER_PATH_KEY"
    RESIZE_FOLDER_PATH_KEY = "RESIZE_FOLDER_PATH_KEY"
    PARALLEL_HANDLING_KEY = "PARALLEL_HANDLING_KEY"

    if db.get(KEY_ACTIVE_KEY) is None:
        db[KEY_ACTIVE_KEY] = ""

    if db.get(ORIGINAL_FOLDER_PATH_KEY) is None:
        db[ORIGINAL_FOLDER_PATH_KEY] = ""

    if db.get(RESIZE_FOLDER_PATH_KEY) is None:
        db[RESIZE_FOLDER_PATH_KEY] = ""

    if db.get(PARALLEL_HANDLING_KEY) is None:
        db[PARALLEL_HANDLING_KEY] = "1"

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(savePreferences)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Redbubble resizer v1.0")
    intValidator = PyQt5.QtGui.QIntValidator()
    # setup logs
    logSignal = LogSignal()
    logTextBox = QTextEditLogger()
    logging.basicConfig(filename='logs.txt',
                        filemode='a',
                        format='%(asctime)s - %(module)s:%(lineno)s %(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        level=logging.INFO)

    formatter = logging.Formatter(fmt='%(asctime)s - %(module)s:%(lineno)s %(funcName)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M')

    logTextBox.setFormatter(formatter)

    logging.getLogger().addHandler(logTextBox)
    logSignal.signal.connect(displayMessage)
    logging.info("=========================================")
    logging.info("NEW SESSION")
    # update data from local database
    mainWindow.edtOriginalFolder.setText(db.get(ORIGINAL_FOLDER_PATH_KEY).decode("utf-8"))
    mainWindow.edtResizeFolder.setText(db.get(RESIZE_FOLDER_PATH_KEY).decode("utf-8"))
    mainWindow.edtParallelHandling.setText(db.get(PARALLEL_HANDLING_KEY).decode("utf-8"))
    #
    mainWindow.edtParallelHandling.setValidator(intValidator)

    # setup active key dialog
    activeKeyDialog = QtWidgets.QDialog()
    activeKeyDialog.setWindowTitle("Active Key")
    activeKeyDialog.setWindowIcon(QtGui.QIcon('icon_app.ico'))
    activeKeyDialogUI = Ui_Dialog()
    activeKeyDialogUI.setupUi(activeKeyDialog)
    activeKeyDialogUI.btnActive.clicked.connect(lambda: handleActiveKey(activeKeyDialogUI.edtActiveKey.text()))
    # check active key
    activeKey = db.get(KEY_ACTIVE_KEY).decode("utf-8")
    print(f"active key: {activeKey}")
    if activeKey == "":
        activeKeyDialog.show()
    else:
        if checkActiveKey(activeKey):
            mainWindow.show()
        else:
            activeKeyDialog.show()
    app.exec_()
