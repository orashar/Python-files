import sys, time
import requests
from bs4 import BeautifulSoup as bs
from PyQt5.QtCore import QThread,pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QApplication,
                             QHBoxLayout , QVBoxLayout,
                             QPushButton, QLabel,
                             QLineEdit, QFileDialog,
                             QTextEdit, QFrame)


class initDownloadingThread(QThread):
    downloadedFileSignal = pyqtSignal(str)
    finishedDownloadSignal = pyqtSignal()

    global filesLinkToDownload


    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        self.filesLinkToDownload = filesLinkToDownload

        self.path = mainApp.path
        print(self.path)
        if self.path.replace(" ", "") == "":
            self.path = "./"
        if self.path[-1] != "/":
            self.path += "/"
    def downloadSelectedFiles(self):

        for self.aChild in self.filesLinkToDownload:
            self.pdfContent = requests.get(self.aChild[-1], stream=True)

            self.filesName = self.path + self.aChild[1] + ".pdf"
            print(self.filesName)
            with open(self.filesName, "wb") as f:
                for chunk in self.pdfContent.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            self.downloadedFileSignal.emit(self.aChild[1])
        self.finishedDownloadSignal.emit()




class collectFilesThread(QThread):
    finished = pyqtSignal()
    collectedFileSignal = pyqtSignal(str)
    global storeRoom
    storeRoom = []

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.mainUrl = mainApp.mainUrl
        self.storeRoom = storeRoom


    def collectLinks(self):
        i = 0
        for self.page in (1, 2):
            self.pageUrl = self.mainUrl + f"?page={self.page}"

            r = requests.get(self.pageUrl)
            print(f"collecting Data from {self.pageUrl}")

            soup = bs(r.content, 'html.parser')
            print("collecting list of files...")

            li = soup.find('ul', {"class": "courses"})

            for self.item in li:
                try:
                    self.collectedFileSignal.emit(self.item.text)

                    i += 1
                    self.storeRoom.append((i, self.item.text, self.item.a.get('href')))
                except:
                    pass
        print(f"collected all {i} files")


class mainApp(QWidget):
    def __init__(self):
        super().__init__()

        global storeRoom
        global filesLinkToDownload

        filesLinkToDownload = []

        self.storeRoom = storeRoom
        self.filesLinkToDownload = filesLinkToDownload
        self.aChild = ()

        self.thread = QThread()

        self.mainFrame = QFrame()
        self.reviewFrame = QFrame()
        self.downloadFrame = QFrame()

        self.handleUI()


    def handleUI(self):
        ## Buttons

        self.browseButton = QPushButton("  Browse  ")
        self.browseButton.released.connect(self.browse)

        self.runButton = QPushButton("  Run  ")
        self.runButton.released.connect(self.initChecking)

        self.reviewListButton = QPushButton("  Review  ")
        self.reviewListButton.released.connect(self.reviewList)
        self.reviewListButton.setEnabled(False)

        self.downloadAllButton = QPushButton("  Download All  ")
        self.downloadAllButton.released.connect(self.downloadAll)
        self.downloadAllButton.setEnabled(False)

        ## Labels

        self.urlLabel = QLabel("Enter Url : ")

        self.locationLabel = QLabel("Enter the location to destination folder : ")

        ## Entry Fields

        self.urlField = QLineEdit()

        self.locationField = QLineEdit()

        self.logField = QTextEdit("Logs:\nhttps://www.studyiq.com/downloads/free-pdfs/ssc-expected-gs-questions-high-level")
        self.logField.setReadOnly(True)

        ## Layouts

        self.hUrl = QHBoxLayout()
        self.hLocation = QHBoxLayout()
        self.hRun = QHBoxLayout()
        self.hLog = QHBoxLayout()

        self.vLogLeft = QVBoxLayout()
        self.vLogRight = QVBoxLayout()
        self.vertical = QVBoxLayout()

        ## Adding Widgets

        self.hUrl.addWidget(self.urlLabel)
        self.hUrl.addWidget(self.urlField)

        self.hLocation.addWidget(self.locationLabel)
        self.hLocation.addWidget(self.locationField)
        self.hLocation.addWidget(self.browseButton)

        self.hRun.addWidget(self.runButton)

        self.vLogLeft.addWidget(self.logField)
        self.vLogRight.addWidget(self.reviewListButton)
        self.vLogRight.addWidget(self.downloadAllButton)

        ## Adding Layouts

        self.hLog.addLayout(self.vLogLeft)
        self.hLog.addLayout(self.vLogRight)

        self.vertical.addLayout(self.hUrl)
        self.vertical.addLayout(self.hLocation)
        self.vertical.addLayout(self.hRun)
        self.vertical.addLayout(self.hLog)

        ## Setting Layout

        self.mainFrame.setLayout(self.vertical)

        self.setWindowTitle("Pdf Downloader")
        self.mainFrame.setGeometry(10, 10, 800, 400)
        self.reviewFrame.setGeometry(10, 10, 800, 400)
        self.downloadFrame.setGeometry(10, 10, 800, 400)

        self.mainFrame.show()


    def browse(self):
        filename = QFileDialog.getExistingDirectory(self, "Select Location")
        self.locationField.setText(filename)


    def reviewList(self):
        self.mainFrame.hide()

        self.reviewFrameMainLayout = QVBoxLayout()


        self.proceedToDownloadButton = QPushButton(" Proceed To Download  ")
        self.proceedToDownloadButton.clicked.connect(self.proceedToDownload)

        self.reviewFrameMainLayout.addWidget(self.proceedToDownloadButton)

        self.addOptionsToReviewFrame()

        self.reviewFrame.setLayout(self.reviewFrameMainLayout)

        self.reviewFrame.show()

    def addOptionsToReviewFrame(self):
        for self.aChild in self.storeRoom:

            self.pdfNameLabel = QLabel(self.aChild[1])

            self.addToQueueButton = QPushButton(f"  Add '{self.aChild[0]}' To Queue  ")
            self.addToQueueButton.clicked.connect(self.addToQueue)

            self.removeFromListButton = QPushButton(f"  Remove '{self.aChild[0]}' From List  ")
            self.removeFromListButton.clicked.connect(self.removeFromList)

            self.reviewFrameLayout = QHBoxLayout()
            self.reviewFrameLayout.addWidget(self.pdfNameLabel)
            self.reviewFrameLayout.addWidget(self.addToQueueButton)
            self.reviewFrameLayout.addWidget(self.removeFromListButton)

            self.reviewFrameMainLayout.addLayout(self.reviewFrameLayout)


    def proceedToDownload(self):

        self.downloadFrameLayout = QVBoxLayout()
        self.downloadFrame.setLayout(self.downloadFrameLayout)

        self.downloadLogFieldText = "  Progress : \n"

        self.downloadLogs = QTextEdit(self.downloadLogFieldText)
        self.downloadLogs.setReadOnly(True)
        self.downloadFrameLayout.addWidget(self.downloadLogs)

        self.reviewFrame.hide()
        self.downloadFrame.show()

        print(f"Downloading {len(self.filesLinkToDownload)} files...")

        self.downloadThread = initDownloadingThread()
        self.dThread = QThread()

        self.downloadThread.moveToThread(self.dThread)
        self.downloadThread.finishedDownloadSignal.connect(self.dThread.quit)
        self.downloadThread.downloadedFileSignal.connect(self.showDownloadLogs)

        self.dThread.started.connect(self.downloadThread.downloadSelectedFiles)
        self.dThread.start()


    def addToQueue(self):
        sender = self.sender()
        self.requestedItemIndex = str(sender.text()).split("'")[1]
        print("added", self.requestedItemIndex)
        for self.aChild in self.storeRoom:
            if self.aChild[0] == int(self.requestedItemIndex):
                self.filesLinkToDownload.append(self.aChild)
                sender.setEnabled(False)

                break


    def removeFromList(self):
        sender = self.sender()
        self.requestedItemIndex = str(sender.text()).split("'")[1]
        print("removed", self.requestedItemIndex)
        for self.aChild in self.filesLinkToDownload:
            if self.aChild[0] == int(self.requestedItemIndex):
                self.filesLinkToDownload.remove(self.aChild)
                sender.setEnabled(False)

                break


    def showDownloadLogs(self, file):

        self.downloadLogFieldText += f"downloaded {file} \n"
        self.downloadLogs.setText(self.downloadLogFieldText)

        print(f"downloaded {file}")


    def downloadAll(self):
        print("downloading of all the files started")


    def initChecking(self):
        mainApp.mainUrl = self.urlField.text()
        mainApp.path = self.locationField.text()
        if self.path == "":
            self.path = "./"
        try:

            r = requests.get(self.mainUrl)

            if r.status_code == 200:
                self.initCollecting()


        except:
            self.logField.setText("Logs:\n!Error Connecting To Provided Url!")


    def initCollecting(self):

        self.collectingThread = collectFilesThread()

        self.collectingThread.moveToThread(self.thread)
        self.collectingThread.finished.connect(self.thread.quit)
        self.collectingThread.collectedFileSignal.connect(self.updateLog)

        self.thread.started.connect(self.collectingThread.collectLinks)
        self.thread.start()

        self.logField.setText("Logs:\nCollecting Data...")


    def updateLog(self, pdfname):
        format = "Logs:\nGot item : " + pdfname
        self.logField.setText(format)
        self.logField.setText("Logs:\nCollected All Files Successfully")
        self.reviewListButton.setEnabled(True)
        self.downloadAllButton.setEnabled(True)




if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = mainApp()

    sys.exit(app.exec_())