from Ella_Script.video_capture.webcamera import Ui_MainWindow
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QMainWindow,QDesktopWidget,QAction,QMessageBox,QFileDialog
from Ella_Script.video_capture.webcam import OpenCVWebCam
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon,QFont,QImage,QPixmap
import cv2
from Ella_Script.video_capture.vision import Ui_Form

class VIDEOTHREAD(threading.Thread):
    def __init__(self,webport,duration,interval,path):
        super(VIDEOTHREAD, self).__init__()
        self.should_stop = threading.Event()
        self.webport=webport
        self.duration = duration
        self.interval = interval
        self.path = path


    def run(self):
        while not self.should_stop.is_set():
            self.web = OpenCVWebCam(self.webport)
            state = self.web.capture_video(self.duration,self.interval,self.path)
            if state == 1:
                self.should_stop.set()
    def stop(self):
        # self.should_stop.set()
        pass


class secondwindow(QtWidgets.QWidget, Ui_Form):  # 创建子UI类

    def __init__(self):
        super(secondwindow, self).__init__()
        self.setupUi(self)



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)  # inherit the Ui_MainWindow Class
        self.setupUi(self)  # run the setupUi
        self.thread = None
        self.web = self.comboBox.currentText()
        self.buttonBox.rejected.connect(self.close_window)
        self.buttonBox.accepted.connect(self.capture_videos)
        self.menuAbout.triggered[QAction].connect(self.processtrigger)
        self.pushButton.clicked.connect(self.open_file)
        self.pushButton_2.clicked.connect(self.capture_videos)
        self.secondwindow = secondwindow()
        self.menuvision.triggered[QAction].connect(self.show_secondwindow)


    def open_file(self):
        OPEN_FILE_NAME = QFileDialog.getExistingDirectory(self,"choose folder")
        if OPEN_FILE_NAME is not None:
            self.lineEdit_3.setText(OPEN_FILE_NAME)
    def processtrigger(self,q):
        if q.text() == "version":
            QMessageBox.information(self, "version","v1.0.0 \r\nelladeng@163.com",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

    def capture_videos(self):
        self.duration = self.lineEdit.text()
        self.interval = self.lineEdit_2.text()
        self.video_path = self.lineEdit_3.text()
        self.thread = VIDEOTHREAD(self.web,int(self.duration),int(self.interval),self.video_path)
        self.thread.setDaemon(True)
        self.thread.start()
        self.pushButton_2.setEnabled(False) #diable start button
        if not self.thread.is_alive():
            self.pushButton_2.setEnabled(True)

    def show_secondwindow(self,q):
        if q.text() == "image":
            self.secondwindow.show()
            self.secondwindow.label.setScaledContents(True)
            self.secondwindow.load_image.clicked.connect(self.show_image)

    def show_image(self):
        OPEN_FILE_NAME = QFileDialog.getOpenFileName(self, "open file",filter="Imagefiles (*.jpg)")
        print(OPEN_FILE_NAME)
        Im = cv2.imread(OPEN_FILE_NAME[0])  # 通过Opencv读入一张图片
        image_height, image_width, image_depth = Im.shape  # 获取图像的高，宽以及深度。
        QIm = cv2.cvtColor(Im, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                     image_width * image_depth,
                     QImage.Format_RGB888)
        self.secondwindow.label.setPixmap(QPixmap.fromImage(QIm))



    def close_window(self):
        # self.thread.stop()
        qApp = QApplication.instance()
        qApp.quit()
        sys.exit()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


