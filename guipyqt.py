from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtTest import QTest
from reader import Reader
from const import CONSTANTS

class MWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MWindow, self).__init__(parent=parent)
        self.setup_init()
    
    def setup_init(self):
        self.dataset = CONSTANTS["DATASET"]
        self.reader = Reader()
        self.reader.signal.connect(self.handle_response)
        self.reader.start()
        self.name = QLabel(self)
        self.name.move(158,490)
        self.name.resize(970, 80)
        self.name.setStyleSheet('QLabel {background: transparent; font-family: "Times new roman"; font-size: 50px}')
        self.name.setAlignment(QtCore.Qt.AlignCenter) 
        self.showFullScreen()
    def setScreen(self, image):
        style = "QWidget {background : url(%s) no-repeat center center fixed}" % image
        self.setStyleSheet(style)
        QTest.qWait(1000)


    def handle_response(self, data):
        print(data)
        if data["type"] == "nonexistent":
            image = CONSTANTS['DATASET']['WAIT'] 
            self.setScreen(image)
            data = self.check_ucdb(data['data']['rfid'])
        if not data:
            image = CONSTANTS['DATASET']['NONEXISTENT']
            self.setScreen(image)
        else:
            image = CONSTANTS['DATASET']['ENROLL']
            self.name.setText(data['data']['student']['nombre'].split(' ')[0].upper())
            self.setScreen(image)


    def check_ucdb(self, rfid):
        print("checking.. ", rfid)
        return None