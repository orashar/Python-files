import requests
from bs4 import BeautifulSoup
import tkinter as tk
import time, os, sys


def downloadPdf(burlget, lcnget):
    location = lcnget.get()
    baseurl = burlget.get()
    if location == '':
        location = "./"
    if baseurl == '':
        label.configure(text="url is required to proceed!!\n restarting in 2 seconds")
        python = sys.executable
        root.after(2000, lambda: os.execl(python, python, *sys.argv))



    else:
        filesNO = 0

    
        for page in (1, 2):
    
            print(f"collecting data from page {page}")
            properBaseUrl = baseurl + "?page=" + str(page)
    
            r = requests.get(properBaseUrl)
    
            print("reading ", properBaseUrl, "...")
    
            soup = BeautifulSoup(r.content, 'html5lib')
    
            print("collecting list of files...")
    
            li = soup.find('ul', {"class": "courses"})
    
    
            for item in li.findAll('li'):
                print("trying ", item.text)
                pdf = item.a.get('href')
                pdfContent = requests.get(pdf, stream=True)
                pdfName = location + pdf.split('/')[-1] + ".pdf"
    
                print(f"downloading {pdf.split('/')[-1]}...")
    
                filesNO += 1
                part = 0
                print(filesNO)
    
                with open(pdfName, "wb") as p:
                    for chunk in pdfContent.iter_content(chunk_size=1024):
                        if chunk:
                            p.write(chunk)

        label.configure(text=f"downloaded {filesNO} files at location {location}")


root = tk.Tk()
root.geometry('500x500')
root.title('PDF Downloader')

label = tk.Label(root, text='')
label.pack(side="bottom")

tk.Label(root, text="Enter url: ").pack()
baseurl = tk.StringVar()
tk.Entry(root, textvariable = baseurl).pack()

tk.Label(root, text="Enter the destination  for file: ").pack()
location = tk.StringVar()
tk.Entry(root, textvariable = location).pack()

tk.Button(root, text="   RUN   ", command = lambda: downloadPdf(baseurl, location)).pack()



tk.mainloop()