from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtTest import QTest
from reader import Reader
from const import CONSTANTS
import apiHandler
import localGui
from web import Browser
import requests
import credentials
from airtable_integration import check_record, create_new_entry, create_new_student, record_departure_time

class MWindow(QMainWindow):
    def __init__(self, parent=None):
        print("Funcionando...")
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
        self.showFullScreen()
        self.webBrowser = Browser()
        self.webBrowser.showFullScreen()
        self.webBrowser.load(CONSTANTS["URL_SLIDE"])

    def setScreen(self, image):        
        style = "QWidget {background : url(%s) no-repeat center center fixed}" % image
        self.setStyleSheet(style)
        self.webBrowser.hide()
        QTest.qWait(4000)
        self.webBrowser.showFullScreen()

    def no_internet(self, rfid):
        local = localGui.LocalW(rfid)
        local.showFullScreen()
        local.show()

    def handle_response(self, data):
        
        response = check_record(data)
        if response['action'] == 'Entry':            
            #Usuario no existe en base de datos.
            if response["type"] == "nonexistent":
                image = CONSTANTS['DATASET']['WAIT'] 
                self.setScreen(image)
                #Buscamos usuario en API UC; si existe crea el nuevo usuario y su ingreso.
                data = self.check_ucdb(data['data']['rfid'])
                if data == 200:
                    #Revisar qué mostrar a usuario creado desde API UC.
                    image = CONSTANTS['DATASET']['NOTAUTH']
                    self.setScreen(image)
                    QTest.qWait(1000)
                    image = CONSTANTS['DATASET']['ENROLL']
                    self.setScreen(image)
                else:
                    #Se muestra solicitud de registro manual por datos no encontrados en API UC.
                    image = CONSTANTS['DATASET']['NONEXISTENT']
                    self.setScreen(image)
            #Usuario existe en base de datos.
            else:
                #Revisar si tiene inducción.
                if not(response['data']['Status (from Inducción-Persona)'][0]):
                    #Acciones para inducción pendiente
                    image = CONSTANTS['DATASET']['NOTAUTH']
                    self.setScreen(image)
                    QTest.qWait(1000)
                image = CONSTANTS['DATASET']['ENROLL']
                create_new_entry(response['data'])
                #self.name.setText(data['data']['student']['nombre'].split(' ')[0].upper()) 
                self.setScreen(image)                               

        elif response['action'] == 'Exit':
            record_departure_time(response['data']['Record ID - Último ingreso'][0])
            image = CONSTANTS['DATASET']['GETOUT']
            self.name.setText(data['data']['Nombre completo'].split(' ')[0].upper())
            self.setScreen(image)


    def check_ucdb(self, rfid):
        #Crea al nuevo usuario y su ingreso respectivo.
        data = apiHandler.get_data(rfid)
        if isinstance(data, str):
            return None
        #Creación de usuario inexistente en base de datos
        # Código antiguo --> student = requests.post(CONSTANTS['STUDENTS-TOTEM'], data, headers=credentials.totem_credential)
        student = create_new_student(data, credentials.totem_credential)
        #Creación de registro de ingreso de usuario  --> Revisar si este paso es necesario.
        # Código antiguo --> record = requests.post(CONSTANTS['RECORDS'], {'rfid': data['rfid'],'lab_id':CONSTANTS['ID']}, headers=credentials.totem_credential).json()
        record = create_new_entry(student)
        QTest.qWait(1000)
        #self.handle_response(record)
        return 200


