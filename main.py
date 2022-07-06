import os
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from tkinter import *
from tkinter import filedialog

from PIL import Image


def handleSelectOriginalFolder():
    processLabel.configure(text="")
    root = filedialog.askdirectory()
    originalEntry.delete(0, END)
    originalEntry.insert(0, root)
    return


def handleSelectResizeFolder():
    processLabel.configure(text="")
    root = filedialog.askdirectory()
    resizeEntry.delete(0, END)
    resizeEntry.insert(0, root)
    return


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
    executor = ThreadPoolExecutor(10)
    folder = originalEntry.get()
    for filename in os.listdir(folder):
        filepath = f"{folder}/{filename}"
        feature = executor.submit(resizeImage, filepath, filename)
        features.append(feature)
    wait(features)
    processLabel.configure(text="All images were resized completely")
    print("ALL DONE")
    return


def resizeImage(filePath, filename):
    print(f"starting crop {filename}")
    originalImage = Image.open(filePath)
    cropImage = originalImage.crop(originalImage.getbbox())
    if cropImage.size[0] >= cropImage.size[1]:
        resizeBaseWith(cropImage, filename)
    else:
        resizeBaseHeight(cropImage, filename)
    return


if __name__ == '__main__':
    MAX_WITH = 4500
    MAX_HEIGHT = 5400
    window = Tk()
    window.title("Redbubble Standardizer v1.1")
    window.geometry("800x200")
    # an original section
    originalLabel = Label(window, text="Original folder")
    originalLabel.grid(column=0, row=0, sticky=W)
    originalEntry = Entry(window, width=80)
    originalEntry.grid(column=1, row=0)
    btnSelectOriginal = Button(window, text="Browse...", command=handleSelectOriginalFolder)
    btnSelectOriginal.grid(column=2, row=0)
    # a resize section
    resizeLabel = Label(window, text="Resize folder")
    resizeLabel.grid(column=0, row=1, sticky=W)
    resizeEntry = Entry(window, width=80)
    resizeEntry.grid(column=1, row=1)
    btnSelectResize = Button(window, text="Browse...", command=handleSelectResizeFolder)
    btnSelectResize.grid(column=2, row=1)
    # process section
    btnProcess = Button(window, text="Start", width=10, command=onStart)
    btnProcess.grid(column=0, row=2, sticky=W)
    # process section
    processLabel = Label(window, text="")
    processLabel.grid(column=0, row=3, sticky=W)

    window.mainloop()
