import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
import qdarkgraystyle

class MP3Player(QWidget):
    def __init__(self):
        super().__init__()

        self.state = "Play"
        self.playlist = []
        self.position = 0
        self.index = ""

        self.init_ui()


    def init_ui(self):
        vb = QVBoxLayout()
        self.setLayout(vb)
        vb.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Wanoid MP3 Player 2022")
        self.label.setFont(QFont("Calibri", 20))
        self.label.setAlignment(Qt.AlignCenter)
        vb.addWidget(self.label)

        hb = QHBoxLayout()
        vb.addLayout(hb)

        font = QFont("Calibri", 14)
        self.skipbackwardbtn = QPushButton()
        self.skipbackwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        hb.addWidget(self.skipbackwardbtn)
        self.backwardbtn = QPushButton()
        self.backwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardbtn.setFont(font)
        hb.addWidget(self.backwardbtn)
        self.playbtn = QPushButton("Play")
        self.playbtn.setEnabled(False)
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbtn.setFont(font)
        hb.addWidget(self.playbtn)
        self.forwardbtn = QPushButton()
        self.forwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardbtn.setFont(font)
        hb.addWidget(self.forwardbtn)
        self.skipforwardbtn = QPushButton()
        self.skipforwardbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        hb.addWidget(self.skipforwardbtn)

        hb2 = QHBoxLayout()
        vb.addLayout(hb2)

        self.openfilebtn = QPushButton()
        self.openfilebtn.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.openfilebtn.setFont(font)
        hb2.addWidget(self.openfilebtn)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
        hb2.addWidget(self.slider)

        self.songlist = QListWidget()
        vb.addWidget(self.songlist)

        self.toolbar = QToolBar()
        vb.addWidget(self.toolbar)

        self.openfileaction = QAction()
        self.openfileaction.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.openfileaction.setFont(font)
        self.openfileaction.triggered.connect(self.open_mp3_file)
        self.toolbar.addAction(self.openfileaction)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        self.volumedown = QAction("-")
        self.volumedown.setFont(font)
        self.toolbar.addAction(self.volumedown)
        self.volumeup = QAction("+")
        self.volumeup.setFont(font)
        self.toolbar.addAction(self.volumeup)
        self.space = QWidget()
        self.space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(self.space)
        self.speaker = QAction()
        self.speaker.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.toolbar.addAction(self.speaker)
        self.slider_vl = QSlider(Qt.Horizontal)
        self.toolbar.addWidget(self.slider_vl)

        self.player = QMediaPlayer()

        self.openfilebtn.clicked.connect(self.open_mp3_file)
        self.playbtn.clicked.connect(self.play_mp3)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.backwardbtn.clicked.connect(self.move_backward)
        self.forwardbtn.clicked.connect(self.move_forward)
        self.songlist.clicked.connect(self.set_state)
        self.songlist.doubleClicked.connect(self.play_mp3)
        self.skipbackwardbtn.clicked.connect(self.skip_backward)
        self.skipforwardbtn.clicked.connect(self.skip_forward)


    def open_mp3_file(self):
        file_name =QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open Files", os.getenv("HOME"))
        self.song = names[0]
        self.songlist.addItems(self.song)

    def set_state(self):
        self.playbtn.setEnabled(True)
        self.state = "Play"
        self.playbtn.setText("Play")
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def play_mp3(self):
        if self.state == "Play":
            self.playbtn.setText("Pause")
            self.state = "Pause"
            path = self.songlist.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.index = self.songlist.currentRow().__index__()
            self.player.setPosition(self.position)
            self.playlist.append(path)
            if len(self.playlist) > 2:
                self.playlist.pop(0)
            if self.songlist.currentItem().text() != self.playlist[0]:
                self.position = 0
                self.player.setPosition(self.position)
            self.player.play()
        else: 
            self.playbtn.setText("Play")
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused

    def skip_backward(self):
        self.state = "Play"
        try:
            self.songlist.setCurrentRow(self.index - 1)
            self.play_mp3()
        except:
            pass

    def skip_forward(self):
        self.state = "Play"
        try:
            self.songlist.setCurrentRow(self.index + 1)
            self.play_mp3()
        except:
            pass

    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)
        duration = self.player.duration()
        Value = self.slider.value()
        if Value == duration:
            self.state = "Play"
            self.play_mp3()

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def state_changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def move_forward(self):
        self.player.setPosition(int(self.player.position()) + 2000)

    def move_backward(self):
        self.player.setPosition(int(self.player.position()) - 2000)



def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    gui = MP3Player()
    gui.setWindowTitle("MP3 Player 0.1 Beta Version 2022")
    gui.setWindowIcon(QIcon("mp3player.png"))
    gui.setGeometry(600,200,600,700)
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()