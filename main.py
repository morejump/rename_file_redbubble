import shutil
import logging
import PyQt5
from getmac import get_mac_address as gma
from active_dialog import Ui_Dialog
from PyQt5 import QtGui, QtWidgets
import requests
from config import DEPLOY_LINK
import threading
import resize
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QFileDialog, QSystemTrayIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread, QRunnable, QThreadPool
from PIL import Image
import sys
import os
import dbm
import dbm.dumb


def resizeBaseWith(image, filename):
    basewidth = MAX_WITH
    wpercent = (basewidth / float(image.size[0]))
    hsize = min(int((float(image.size[1]) * float(wpercent))), MAX_HEIGHT)
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    backgroundTrans = Image.new("RGBA", (MAX_WITH, MAX_HEIGHT), (255, 255, 255, 0))
    xBasis = int((backgroundTrans.size[0] - image.size[0]) / 2)
    yBasis = int((backgroundTrans.size[1] - image.size[1]) / 2)
    backgroundTrans.paste(image, (xBasis, yBasis))
    resizeFolder = mainWindow.edtResizeFolder.text()
    backgroundTrans.save(f"{resizeFolder}/{filename}")
    return


def resizeBaseHeight(image, filename):
    baseheight = MAX_HEIGHT
    hpercent = (baseheight / float(image.size[1]))
    wsize = min(int((float(image.size[0]) * float(hpercent))), MAX_WITH)
    image = image.resize((wsize, baseheight), Image.ANTIALIAS)
    backgroundTrans = Image.new("RGBA", (MAX_WITH, MAX_HEIGHT), (255, 255, 255, 0))
    xBasis = int((backgroundTrans.size[0] - image.size[0]) / 2)
    yBasis = int((backgroundTrans.size[1] - image.size[1]) / 2)
    backgroundTrans.paste(image, (xBasis, yBasis))
    resizeFolder = mainWindow.edtResizeFolder.text()
    backgroundTrans.save(f"{resizeFolder}/{filename}")
    return


def onStart():
    global isStart
    isStart = not isStart
    if isStart:
        logging.info("Starting")
        mainWindow.btnStart.setText("Stop")
        mainWindow.btnStart.setStyleSheet("background-color : red; color: white;")
        threading.Thread(target=resizeImages).start()
    else:
        threadPool.clear()
        logging.info("Stopping")
        mainWindow.btnStart.setText("Start")
        mainWindow.btnStart.setStyleSheet("background-color : green; color: white;")
    return


def resizeImages():
    global threadPool
    threadPool.setMaxThreadCount(int(mainWindow.edtParallelHandling.text()))
    logging.info("Starting resize images")
    global MAX_WITH
    global MAX_HEIGHT
    if mainWindow.edtWidth.text() != "":
        MAX_WITH = int(mainWindow.edtWidth.text())
    if mainWindow.edtHeight.text() != "":
        MAX_HEIGHT = int(mainWindow.edtHeight.text())

    if MAX_WITH == 0 or MAX_HEIGHT == 0:
        logging.info(f"Please, Enter your expect size, Current expect size W:H = {MAX_WITH}:{MAX_HEIGHT}")
        return

    folder = mainWindow.edtOriginalFolder.text()
    for filename in os.listdir(folder):
        filepath = f"{folder}/{filename}"
        threadPool.start(ResizeImageTask(filepath, filename))

    threadPool.waitForDone()

    totalImage = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
    resizeFolder = mainWindow.edtResizeFolder.text()
    successImage = len([name for name in os.listdir(resizeFolder) if os.path.isfile(os.path.join(resizeFolder, name))])
    errorFolder = f'{folder}/error_images'
    failImage = 0
    if os.path.exists(errorFolder):
        failImage = len([name for name in os.listdir(errorFolder) if os.path.isfile(os.path.join(errorFolder, name))])
    logging.info(f"Try to resize {totalImage} images: {successImage} succeed, {failImage} failed ")
    return


def resizeImage(filePath, filename):
    try:
        logging.info(f"starting crop {filename}")
        originalImage = Image.open(filePath)
        cropImage = originalImage.crop(originalImage.getbbox())
        if cropImage.size[0] >= cropImage.size[1]:
            resizeBaseWith(cropImage, filename)
        else:
            resizeBaseHeight(cropImage, filename)
    except Exception as ex:
        logging.info(f"Image {filename}: {ex}")
        currentFolder = originalEntry.get()
        errorFolder = f'{currentFolder}/error_images'
        if not os.path.exists(errorFolder):
            os.makedirs(errorFolder)
        shutil.copy(filePath, errorFolder)
    finally:
        originalImage.close()
        cropImage.close()
    return


class ResizeImageTask(QRunnable):

    def __init__(self, filePath, filename):
        super(ResizeImageTask, self).__init__()
        self.filePath = filePath
        self.filename = filename

    def run(self):
        resizeImage(self.filePath, self.filename)


class MainWindow(QMainWindow, resize.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon_app.ico'))
        self.setupUi(self)
        self.btnBrowserOriginal.clicked.connect(self.openOriginalFolder)
        self.btnBrowserResize.clicked.connect(self.openResizeFolder)

    def openOriginalFolder(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(None, 'Select a original folder:', 'C:\\',
                                                          QFileDialog.ShowDirsOnly)
            logging.info(folderPath)
            if folderPath:
                self.edtOriginalFolder.setText(folderPath)
        except Exception as ex:
            logging.info(ex)
        return

    def openResizeFolder(self):
        try:
            folderPath = QFileDialog.getExistingDirectory(None, 'Select a resize folder:', 'C:\\',
                                                          QFileDialog.ShowDirsOnly)
            logging.info(folderPath)
            if folderPath:
                self.edtResizeFolder.setText(folderPath)
        except Exception as ex:
            logging.info(ex)
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
    if "succeed" in msg:
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

    isStart = False
    MAX_WITH = 0
    MAX_HEIGHT = 0

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
    mainWindow.setWindowTitle("Image resizer v1.0 - Copyright © 2023 By MMO.FARM")
    intValidator = PyQt5.QtGui.QIntValidator()
    #  threadpool
    threadPool = QThreadPool.globalInstance()
    threadPool.clear()
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
    mainWindow.edtWidth.setValidator(intValidator)
    mainWindow.edtHeight.setValidator(intValidator)
    mainWindow.btnStart.clicked.connect(onStart)

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
