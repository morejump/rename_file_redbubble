from os import listdir
import pathlib
from tkinter import *
from tkinter import filedialog
import tkinter
import os


def handleSelectFolder():
    labelSuccess.configure(text="")
    path = filedialog.askdirectory()
    labelSelectedPath.configure(text=path)
    return


def handleRenameAllFiles():
    folder = labelSelectedPath.cget("text")
    for count, filename in enumerate(os.listdir(folder)):
        if filename.lower().endswith('.png'):
            lastOccur = filename.rfind("T-Shirt")
            if lastOccur != -1:
                print(f"last occur: {lastOccur}")
                newFile = filename[:lastOccur].strip()
                dst = f"{newFile}.png"
                dst = f"{folder}/{dst}"
                src = f"{folder}/{filename}"
                try:
                    os.rename(src, dst)
                except:
                    print("An exception occurred")
                    pass
    labelSuccess.configure(text="Successfully renamed all image files!")
    return


window = Tk()
window.title("Rename all image files in a specific folder")
window.geometry("400x100")
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
# Add a rename button
# Add button select a folder
btnRename = Button(window, text="Rename all files", command=handleRenameAllFiles)
btnRename.grid(column=0, row=2)
# Add label successfully
labelSuccess = Label(window, text="", fg="green", font=("Arial", 10))
labelSuccess.grid(column=0, row=3)

window.mainloop()
