from PyQt5.QtWidgets import QApplication,QStackedWidget, QLineEdit,QWidget,QVBoxLayout, \
    QFormLayout, QRadioButton,QLabel,QGridLayout,QPushButton,QFileDialog,QMainWindow,QSizePolicy, QStyle,\
    QSlider, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont,QImage
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot, QRect,  QUrl,QTime,QObject, QTimer,QCoreApplication,QProcess
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoProbe,QVideoFrame,QAbstractVideoSurface,QAbstractVideoBuffer,QVideoSurfaceFormat
from PyQt5.QtMultimediaWidgets import QVideoWidget
import cv2 
import sys

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Starting/Ending Frame of Shot")
        self.UiComponents()
        self.setGeometry(500, 300, 1000, 700)

    def UiComponents(self):
       #create media player object
        self.frame_number = 0
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object 
        videowidget = QVideoWidget()
 
        #create open button
        openBtn = QPushButton('Open Video')
        self.frame_rate=0
        self.length =0
        openBtn.clicked.connect(self.open_file)
        
        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
 
        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #Create frame number label
        self.currenttime_label= QLabel('Time:')
        self.currenttime_label.setFixedSize(500, 30)
        self.currentframe_label= QLabel('Current Frame Number:')
        self.currentframe_label.setFixedSize(500, 30)
        #self.totalframe_label= QLabel('Total Frame Number:')
        #self.totalframe_label.setFixedSize(500, 30)
        self.setframeinstructions_label= QLabel('Click "set" button to grab current frame number from video.')
        self.setframeinstructions_label.setFixedSize(500, 30)
        #Create start_frame and end_frame label
        self.startframe_button = QPushButton('Set')
        self.startframe_button.clicked.connect(lambda:self.save_framenum('start'))

        self.endframe_button = QPushButton('Set')
        self.endframe_button.clicked.connect(lambda:self.save_framenum('end'))

        self.startframe_label= QLabel('Starting Frame:')
        self.endframe_label= QLabel('Ending Frame:')

        self.startframe_edit= QLineEdit()
        self.endframe_edit = QLineEdit()

        self.time_label = QLabel('Diff Between Frames/Time Between Frames(s):')
        self.time_edit = QLineEdit()
        #Create submit button
        self.submitButton=QPushButton("Submit",self)
        self.submitButton.clicked.connect(self.processSubmission)

        #Create vars for inputs from MainWindow
        self.release_height = QLineEdit()
        self.right_handed = QCheckBox('')

        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)


        #Create first gridbox layout
        gridLayout= QGridLayout()
        
        gridLayout.addWidget(self.startframe_button,0,1)
        gridLayout.addWidget(self.startframe_label, 0, 2)
        gridLayout.addWidget(self.startframe_edit, 0, 3)
        gridLayout.addWidget(self.endframe_button,1,1)
        gridLayout.addWidget(self.endframe_label, 1, 2)
        gridLayout.addWidget(self.endframe_edit, 1, 3)
        gridLayout.addWidget(self.time_label, 2, 2)
        gridLayout.addWidget(self.time_edit, 2, 3)
        #Create second gridbox layout for submission
        gridLayout2 = QGridLayout()
        #gridLayout2.addWidget(self.backButton,0,1)
        gridLayout2.addWidget(self.submitButton,1,2)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout.addWidget(self.currenttime_label)
        vboxLayout.addWidget(self.currentframe_label)
        #vboxLayout.addWidget(self.totalframe_label)
        vboxLayout.addWidget(self.setframeinstructions_label)
        vboxLayout.addLayout(gridLayout)
        vboxLayout.addLayout(gridLayout2)
 
        self.setLayout(vboxLayout)
 
        self.mediaPlayer.setVideoOutput(videowidget)
 
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)


    def processSubmission(self):
        start_frame = int(self.startframe_edit.text())
        end_frame = int(self.endframe_edit.text())
        self.run_save_frames(start_frame,'start_frame')
        self.run_save_frames(end_frame,'end_frame')

    def passingInformation(self):
        self.VideoWindow.release_height.setText(self.e2.text())
        self.VideoWindow.right_handed.setChecked(self.b1.isChecked())
        self.VideoWindow.displayInfo()
        self.close()
    def run_save_frames(self,frame,file_name):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        flag, img = self.cap.read()
        self.filename
        cv2.imwrite(self.filename+file_name+'.jpg',img)
    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
 
        if self.filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))
            self.playBtn.setEnabled(True)
            self.cap = cv2.VideoCapture(self.filename)
            self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            #self.totalframe_label.setText('Total Frame Number: '+str(int(self.frame_count)))
 
 
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()
  
    def save_framenum(self,frame_type):
        if frame_type == 'start':
            self.startframe_edit.setText(str(self.frame_number))
        else:
            self.endframe_edit.setText(str(self.frame_number))
        
        if self.endframe_edit.text() and self.endframe_edit.text():
            diff = (int(self.endframe_edit.text())- int(self.startframe_edit.text()))
            num_sec = diff*(1/float(self.frame_rate))
            self.time_edit.setText(str(diff)+' / '+str(num_sec))

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
 
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)
        self.seconds = (position/1000)
        self.frame_number = int(self.frame_rate*self.seconds)

        seconds=(position/1000)%60
        minutes=(position/(1000*60))%60
        hours=(position/(1000*60*60))%24

        self.currentframe_label.setText('Current Frame Number: '+str(self.frame_number))
        self.currenttime_label.setText('Time: '+"%d:%d:%d" % (hours, minutes, seconds))
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
    def displayInfo(self):
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = VideoWindow()
    demo.show()
    sys.exit(app.exec_())