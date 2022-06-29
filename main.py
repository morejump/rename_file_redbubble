import threading
from tkinter import *
import uuid
from datetime import datetime


def startGenerateGmail():
    lastGenerate = datetime.now().strftime('%H:%M:%S')
    labelLastTime.config(text=lastGenerate)
    mainMail = entryMainMail.get()

    uniqueString = str(uuid.uuid4()).split("-")[-1]

    text = mainMail.split("@")
    print(text)
    newMail = f"{text[0]}+{uniqueString}@{text[1]}"
    entryGenerateMail.delete(0, END)
    entryGenerateMail.insert(0, newMail)
    return


def processEmail():
    threading.Thread(target=startGenerateGmail).start()
    return


def copyEmail():
    window.clipboard_clear()
    window.clipboard_append(entryGenerateMail.get())
    return


window = Tk()
window.title("Gmail Generator v1.1")
window.geometry("500x130")
# Main mail
labelGmail = Label(window, text="Main Gmail:")
labelGmail.grid(column=0, row=0)
entryMainMail = Entry(window, width=50)
entryMainMail.grid(column=1, row=0)
#  Generate
btnGenerate = Button(window, text="Generate", command=processEmail)
btnGenerate.grid(column=0, row=1)
entryGenerateMail = Entry(window, width=50)
entryGenerateMail.grid(column=1, row=1)
btnCopy = Button(window, text="Copy", command=copyEmail)
btnCopy.grid(column=2, row=1)

labelLastGenerate = Label(window, text="Last generate: ")
labelLastGenerate.grid(column=0, row=2)

labelLastTime = Label(window, text="N/A")
labelLastTime.grid(column=1, row=2)

window.mainloop()
