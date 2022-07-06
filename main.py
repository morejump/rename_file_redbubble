import os
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageEnhance


def handleSelectFolder():
    labelSuccess.configure(text="")
    root = filedialog.askdirectory()
    labelSelectedPath.configure(text=root)
    return


def enhanceImage(filePath):
    try:
        print(f"Handling {filePath}...")
        # filePath = f"{folder}/{filename}"
        #  Enhance color
        image = Image.open(filePath)
        coloredImage = ImageEnhance.Color(image)
        coloredImage.enhance(1.2).save(filePath)
        image.close()
        # Enhance Sharpness
        # image = Image.open(filePath)
        # coloredImage = ImageEnhance.Sharpness(image)
        # coloredImage.enhance(2).save(filePath)
        # image.close()
        # Enhance Brightness
        # image = Image.open(filePath)
        # coloredImage = ImageEnhance.Brightness(image)
        # coloredImage.enhance(1.1).save(filePath)
        # image.close()

        print(f"Complete handling {filePath}!")
    except Exception as ex:
        print(f"Ignoring handle {filePath} cause by an exception: {ex}")
    return


def enhanceImages():
    features = []
    executor = ThreadPoolExecutor(5)
    folder = labelSelectedPath.cget("text")
    if isIncludeSubFolder.get() == 0:
        print("Handle only root folder")
        for filename in os.listdir(folder):
            if filename.lower().endswith('.png'):
                filePath = f"{folder}/{filename}"
                feature = executor.submit(enhanceImage, filePath)
                features.append(feature)
    else:
        print("Including sub folder")
        for path, subdirs, files in os.walk(folder):
            for name in files:
                if name.lower().endswith('.png'):
                    filePath = f"{path}/{name}".replace("\\", "/")
                    feature = executor.submit(enhanceImage, filePath)
                    features.append(feature)
    imageNumbers = len(features)
    wait(features)
    labelSuccess.configure(text=f"Bypass {imageNumbers} images successfully")
    print("ALL IMAGES IS HANDLED!!!")
    return


def onClickBypass():
    labelSuccess.configure(text=f"Processing...")
    threading.Thread(target=enhanceImages).start()


window = Tk()
window.title("Redbubble Bypasser - v1.4")
window.geometry("400x130")
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
# including sub-folder
isIncludeSubFolder = IntVar()
cbSubFolder = Checkbutton(window, text="Including SubFolder", variable=isIncludeSubFolder)
cbSubFolder.grid(column=0, row=2)
# Add a rename button
btnBypass = Button(window, text="Bypass", command=onClickBypass)
btnBypass.grid(column=0, row=3)
# Add label successfully
labelSuccess = Label(window, text="", font=("Arial", 10))
labelSuccess.grid(column=0, row=4)

window.mainloop()
