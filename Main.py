import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject
from PyQt5 import QtCore
import sys

class Camera_Managerment(QThread):
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url) -> None:
        super(Camera_Managerment, self).__init__()
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False

    def run(self) -> None:
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        if cap.isOpened():
            while self.__thread_active:
                #
                if not self.__thread_pause:
                    ret, frame = cap.read()

                    if ret:
                        h, w, ch = frame.shape
                        bytes_per_line = w * ch
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_rgb_image = QImage(cv_rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                        qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio)  # 720p
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                    else:
                        break

        cap.release()
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0
        #self.url_1 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"
        #self.url_2 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"
        #self.url_3 = "rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0"

        self.url_1 ="1.mp4"
        self.url_2 = "2.mp4"
        self.url_3 = "3.mp4"


        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}
        self.cam_1 = QLabel()
        self.cam_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.cam_1.setScaledContents(True)
        self.cam_1.installEventFilter(self)
        self.cam_1.setObjectName("cam_1")
        self.list_of_cameras_state["cam_1"] = "Normal"

        self.QScrollArea_1 = QScrollArea()
        self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_1.setWidgetResizable(True)
        self.QScrollArea_1.setWidget(self.cam_1)

        self.cam_2 = QLabel()
        self.cam_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.cam_2.setScaledContents(True)
        self.cam_2.installEventFilter(self)
        self.cam_2.setObjectName("cam_2")
        self.list_of_cameras_state["cam_2"] = "Normal"

        self.QScrollArea_2 = QScrollArea()
        self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_2.setWidgetResizable(True)
        self.QScrollArea_2.setWidget(self.cam_2)

        self.cam_3 = QLabel()
        self.cam_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.cam_3.setScaledContents(True)
        self.cam_3.installEventFilter(self)
        self.cam_3.setObjectName("cam_3")
        self.list_of_cameras_state["cam_3"] = "Normal"

        self.QScrollArea_3 = QScrollArea()
        self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_3.setWidgetResizable(True)
        self.QScrollArea_3.setWidget(self.cam_3)

        self.cam_4 = QLabel()
        self.cam_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.cam_4.setScaledContents(True)
        self.cam_4.installEventFilter(self)
        self.cam_4.setObjectName("cam_4")
        self.list_of_cameras_state["cam_4"] = "Normal"

        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.cam_4)
        self.__SetupUI()

        self.CaptureIpCamera_1 = Camera_Managerment(self.url_1)
        self.CaptureIpCamera_1.ImageUpdated.connect(lambda image: self.ShowCam1(image))

        self.CaptureIpCamera_2 = Camera_Managerment(self.url_2)
        self.CaptureIpCamera_2.ImageUpdated.connect(lambda image: self.ShowCam2(image))

        self.CaptureIpCamera_3 = Camera_Managerment(self.url_3)
        self.CaptureIpCamera_3.ImageUpdated.connect(lambda image: self.ShowCam3(image))

        self.CaptureIpCamera_4 = Camera_Managerment(self.url_1)
        self.CaptureIpCamera_4.ImageUpdated.connect(lambda image: self.ShowCam4(image))

        self.CaptureIpCamera_1.start()
        self.CaptureIpCamera_2.start()
        self.CaptureIpCamera_3.start()
        self.CaptureIpCamera_4.start()

    def __SetupUI(self) -> None:
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.QScrollArea_1, 0, 0)
        grid.addWidget(self.QScrollArea_2, 0, 1)
        grid.addWidget(self.QScrollArea_3, 1, 0)
        grid.addWidget(self.QScrollArea_4, 1, 1)

        self.widget = QWidget(self)
        self.widget.setLayout(grid)

        self.setCentralWidget(self.widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'Blue';}")
        self.setWindowIcon(QIcon(QPixmap("cam_2.png")))
        self.setWindowTitle("IP Camera Management System")

    @QtCore.pyqtSlot()
    def ShowCam1(self, frame: QImage) -> None:
        self.cam_1.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCam2(self, frame: QImage) -> None:
        self.cam_2.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCam3(self, frame: QImage) -> None:
        self.cam_3.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def ShowCam4(self, frame: QImage) -> None:
        self.cam_4.setPixmap(QPixmap.fromImage(frame))


    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if source.objectName() == 'cam_1':
                #
                if self.list_of_cameras_state["cam_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["cam_1"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["cam_1"] = "Normal"
            elif source.objectName() == 'cam_2':
                #
                if self.list_of_cameras_state["cam_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["cam_2"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["cam_2"] = "Normal"
            elif source.objectName() == 'cam_3':
                #
                if self.list_of_cameras_state["cam_3"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_4.hide()
                    self.list_of_cameras_state["cam_3"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_4.show()
                    self.list_of_cameras_state["cam_3"] = "Normal"
            elif source.objectName() == 'cam_4':
                #
                if self.list_of_cameras_state["cam_4"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.list_of_cameras_state["cam_4"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.list_of_cameras_state["cam_4"] = "Normal"
            else:
                return super(MainWindow, self).eventFilter(source, event)
            return True
        else:
            return super(MainWindow, self).eventFilter(source, event)

    def closeEvent(self, event) -> None:
        if self.CaptureIpCamera_1.isRunning():
            self.CaptureIpCamera_1.quit()

        if self.CaptureIpCamera_2.isRunning():
            self.CaptureIpCamera_2.quit()

        if self.CaptureIpCamera_3.isRunning():
            self.CaptureIpCamera_3.quit()
        event.accept()

def main() -> None:
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()