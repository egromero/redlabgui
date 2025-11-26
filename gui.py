from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtTest import QTest
from reader import Reader, SerialManager
import reader
from const import CONSTANTS
import apiHandler
import localGui
from web import Browser
import requests
import credentials
from airtable_integration import check_record, create_new_entry, create_new_student, record_departure_time
import logging

class MWindow(QMainWindow):
    def __init__(self, parent=None):        
        super(MWindow, self).__init__(parent=parent)
        self.setup_init()
    
    def setup_init(self):
        logging.info("Iniciando Mwindow...")
        self.dataset = CONSTANTS["DATASET"]
        
        self.serial_manager = SerialManager()
        self.serial_manager.start_threads()
        
        self.reader = Reader(self.serial_manager)
        self.reader.signal.connect(self.handle_response)
        self.reader.nointernet.connect(self.no_internet)
        self.reader.start()
        
        self.name = QLabel(self)
        self.name.move(CONSTANTS["XLABEL"],CONSTANTS["YLABEL"])
        self.name.resize(CONSTANTS["SIZELABELX"], CONSTANTS["SIZELABELY"])
        self.name.setStyleSheet('QLabel {background: transparent; font-family: "Times new roman"; font-size: 50px}')
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        
        #Capacidad
        #self.capacidad = 10
        #self.personas = 1
        
        #self.cap_overlay = QLabel(
        #    None,
        #    flags=QtCore.Qt.Tool
        #        | QtCore.Qt.FramelessWindowHint
        #        | QtCore.Qt.WindowStaysOnTopHint
        #)
        #self.cap_overlay.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #self.cap_overlay.setStyleSheet(
        #    "QLabel {"
        #    " background: rgba(255,255,255,200);"
        #    " border: 1px solid rgba(0,0,0,180);"
        #    " border-radius: 6px;"
        #    " padding: 6px 10px;"
        #    " font-size: 16px;"
        #    "}"
        #)
        #self.cap_overlay.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)        
        #self.update_capacidad_texto()
        #self.position_overlay()
        #self.cap_overlay.show()
        #self.resizeEvent = self.on_resize
        
        self.showFullScreen()
        self.webBrowser = Browser()
        self.webBrowser.showFullScreen()
        self.webBrowser.load(CONSTANTS["URL_SLIDE"])
        logging.info("Terminando inicialización de Mwindow...")
        
        
    #def update_capacidad_texto(self):
    #    texto = f'Capacidad\n{self.personas} / {self.capacidad}'
    #    self.cap_overlay.setText(texto)
    #    self.cap_overlay.adjustSize()
    
    #def position_overlay(self, margin=12):
    #    screen = QApplication.primaryScreen()
    #    geo = screen.availableGeometry()
    #    x = geo.right() - self.cap_overlay.width() - margin
    #    y = geo.bottom() - self.cap_overlay.height() - margin
    #    self.cap_overlay.move(x,y)
        
    #def on_resize(self, event):
    #    super(MWindow, self).resizeEvent(event)
    #    self.position_overlay()
    
    #def on_capacidad_cambio(self, personas=None, capacidad=None):
    #    if personas is not None:
    #        self.personas = personas
    #    if capacidad is not None:
    #        self.capacidad = capacidad
    #    self.update_capacidad_texto()
    #    self.position_overlay()
        
    def setScreen(self, image):        
        style = "QWidget {background : url(%s) no-repeat center center fixed}" % image
        self.setStyleSheet(style)
        self.webBrowser.hide()
        QTest.qWait(4000)
        self.webBrowser.showFullScreen()

    def no_internet(self, rfid):
        #local = localGui.LocalW(rfid)
        print('No hay internet --------------------------------------------')
        #local.showFullScreen()
        #local.show()

    def handle_response(self, data):
        #Abre el torniquete (DEBUG)
        print("Entrando a handle response")
        self.serial_manager.client_flag = 1 #-> Habilitacion de entrada y salida
        
        
        #data = self.serial_manager.uid
        
        
        logging.info("Entrando a handle response...")
        print("Entrando a handle response...")
        print(data)
        #response = check_record(data)
        #if response['action'] == 'Entry':
        if False:
            #Usuario no existe en base de datos.
            #if response["type"] == "nonexistent":
            if True:
                image = CONSTANTS['DATASET']['WAIT'] 
                self.setScreen(image)
                #Buscamos usuario en API UC; si existe crea el nuevo usuario y su ingreso.
                logging.info('Buscando datos desde API UC...')
                print('Buscando datos desde API UC...')
                logging.info(data)
                data = self.check_ucdb(data['rfid'])
                logging.info('Datos obtenidos desde API UC...')
                print('Datos obtenidos desde API UC...') 
                if data == 200:
                    #Revisar que mostrar a usuario creado desde API UC.
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
            #else:
                #Revisar si tiene induccion.
                #if not(response['data']['Status (from Inducción-Persona)'][0]):
                    #Acciones para induccion pendiente
                    #logging.info('Mostrando inducción pendiente...')
                    #image = CONSTANTS['DATASET']['NOTAUTH']
                    #self.setScreen(image)
                    #QTest.qWait(1000)
                #logging.info('Mostrando Bienvenida...')
                #image = CONSTANTS['DATASET']['ENROLL']
                #create_new_entry(response['data'], credentials.totem_credential)
                #self.name.setText(data['data']['student']['nombre'].split(' ')[0].upper()) 
                #self.setScreen(image)                               

        #elif response['action'] == 'Exit':
            #record_departure_time(response['data']['Record ID - Último ingreso'][0])
            #image = CONSTANTS['DATASET']['GETOUT']
            #logging.info("Nombre de salida: {0}".format(reponse['data']['Nombre completo'].split(' ')[0].upper()))
            #self.name.setText(reponse['data']['Nombre completo'].split(' ')[0].upper())
            #logging.info("Texto seteado para salida...")
            #self.setScreen(image)
           
           
        # AIRTABLE
                            

      
    def check_ucdb(self, rfid):
        #Crea al nuevo usuario y su ingreso respectivo.
        logging.info('Entrando a check_ucdb...')
        logging.info('Entrando a apiHandler...')
        data = apiHandler.get_data(rfid)
        logging.info('Saliendo de apiHandler...')
        logging.info("Output ApiHandler: {0}".format(data))
        if isinstance(data, str):
            return None
        #Creacion de usuario inexistente en base de datos
        # Last code --> student = requests.post(CONSTANTS['STUDENTS-TOTEM'], data, headers=credentials.totem_credential)
        student = create_new_student(data, credentials.totem_credential)
        #Creacion de registro de ingreso de usuario  --> Revisar si este paso es necesario.
        # Last code --> record = requests.post(CONSTANTS['RECORDS'], {'rfid': data['rfid'],'lab_id':CONSTANTS['ID']}, headers=credentials.totem_credential).json()
        record = create_new_entry(student, credentials.totem_credential)
        QTest.qWait(1000)
        #self.handle_response(record)
        return 200


