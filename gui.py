from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtTest import QTest
from reader import Reader
from const import CONSTANTS
import apiHandler
import localGui

class MWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MWindow, self).__init__(parent=parent)
        self.setup_init()
    
    def setup_init(self):
        self.dataset = CONSTANTS["DATASET"]
        self.reader = Reader()
        self.reader.signal.connect(self.handle_response)
        self.reader.nointernet.connect(self.no_internet)
        self.reader.start()
        self.name = QLabel(self)
        self.name.move(CONSTANTS["XLABEL"],CONSTANTS["YLABEL"])
        self.name.resize(CONSTANTS["SIZELABELX"], CONSTANTS["SIZELABELY"])
        self.name.setStyleSheet('QLabel {background: transparent; font-family: "Times new roman"; font-size: 50px}')
        self.name.setAlignment(QtCore.Qt.AlignCenter) 
        #self.showFullScreen()

    def setScreen(self, image):
        style = "QWidget {background : url(%s) no-repeat center center fixed}" % image
        self.setStyleSheet(style)
        QTest.qWait(2000)

    def no_internet(self, rfid):
        local = localGui.LocalW(rfid)
        local.showFullScreen()
        local.show()



    def handle_response(self, data):
        if data["type"] == "nonexistent":
            image = CONSTANTS['DATASET']['WAIT'] 
            self.setScreen(image)
            data = self.check_ucdb(data['data']['rfid'])
        if not data:
            image = CONSTANTS['DATASET']['NONEXISTENT']
            self.setScreen(image)
        else:
            if data['data']['student']['status']:
                image = CONSTANTS['DATASET']['NOTAUTH']
                labs = list(filter(lambda x: (x['id'] == CONSTANTS["ID"]), data['data']['laboratory']))
                if labs:
                    image = CONSTANTS['DATASET']['ENROLL']
            else:
                image = CONSTANTS['DATASET']['GETOUT']

            self.name.setText(data['data']['student']['nombre'].split(' ')[0].upper())
            self.setScreen(image)


    def check_ucdb(self, rfid):
        data = apiHandler.get_data(rfid)
        if isinstance(data, str):
            return None
        student = requests.post(self.url_student, data, headers=credentials.totem_credential)
        record = requests.post(CONSTANTS['RECORDS'], {'rfid': data['rfid'],'lab_id':CONSTANTS['ID']}, headers=credentials.totem_credential).json()
        QTest.qWait(1000)
        self.handle_response(record)


