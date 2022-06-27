import os
import uuid
import threading
from tkinter import *
from tkinter import filedialog


def handleSelectFolder():
    labelSuccess.configure(text="")
    path = filedialog.askdirectory()
    labelSelectedPath.configure(text=path)
    return


def renameFile(sourcePath, cutText):
    filename = sourcePath.split("/")[-1]
    lastBackSlash = sourcePath.rfind("/")
    folder = sourcePath[:lastBackSlash].strip()

    lastOccur = filename.rfind(cutText)
    print(f"last occur: {lastOccur}")
    if lastOccur != -1:
        print(f"last occur: {lastOccur}")
        newFile = filename[:lastOccur].strip()
        dst = f"{folder}/{newFile}.png"
        try:
            os.rename(sourcePath, dst)
        except FileExistsError as ex:
            uniqueId = str(uuid.uuid4()).split("-")[-1]
            dst = f"{folder}/{newFile}_{uniqueId}.png"
            os.rename(sourcePath, dst)
        except Exception as ex:
            print(f"An exception occurred: {ex}")
            pass

    return


def startRename():
    labelSuccess.configure(text="Processing...")
    folder = labelSelectedPath.cget("text")
    if isIncludeSubFolder.get() == 0:
        print("Handle only root folder")
        for filename in os.listdir(folder):
            if filename.lower().endswith('.png'):
                sourcePath = f"{folder}/{filename}"
                print(sourcePath)
                renameFile(sourcePath, cutToText.get())
    else:
        print("Including sub folder")
        for path, subdirs, files in os.walk(folder):
            for filename in files:
                if filename.lower().endswith('.png'):
                    sourcePath = f"{path}/{filename}".replace("\\", "/")
                    print(sourcePath)
                    renameFile(sourcePath, cutToText.get())

    labelSuccess.configure(text="Successfully renamed all images files!")
    return


def processImages():
    threading.Thread(target=startRename).start()
    return


window = Tk()
window.title("Rename images v1.2")
window.geometry("400x200")
# Add a intro label
labelIntro = Label(window, text="Select the folder:")
labelIntro.grid(column=0, row=0)
# Add button select a folder
btnSelectFolder = Button(window, text="Browse...", command=handleSelectFolder)
btnSelectFolder.grid(column=1, row=0)
# Add a path label
labelPath = Label(window, text="Path:", anchor="w")
labelPath.grid(column=0, row=1)
# Add a selected path label
labelSelectedPath = Label(window, text="N/A", anchor="w")
labelSelectedPath.grid(column=1, row=1)
# Entry text
labelCutToText = Label(window, text="Trim to keyword: ", anchor="w")
labelCutToText.grid(column=0, row=2)

cutToText = Entry(window)
cutToText.grid(column=1, row=2)
# including Sub-Folder
isIncludeSubFolder = IntVar()
cbSubFolder = Checkbutton(window, text="Including SubFolder", variable=isIncludeSubFolder)
cbSubFolder.grid(column=0, row=3)
# Add a rename button
btnRename = Button(window, text="Rename all files", command=processImages)
btnRename.grid(column=0, row=4)
# Add label successfully
labelSuccess = Label(window, text="")
labelSuccess.grid(column=0, row=5)

window.mainloop()
