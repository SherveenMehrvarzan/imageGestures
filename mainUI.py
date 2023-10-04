import sys
from typing import Optional
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import QThread, Signal, QObject, Slot, QSize, Qt
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage
import cv2
import time
import os
from pathlib import Path

# app = QApplication(sys.argv)
# label = QLabel("Hello World!")
# label.show()
# app.exec()

class CameraThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    
    def run(self):
        # TODO: allow user to select camera here
        self.cap = cv2.VideoCapture(0)

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                # ERROR
                print("error happened")
            else:
                imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cTime = time.time()
                print(cTime)
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(imgRGB, f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                img = QImage(imgRGB.data, imgRGB.shape[1], imgRGB.shape[0], QImage.Format_RGB888)
                self.updateFrame.emit(img)

class ImageProvider(QQuickImageProvider):
    imageChanged = Signal(QImage)
    
    def __init__(self):
        super(ImageProvider, self).__init__(QQuickImageProvider.Image)

        self.cam = CameraThread()
        self.cam.updateFrame.connect(self.update_image)
        self.image = None
    
    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        if self.image:
            img = self.image
        else:
            img = QImage(600, 500, QImage.Format_RGBA8888)
            img.fill(Qt.black)
        
        return img

    @Slot()
    def update_image(self, img):
        self.imageChanged.emit(img)
        self.image = img
    
    @Slot()
    def start(self):
        print("starting")
        self.cam.start()
    
    @Slot()
    def killThread(self):
        print("finishing thread...")
        try:
            self.cam.cap.release()
            cv2.destroyAllWindows()
        except:
            pass

class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    main = MainWindow()
    myImageProvider = ImageProvider()
    engine.rootContext().setContextProperty("backend", main)
    engine.rootContext().setContextProperty("myImageProvider", myImageProvider)

    engine.addImageProvider("myImageProvider", myImageProvider)

    engine.load(os.fspath(Path(__file__).resolve().parent /  "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())