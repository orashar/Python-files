from tkinter import *
from tkinter import filedialog

root = Tk()

def browse():
    global path
    fileName = filedialog.askdirectory()
    path.set(fileName)
    print(path.get())


path = StringVar()
label = Label(root, text="select path").pack()
Entry(root, textvariable=path).pack()
button = Button(root, text="browse", command=browse).pack()

mainloop()

