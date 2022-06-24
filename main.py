import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageEnhance


def handleSelectFolder():
    labelSuccess.configure(text="")
    path = filedialog.askdirectory()
    labelSelectedPath.configure(text=path)
    return


def enhanceImages():
    folder = labelSelectedPath.cget("text")
    for count, filename in enumerate(os.listdir(folder)):
        if filename.lower().endswith('.png'):
            try:
                print(f"Handling {filename}...")
                filePath = f"{folder}/{filename}"
                image = Image.open(filePath)
                coloredImage = ImageEnhance.Color(image)
                coloredImage.enhance(2).save(filePath)
                image.close()
                print(f"Complete handling {filename}!")
            except Exception as ex:
                print(f"Ignoring handle {filename} cause by an exception: {ex}")
    labelSuccess.configure(text="Bypass Redbuble AI successfully!")
    return


window = Tk()
window.title("Redbubble Bypasser")
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
btnRename = Button(window, text="Bypass", command=enhanceImages)
btnRename.grid(column=0, row=2)
# Add label successfully
labelSuccess = Label(window, text="", font=("Arial", 10))
labelSuccess.grid(column=0, row=3)

window.mainloop()
