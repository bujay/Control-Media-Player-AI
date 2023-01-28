import os
import sys
import pysrt
import datetime
import webbrowser
import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import image_file
from tkinter import *
from tkinter import messagebox as mbox
from tkinter.messagebox import askokcancel

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QUrl, QTime, QTimer, QThread, pyqtSlot
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QFileDialog, QStyle, QLabel, QAction, \
    QSizePolicy, QWidget, QGridLayout, QLineEdit


class LisensiKey(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Lisensi Key Pemutar Media'
        self.left = 500
        self.top = 150
        self.width = 520
        self.height = 75
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        self.label = QLabel(self)
        self.label.setText('Lisensi Key: ')
        self.label.move(30, 30)

        self.textbox = QLineEdit(self)
        self.textbox.move(120, 20)
        self.textbox.resize(280, 30)

        self.lisensiButton = QPushButton('Cek Lisensi Key', self)
        self.lisensiButton.move(420, 25)
        # self.lisensiButton.setShortcut(QKeySequence("Ctrl+L"))  # menambahkan shortcut Ctrl+L
        self.lisensiButton.clicked.connect(self.cek_lisensi_key)

        self.show()

    @pyqtSlot()
    def cek_lisensi_key(self):
        lisensi_key = 'Ahmad Bujai Rimi', 'UEU Teknik Informatika 2019'
        #if self.textbox.text() in lisensi_key:
        if self.textbox.text() == lisensi_key[0] or self.textbox.text() == lisensi_key[1]:
            mbox.showinfo('Lisensi Key', 'Lisensi Key sudah masuk')
            self.close()
            # Masuk Ke Class Window(QMainWindow)
            self.window = Window()
            self.window.show()
        else:
            mbox.showinfo('Lisensi Key', 'Lisensi Key belum masuk')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pemutar Media Sederhana (Coded By: Enjay)")
        self.setGeometry(100, 100, 800, 600)
        #self.setStyleSheet("background-color: Black; color: red; font-weight: bold; border: 2px solid red; border-radius: 10px;"
        #                   "padding: 5px; border-width: 2px; selection-color: black;selection-background-color: red;")

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

        # Create Media Player Object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create Video Widget Object
        videoWidget = QVideoWidget()

        # Create MenuBar
        main_menu = self.menuBar()
        main_menu.setStyleSheet("background-color: Black; color: red; font-weight: bold; border-radius: 10px; selection-color: black; selection-background-color: red;"
                                "border: 2px solid red; padding: 2px; border-width: 2px; border-style: outset;")

        file_menu = main_menu.addMenu("Dokumen")
        tools_menu = main_menu.addMenu("Alat")
        ai_menu = main_menu.addMenu("AI")
        view_menu = main_menu.addMenu("View")
        help_menu = main_menu.addMenu("Bantuan")

        # Create Open Action
        open_file_action = QAction("Buka File", self)
        open_file_action.setShortcut(QKeySequence("Ctrl+O"))
        open_file_action.setIcon(QIcon("icons/open.png"))
        open_file_action.triggered.connect(self.open_file)

        # Create Exit Action
        exit_action = QAction("Keluar", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setIcon(QIcon("icons/exit.png"))
        exit_action.triggered.connect(self.exit_app)

        # Create Open Subtitle Action
        open_subtitle_action = QAction("Buka Subtitle", self)
        open_subtitle_action.setShortcut(QKeySequence("Ctrl+S"))
        open_subtitle_action.setIcon(QIcon("icons/subtitle.png"))
        open_subtitle_action.triggered.connect(self.open_subtitle)

        # Sub Menu Tools
        speed_menu = tools_menu.addMenu("Kecepatan Video")
        speed_menu.addAction("Lambat", self.slow_video)
        speed_menu.addAction("Normal", self.normal_video)
        speed_menu.addAction("Cepat", self.fast_video)

        # repeat menu
        repeat_menu = tools_menu.addMenu("Ulangi Video")
        repeat_menu.addAction("Aktifkan", self.video_auto_on)
        repeat_menu.addAction("Matikan", self.video_auto_off)

        # Create Sleep Time
        sleep_time_menu = tools_menu.addMenu("Waktu Tidur")
        sleep_time_menu.addAction("1 Menit", self.sleep_time_1_minute)
        sleep_time_menu.addAction("15 Menit", self.sleep_time_15_minute)
        sleep_time_menu.addAction("30 Menit", self.sleep_time_30_minute)
        sleep_time_menu.addAction("45 Menit", self.sleep_time_45_minute)
        sleep_time_menu.addAction("1 Jam", self.sleep_time_60_minute)
        sleep_time_menu.addAction("Matikan", self.timer_stop)

        # Create ScreenShot Action
        screenshot_action = QAction("Ambil Gambar", self)
        screenshot_action.setShortcut(QKeySequence("Ctrl+P"))
        screenshot_action.setIcon(QIcon("icons/screenshot.png"))
        screenshot_action.triggered.connect(self.screen)

        # Create Hand Gesture Action
        hand_gesture_action = QAction("AI Gerakan Tangan", self)
        hand_gesture_action.setShortcut(QKeySequence("Ctrl+G"))
        hand_gesture_action.setIcon(QIcon("icons/hand.png"))
        hand_gesture_action.triggered.connect(self.hand_gesture)

        # Create Objek Video Action
        objek_video_action = QAction("AI Objek Video", self)
        objek_video_action.setShortcut(QKeySequence("Ctrl+V"))
        objek_video_action.setIcon(QIcon("icons/objek.png"))
        objek_video_action.triggered.connect(self.deteksi_objek_video)

        # Create Objek Kamera Action
        objek_kamera_action = QAction("AI Objek Kamera", self)
        objek_kamera_action.setShortcut(QKeySequence("Ctrl+K"))
        objek_kamera_action.setIcon(QIcon("icons/objek.png"))
        objek_kamera_action.triggered.connect(self.deteksi_objek_kamera)

        # Sub Menu Time Watch
        time_watch_menu = view_menu.addMenu("Jam Digital")
        time_watch_menu.addAction("Tampilkan", self.showTimeWatch)
        time_watch_menu.addAction("Sembuyikan", self.hideTimeWatch)

        # Sub Speed Effect Sound
        sound_efect_menu = view_menu.addMenu("Efek Suara")
        sound_efect_menu.addAction("Tampilkan", self.show_speed)
        sound_efect_menu.addAction("Sembuyikan", self.hide_speed)

        # Sub Menu Subtitle
        subtitle_menu = view_menu.addMenu("Subtitle")
        subtitle_menu.addAction("Tampilkan", self.show_subtitle)
        subtitle_menu.addAction("Sembuyikan", self.hide_subtitle)

        # Create MyGithub Action
        mygithub_action = QAction("Github Saya", self)
        mygithub_action.setShortcut(QKeySequence("Ctrl+G"))
        mygithub_action.setIcon(QIcon("icons/about.png"))
        mygithub_action.triggered.connect(self.mygithub_app)

        # Create About AI Hand Gesture Action
        about_ai_hand_gesture_action = QAction("Penggunaan AI Gerakan Tangan", self)
        about_ai_hand_gesture_action.setShortcut(QKeySequence("Ctrl+A"))
        about_ai_hand_gesture_action.setIcon(QIcon("icons/about.png"))
        about_ai_hand_gesture_action.triggered.connect(self.about_ai_hand_gesture)

        # Create update Action
        update_action = QAction("Fitur Tebaru", self)
        update_action.setShortcut(QKeySequence("Ctrl+T"))
        update_action.setIcon(QIcon("icons/about.png"))
        update_action.triggered.connect(self.update_app)

        # Create About Action
        about_action = QAction("Tentang Aplikasi", self)
        about_action.setShortcut(QKeySequence("Ctrl+A"))
        about_action.setIcon(QIcon("icons/about.png"))
        about_action.triggered.connect(self.about_app)

        # Create Action
        file_menu.addAction(open_file_action)
        file_menu.addAction(open_subtitle_action)
        # file_menu.addSeparator()
        file_menu.addAction(exit_action)
        tools_menu.addAction(screenshot_action)
        ai_menu.addAction(hand_gesture_action)
        ai_menu.addAction(objek_video_action)
        ai_menu.addAction(objek_kamera_action)
        help_menu.addAction(mygithub_action)
        # help_menu.addSeparator()
        help_menu.addAction(about_ai_hand_gesture_action)
        help_menu.addAction(update_action)
        help_menu.addAction(about_action)

        self.openBtn = QPushButton('Buka Video/Musik')
        self.openBtn.clicked.connect(self.open_file)
        self.openBtn.setStyleSheet("background-color: white; color: black; font-size: 13px; border-style: outset; "
                                   "border-width: 2px; border-radius: 10px; min-width: 3em; padding: 3px;")

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        self.playBtn.setShortcut(QKeySequence("Space"))
        self.playBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.stopBtn = QPushButton()
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_video)
        self.stopBtn.setShortcut(QKeySequence("S"))
        self.stopBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.muteBtn = QPushButton()
        self.muteBtn.setEnabled(False)
        self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.muteBtn.clicked.connect(self.mute_video)
        self.muteBtn.setShortcut(QKeySequence("M"))
        self.muteBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.forwardButton = QPushButton()
        self.forwardButton.setEnabled(False)
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardButton.clicked.connect(self.forward_video)
        self.forwardButton.setShortcut(QKeySequence("Right"))
        self.forwardButton.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.backwardButton = QPushButton()
        self.backwardButton.setEnabled(False)
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardButton.clicked.connect(self.backward_video)
        self.backwardButton.setShortcut(QKeySequence("Left"))
        self.backwardButton.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        self.fullscreenBtn = QPushButton()
        self.fullscreenBtn.setEnabled(False)
        self.fullscreenBtn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreenBtn.clicked.connect(self.fullscreen_video)
        self.fullscreenBtn.setShortcut(QKeySequence("F"))
        self.fullscreenBtn.setStyleSheet("color: red; border-style: outset; border-width: 2px; border-radius: 10px;"
                                              "min-width: 3em; padding: 3px;")

        # Create Slider Video Position
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create Slider Volume Position
        self.sliderVolume = QSlider(QtCore.Qt.Horizontal)
        self.sliderVolume.setRange(0, 200)
        self.sliderVolume.setValue(100)
        # Membuat up dan down volume dengan tombol panah atas dan bawah
        self.sliderVolume.valueChanged.connect(self.set_volume)
        self.sliderVolume.sliderMoved.connect(self.set_volume)

        # Create Speed Slider
        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setRange(0, 200)
        self.speedSlider.setValue(100)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(10)
        self.speedSlider.valueChanged.connect(self.set_speed)

        # Create Speed Label
        self.speedLabel = QLabel()
        self.speedLabel.setText('100%')
        self.speedLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.speedLabel.setStyleSheet("color: red; font-size: 12px;")

        # Create Label
        self.label = QLabel()
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Create Watch Digital Clock
        self.labelWatch = QLabel()
        self.labelWatch.setAlignment(Qt.AlignRight)
        self.labelWatch.setFont(QFont("Times New Roman", 14))
        self.labelWatch.setStyleSheet("color:Red; font-weight: bold")
        self.labelWatch.setText(self.timeWatch())
        self.labelWatch.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_watch)
        self.timer.start(1000)

        # label volume
        self.labelVolume = QtWidgets.QLabel()
        self.labelVolume.setText("Volume :")
        self.labelVolume.setStyleSheet("color: white;")

        # label position
        self.labelPosition = QtWidgets.QLabel()
        self.labelPosition.setText("Position :")
        self.labelPosition.setStyleSheet("color: white;")

        self.elapsed_time_label = QLabel("00:00:00")
        self.elapsed_time_label.setStyleSheet("color: white;")

        self.remaining_time_label = QLabel("00:00:00")
        self.remaining_time_label.setStyleSheet("color: white;")

        # Membuat label untuk menampilkan nama file
        self.labelFile = QLabel()
        self.labelFile.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        self.labelFile.setStyleSheet("color: white; font-size: 15px;")

        # Membuat Label untuk menampilkan subtitle video yang sedang diputar format .srt
        self.labelSubtitle = QLabel()
        self.labelSubtitle.setAlignment(Qt.AlignCenter)
        self.labelSubtitle.setFont(QFont("Times New Roman", 14))
        self.labelSubtitle.setStyleSheet("color:Red; font-weight: bold")
        self.labelSubtitle.setText("")
        # label size subtitle 600
        self.labelSubtitle.setFixedWidth(600)
        # Jika Text Subtitle melebihi label maka akan di scroll
        self.labelSubtitle.setWordWrap(True)
        self.labelSubtitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.position = 0
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        hboxLayout = QtWidgets.QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        #hboxLayout.addWidget(self.openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)
        hboxLayout.addWidget(self.muteBtn)
        hboxLayout.addWidget(self.backwardButton)
        hboxLayout.addWidget(self.forwardButton)
        hboxLayout.addWidget(self.fullscreenBtn)

        hboxLayoutVolume = QtWidgets.QHBoxLayout()
        hboxLayoutVolume.setContentsMargins(0, 0, 0, 0)
        hboxLayoutVolume.addWidget(self.labelVolume)
        hboxLayoutVolume.addWidget(self.sliderVolume)

        hboxLayoutPosition = QtWidgets.QHBoxLayout()
        hboxLayoutPosition.setContentsMargins(0, 0, 0, 0)
        hboxLayoutPosition.addWidget(self.labelPosition)
        hboxLayoutPosition.addWidget(self.slider)

        hboxLayoutTime = QtWidgets.QHBoxLayout()
        hboxLayoutTime.setContentsMargins(0, 0, 0, 0)
        hboxLayoutTime.addWidget(self.elapsed_time_label, 0, Qt.AlignLeft)
        hboxLayoutTime.addWidget(self.remaining_time_label, 1, Qt.AlignRight)
        hboxLayoutTime.addWidget(self.label)

        hboxLayoutSpeed = QtWidgets.QHBoxLayout()
        hboxLayoutSpeed.setContentsMargins(0, 0, 0, 0)
        hboxLayoutSpeed.addWidget(self.speedSlider)
        hboxLayoutSpeed.addWidget(self.speedLabel)

        hboxLayoutFileName = QtWidgets.QHBoxLayout()
        hboxLayoutFileName.setContentsMargins(0, 0, 0, 0)
        hboxLayoutFileName.addWidget(self.labelFile)

        hboxLayoutSubtitle = QtWidgets.QHBoxLayout()
        hboxLayoutSubtitle.setContentsMargins(0, 0, 0, 0)
        hboxLayoutSubtitle.addWidget(self.labelSubtitle)

        vboxLayout = QtWidgets.QVBoxLayout()
        vboxLayout.addWidget(self.labelWatch)
        vboxLayout.addWidget(videoWidget)
        vboxLayout.addLayout(hboxLayoutSubtitle)
        vboxLayout.addLayout(hboxLayoutFileName)
        vboxLayout.addLayout(hboxLayoutTime)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addLayout(hboxLayoutPosition)
        vboxLayout.addLayout(hboxLayoutVolume)
        vboxLayout.addLayout(hboxLayoutSpeed)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)

        # Set Speed Slider
        self.speedSlider.hide()

        # Set Speed Label
        self.speedLabel.hide()

        # set Time Watch Show
        self.labelWatch.hide()

        # Set Subtitle
        self.labelSubtitle.hide()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Buka Video/Musik", os.curdir, "Video Files (*.avi *.mp3)")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.muteBtn.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.fullscreenBtn.setEnabled(True)
            # Menampilkan nama file yang dipilih tidak termasuk path
            self.labelFile.setText(os.path.basename(filename))

    # Buka Subtitle File .srt
    def open_subtitle(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Buka Subtitle", os.curdir, "Subtitle Files (*.srt)")

        if filename != '':
            self.subtitle = pysrt.open(filename)
            # Subtitle position in seconds (float)
            self.subtitle_position = 0
            # Subtitle index
            self.subtitle_index = 0
            # Subtitle text
            self.subtitle_text = ""
            # Subtitle timer
            self.subtitle_timer = QTimer()
            self.subtitle_timer.timeout.connect(self.update_subtitle)
            self.subtitle_timer.start(1000)

    def update_subtitle(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.subtitle_position = self.mediaPlayer.position() / 1000
            if self.subtitle_index < len(self.subtitle):
                if self.subtitle_position >= self.subtitle[self.subtitle_index].start.minutes * 60 + self.subtitle[self.subtitle_index].start.seconds + self.subtitle[self.subtitle_index].start.milliseconds / 1000:
                    self.subtitle_text = self.subtitle[self.subtitle_index].text
                    self.labelSubtitle.setText(self.subtitle_text)
                    self.subtitle_index += 1
                    # Jika video sudah selesai dan durasi video ulang dari awal maka subtitle akan di reset ke awal
                    if self.subtitle_index == len(self.subtitle):
                        self.subtitle_index = 0
                        self.subtitle_position = 0
                        self.subtitle_text = ""
                        self.labelSubtitle.setText(self.subtitle_text)
        else:
            self.labelSubtitle.setText("")

    def show_subtitle(self):
        self.labelSubtitle.show()

    def hide_subtitle(self):
        self.labelSubtitle.hide()

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def stop_video(self):
        self.mediaPlayer.stop()

    def mute_video(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.mediaPlayer.setMuted(True)
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))

    def forward_video(self):
        self.mediaPlayer.setPosition(self.position + 5000)

    def backward_video(self):
        self.mediaPlayer.setPosition(self.position - 5000)

    def fullscreen_video(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)
        # Jika volume 0 maka icon mute akan muncul
        if volume == 0:
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        else:
            self.muteBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))

    def position_changed(self, position):
        self.slider.setValue(position)
        self.position = position

        elapsed_time = QTime(0, 0, 0)
        elapsed_time = elapsed_time.addMSecs(position)
        elapsed_time_string = elapsed_time.toString("hh:mm:ss")
        self.elapsed_time_label.setText(elapsed_time_string)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

        remaining_time = QTime(0, 0, 0)
        remaining_time = remaining_time.addMSecs(duration)
        remaining_time_string = remaining_time.toString("hh:mm:ss")
        self.remaining_time_label.setText(remaining_time_string)

    def slow_video(self):
        self.mediaPlayer.setPlaybackRate(0.5)

    def normal_video(self):
        self.mediaPlayer.setPlaybackRate(1.0)

    def fast_video(self):
        self.mediaPlayer.setPlaybackRate(2.0)

    def set_speed(self, speed):
        self.speedLabel.setText(str(speed) + '%')
        self.mediaPlayer.setPlaybackRate(speed / 100)

    def show_speed(self):
        self.speedSlider.show()
        self.speedLabel.show()

    def hide_speed(self):
        self.speedSlider.hide()
        self.speedLabel.hide()

    def exit_app(self):
        ans = askokcancel('Keluar', "Anda Yakin Ingin Keluar?")  # menampilkan kotak konfirmasi
        if ans:
            self.close()

    def timeWatch(self):
        time = datetime.datetime.now()
        return time.strftime("Waktu Jakarta: " + "%H:%M:%S")

    def showTimeWatch(self):
        self.labelWatch.show()
        self.labelWatch.setText(self.timeWatch())

    def hideTimeWatch(self):
        self.labelWatch.hide()

    def run_watch(self):
        self.labelWatch.setText(self.timeWatch())

    def sleep_time_1_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(1 * 60000)

    def sleep_time_15_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(15 * 60000)

    def sleep_time_30_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(30 * 60000)

    def sleep_time_45_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(45 * 60000)

    def sleep_time_60_minute(self):
        self.sleepTimer = QTimer()
        self.sleepTimer.setSingleShot(True)
        self.sleepTimer.timeout.connect(self.sleep_video)
        self.sleepTimer.start(60 * 60000)

    def sleep_video(self):
        self.mediaPlayer.pause()
        ans = askokcancel('Waktu Tidur Sudah Habis', "Apakah Anda Ingin Keluar?")  # menampilkan kotak konfirmasi
        if ans:
            self.close()

    # membuat fungsi untuk mengulangi video otomatis jika sudah durasi video sudah selesai
    def video_auto_on(self):
        self.mediaPlayer.positionChanged.connect(self.video_on)

    def video_on(self, position):
        if self.mediaPlayer.duration() - position < 1000:
            self.mediaPlayer.setPosition(0)

    # membuat fungsi untuk mematikan video otomatis
    def video_auto_off(self):
        self.mediaPlayer.positionChanged.connect(self.video_off)

    def video_off(self, position):
        if self.mediaPlayer.duration() - position < 1000:
            self.play_video()

    def timer_stop(self):
        self.sleepTimer.stop()

    # membuat fungsi untuk menghubungkan class screen
    def screen(self):
        self.screen = screen()
        self.screen.show()

    # membuat fungsi untuk menghubungkan class handGesture
    def hand_gesture(self):
        self.gerakanTangan = handGesture()
        self.gerakanTangan.show()

    def deteksi_objek_video(self):
        self.DeteksiObjekVideo = ObjectDetectionVideo()
        self.DeteksiObjekVideo.show()

    def deteksi_objek_kamera(self):
        self.DeteksiObjekCamera = ObjectDetectionCamera()
        self.DeteksiObjekCamera.show()

    def mygithub_app(self):
        webbrowser.open_new(r"https://github.com/bujay")  # pergi ke Github saya

    def about_app(self):
        mbox.showinfo("Pemutar Media Sederhana", "Media Player (Final Version)\n"
                                              "Versi: 1.0.12\n"
                                              "Data Lilis: 09-09-2022\n""Format: Avi, Mp3\n""OS: Windows 7,8,10,11\n\n"
                                              "Developer: Ahmad Bujay Rimi | Enjay Studio\n""Teknik Informatika, Universitas Esa Unggul")

    def about_ai_hand_gesture(self):
        mbox.showinfo("Penggunaan AI Pergerakan Tangan (Tahap Pengembang)", "Angkat tangan ke arah kamera dan sesuaikan jari anda"
                                                                                         "\ndengan jari yang ada di layar untuk mengontrol media player.\n"
                                                                                         "Berawal dari jari telunjuk, jari tengah, jari manis, jari kelingking, dan jari kecil.\n\n"
                                                                                         "- Jari Telunjuk (1) = play/pause\n"
                                                                                         "- Jari Tengah (2) = mute\n"
                                                                                         "- Jari Manis (3) = backward\n"
                                                                                         "- Jari Kelingking (4) = forward\n"
                                                                                         "- Jari Kecil/Ibu Jari (5) = fullscreen\n\n"
                                                                                         "Developer: Ahmad Bujay Rimi | Enjay Studio\n""Teknik Informatika, Universitas Esa Unggul")

    def update_app(self):
        mbox.showinfo("Fitur Terbaru Versi: 1.0.12", "- Fitur MenuBar\n" "- Durasi Video\n" "- Penambahan Fitur Borderless\n"
                                                    "- Memindahkan Open File ke MenuBar\n" "- Menambahkan Fitur Efek Suara Dan Kecepatan Video\n" 
                                                    "- Menambahkan Fitur Waktu Jakarta\n""- Menambahkan Pengaturan Waktu Tidur\n"
                                                    "- Menambahkan Fitur Auto Repeat Video\n" "- Menambahkan Fitur FileName\n"
                                                    "- Memindahkan Waktu Jam Ke MenuBar\n" "- Menambahkan Fitur Subtitle"
                                                    "- Bug Fix Subtitle\n" "- Menambahkan Fitur ScreenShot\n" "- Menambahkan Fitur Hand Gesture\n"
                                                    "- Menambahkan Fitur Deteksi Objek Video\n""- Menambahkan Fitur Deteksi Objek Kamera\n")


class screen(QWidget):
    def __init__(self, parent=None):
        super(screen, self).__init__()
        self.preview_screen = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        print(QApplication.screens())
        self.settings()
        self.create_widgets()
        self.set_layout()

    def settings(self):
        self.resize(570, 320)
        self.setWindowTitle("Gambar Layar ScreenShot")
        self.setWindowIcon(QtGui.QIcon(':/Logo.png'))

    def create_widgets(self):
        self.img_preview = QLabel()
        self.img_preview.setPixmap(self.preview_screen.scaled(550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.btn_save_screenshot = QPushButton("Simpan screenshot")
        self.btn_new_screenshot = QPushButton("Keluar")

        # signals connections
        self.btn_save_screenshot.clicked.connect(self.save_screenshot)
        self.btn_new_screenshot.clicked.connect(self.new_screenshot)

    def set_layout(self):
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.img_preview, 0, 0, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.btn_save_screenshot, 2, 0, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.btn_new_screenshot, 2, 0, alignment=Qt.AlignRight)
        self.setLayout(self.layout)

    def save_screenshot(self):
        img, _ = QFileDialog.getSaveFileName(self, "Menyimpan File",
                                             filter="PNG(*.png);; JPEG(*.jpg)")
        if img[-3:] == "png":
            self.preview_screen.save(img, "png")
        elif img[-3:] == "jpg":
            self.preview_screen.save(img, "jpg")

    def new_screenshot(self):
        self.close()


class handGesture(QThread):
    def __init__(self, parent=None):
        super(handGesture, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.drawing = mp.solutions.drawing_utils
        self.hands = mp.solutions.hands
        self.hand_obj = self.hands.Hands(max_num_hands=1)
        self.start_init = False
        self.prev = -1
        self.start_time = 0
        self.end_time = 0

    def count_fingers(self, lst):
        cnt = 0
        thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2
        if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
            cnt += 1
        if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
            cnt += 1
        return cnt

    def run(self):
        while True:
            self.end_time = time.time()
            _, frm = self.cap.read()
            frm = cv2.flip(frm, 1)
            res = self.hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
            if res.multi_hand_landmarks:
                hand_keyPoints = res.multi_hand_landmarks[0]
                cnt = self.count_fingers(hand_keyPoints)
                print(self.count_fingers(hand_keyPoints))
                if not (self.prev == cnt):
                    if not (self.start_init):
                        self.start_time = time.time()
                        self.start_init = True
                    elif (self.end_time - self.start_time) > 0.2:
                        if (cnt == 0):
                            pyautogui.press("Escape")
                        elif (cnt == 1):
                            pyautogui.press("space")
                        elif (cnt == 2):
                            pyautogui.press("m")
                        elif (cnt == 3):
                            pyautogui.press("left")
                        elif (cnt == 4):
                            pyautogui.press("right")
                        elif (cnt == 5):
                            pyautogui.press("f")
                        self.prev = cnt
                        self.start_init = False
                self.drawing.draw_landmarks(frm, hand_keyPoints, self.hands.HAND_CONNECTIONS)
            cv2.imshow("Window Pergerakan Tangan", frm)
            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break

    def show(self):
        self.start()
        pass


class ObjectDetectionVideo(QThread):
    def __init__(self, parent=None):
        super(ObjectDetectionVideo, self).__init__(parent)
        self.net = cv2.dnn.readNet("weight/yolov3-tiny.weights", "cfg_realtime/yolov3-tiny.cfg")
        self.net = cv2.dnn.readNet("weight/yolov3.weights", "cfg_realtime/yolov3.cfg")
        self.classes = []
        with open("coco.names_object/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def run(self):
        timeframe = time.time()
        frame_id = 0
        while True:
            _, frm = self.cap.read()
            frame_id += 1
            # frm = cv2.flip(frm, 1)
            height, width, channels = frm.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frm, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[i]
                    color = (30, 144, 255)
                    rectangle_bgr = (30, 144, 255)
                    cv2.rectangle(frm, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frm, label, (x, y + 30), font, 1, color, 2)
                    cv2.putText(frm, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)

            elapsed_time = time.time() - timeframe
            fps = frame_id / elapsed_time
            cv2.putText(frm, str(round(fps, 2)), (10, 50), font, 2, (0, 0, 255), 2)
            cv2.putText(frm, "FPS", (220, 50), font, 2, (0, 0, 255), 2)
            cv2.imshow("Mendeteksi Objek Video", frm)
            # Jika menekan escape maka akan keluar dari program
            if cv2.waitKey(1) & 0xFF == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        #self.cap.release()
        #cv2.destroyAllWindows()

    def show(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Buka File", "", "Video (*.avi *.jpg)")
        self.cap = cv2.VideoCapture(filename)
        self.start()
        pass


class ObjectDetectionCamera(QThread):
    def __init__(self, parent=None):
        super(ObjectDetectionCamera, self).__init__(parent)
        self.net = cv2.dnn.readNet("weight/yolov3-tiny.weights", "cfg_realtime/yolov3-tiny.cfg")
        self.net = cv2.dnn.readNet("weight/yolov3.weights", "cfg_realtime/yolov3.cfg")
        self.classes = []
        with open("coco.names_object/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def run(self):
        timeframe = time.time()
        frame_id = 0
        while True:
            _, frm = self.cap.read()
            frame_id += 1
            # frm = cv2.flip(frm, 1)
            height, width, channels = frm.shape

            # Detecting objects
            blob = cv2.dnn.blobFromImage(frm, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[i]
                    color = (30, 144, 255)
                    rectangle_bgr = (30, 144, 255)
                    cv2.rectangle(frm, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frm, label, (x, y + 30), font, 1, color, 2)
                    cv2.putText(frm, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)

            elapsed_time = time.time() - timeframe
            fps = frame_id / elapsed_time
            cv2.putText(frm, str(round(fps, 2)), (10, 50), font, 2, (255, 255, 255), 2)
            cv2.putText(frm, "FPS", (220, 50), font, 2, (255, 255, 255), 2)
            cv2.imshow("Mendeteksi Objek Kamera", frm)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            if cv2.waitKey(1) & 0xFF == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break

        #self.cap.release()
        #cv2.destroyAllWindows()

    def show(self):
        self.cap = cv2.VideoCapture(0)
        self.start()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lisensi = LisensiKey()
    lisensi.show()
    sys.exit(app.exec_())