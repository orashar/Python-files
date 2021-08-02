import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QFileDialog,
                             QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy,
                             QSlider, QStyle, QAction,
                             QVBoxLayout, QWidget)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon


class VideoMain(QMainWindow):

    def __init__(self, parent=None):
        super(VideoMain, self).__init__(parent)

        self.setWindowTitle("VM Player")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        ## play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.playVideo)

        ## skip button
        self.seekLeft = QPushButton()
        self.seekLeft.setEnabled(False)
        self.seekLeft.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.seekLeft.clicked.connect(self.seekBackward)

        self.seekRight = QPushButton()
        self.seekRight.setEnabled(False)
        self.seekRight.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.seekRight.clicked.connect(self.seekForward)

        ## volume button and slider
        self.volumeButton = QPushButton()
        self.volumeButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeButton.clicked.connect(self.muteUnmute)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.valueChanged.connect(self.changeVolume)

        ## seek slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        ## error label
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        ### actions

        ## open action
        openAction = QAction('&Open', self)
        openAction.setShortcut('CTRL+O')
        openAction.setStatusTip('Open Video')
        openAction.triggered.connect(self.openFile)

        ## exit action
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        ### create menubar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')

        ### add actions in menubar
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        ### create a widget for window content
        wid = QWidget(self)
        self.setCentralWidget(wid)

        ### create layout
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.seekLeft)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.seekRight)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeButton)
        controlLayout.addWidget(self.volumeSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        ## set widget to contain window contents
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)


    def playVideo(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def seekBackward(self, position):
        pass

    def seekForward(self):
        pass

    def muteUnmute(self):
        if self.volumeSlider.value() != 0:
            self.changeVolume(0)
            self.volumeButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.changeVolume(70)
            self.volumeButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.seekRight.setEnabled(True)
            self.seekLeft.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def mediaStateChanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def changeVolume(self, volume):
        print(volume)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("ERror: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoMain()
    player.resize(1500, 800)
    player.show()
    sys.exit(app.exec_())