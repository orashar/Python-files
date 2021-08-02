import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
import time, os, sys


class Display(tk.Frame):
    def __init__(self, parent):
        global root
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.completed = 0
        self.initUI()


    def initUI(self):

        ## log label

        self.logTitleLabel = tk.Label(root, text='LOGS: ', bg = "skyblue")
        self.logTitleLabel.grid(row = 3, column = 0, columnspan=3)
        self.logLabel = tk.Label(root, text="Enter Url and select destination. Then press 'Run'", bg="skyblue")
        self.logLabel.grid(row=4, column=0, columnspan=3)

        ## main widgets

        self.urlLabel = tk.Label(root, text="Enter url : ")
        self.urlLabel.grid(row = 0, column = 0)
        self.url = tk.StringVar()
        tk.Entry(root, textvariable=self.url).grid(row = 0, column = 1)

        self.locationLabel = tk.Label(root, text="Enter the destination  for files : ")
        self.locationLabel.grid(row = 1, column = 0)
        self.location = tk.StringVar()
        tk.Entry(root, textvariable=self.location).grid(row = 1, column = 1)
        self.browseButton = tk.Button(root, text="  Browse  ", command=self.browse)
        self.browseButton.grid(row = 1, column = 2)

        self.runButton = tk.Button(root, text="   RUN   ", command=self.initDownloading)
        self.runButton.grid(row = 2, column = 1)

    def initDownloading(self):
        self.path = self.location.get()
        self.mainurl = self.url.get()
        if self.path == '':
            self.path = "./"
        if self.mainurl == '':
            self.logLabel.configure(text="url is required to proceed!!\n Try agian...")

        else:
            try:
                self.r = requests.get(self.mainurl)

                if self.r.status_code == 200:

                    self.logLabel.configure(text="please wait..")
                    self.parent.update()
                    time.sleep(0.5)
                    self.logLabel.configure(text="Starting Download...")
                    self.parent.update()

                    for self.page in (1, 2):

                        self.parent.update()
                        print(f"collecting data from page {self.page}")

                        properBaseUrl = self.mainurl + "?page=" + str(self.page)
                        print(properBaseUrl)
                        self.req = requests.get(properBaseUrl)

                        print("reading ", properBaseUrl, "...")

                        soup = BeautifulSoup(self.req.content, 'html.parser')

                        print("collecting list of files...")

                        li = soup.find('ul', {"class": "courses"})

                        for self.item in li.findAll('li'):

                            self.logLabel.configure(text=f"Collecting data from {self.item.text}")
                            self.parent.update()
                            print("trying ", self.item.text)

                            pdf = self.item.a.get('href')

                            pdfContent = requests.get(pdf, stream=True)
                            if self.path[-1] == "/":
                                self.pdfName = self.path + self.item.text + ".pdf"
                            else:
                                self.pdfName = self.path + "/" + self.item.text + ".pdf"

                                                
                            self.logLabel.configure(text=f"Downloading {self.pdfName}")
                            self.parent.update()
                            print(f"downloading {self.pdfName}...")

                            with open(self.pdfName, "wb") as p:
                                for chunk in pdfContent.iter_content(chunk_size=1024):
                                    if chunk:
                                        p.write(chunk)
                            self.completed += 1
                            self.logLabel.configure(text=f"Download complete : {self.pdfName}")
                            self.parent.update()


                    self.logLabel.configure(text=f"Task Completed Successfully ^_^\nTotal {self.completed} files  Downloaded at location {self.path}")


                else:
                    self.logLabel.configure(text="!!Currently facing Problem connecting to requested url!! Give it another Try...")

            except:
                self.logLabel.configure(text="!!Currently facing Problem connecting to requested url!! Give it another Try...")

    def browse(self):
        global location
        fileName = filedialog.askdirectory(parent=root)
        self.location.set(fileName)
        print(location.get())


def main():
    global root
    root = tk.Tk()
    root.geometry('700x500')
    root.title('PDF Downloader')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    Display(root)
    root.mainloop()


if __name__ == '__main__':
    main()
