import os
from tkinter import *
from tkinter import filedialog
from os.path import isfile, join
import shutil


def handleSelectFolder():
    labelSuccess.configure(text="")
    path = filedialog.askdirectory()
    labelSelectedPath.configure(text=path)
    return


def divideFolderImages():
    count = 0
    folder = labelSelectedPath.cget("text")
    onlyfiles = [file for file in os.listdir(folder) if isfile(join(folder, file))]
    print(onlyfiles)
    _numberImage = int(numberImages.get())
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
    labelSuccess.configure(text="Successfully divided images")
    return


window = Tk()
window.title("Divide images into folders")
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
# add textbox get number of image per folder
labelNumberImages = Label(window, text="Entering number of image per folder:", anchor="w")
labelNumberImages.grid(column=0, row=2)
numberImages = Entry(window)
numberImages.grid(column=1, row=2)
# Add button divide images
btnRename = Button(window, text="Divide", command=divideFolderImages)
btnRename.grid(column=0, row=3)
# Add label successfully
labelSuccess = Label(window, text="", fg="green", font=("Arial", 10))
labelSuccess.grid(column=0, row=4)

window.mainloop()
