import RPi.GPIO as GPIO
import MFRC522
import requests
from soundplayer import SoundPlayer
import pygame
import time
import credentials
from const import CONSTANTS
from PyQt5.QtCore import QThread, pyqtSignal
import checkInternet
import logging
pygame.init()
class Reader(QThread):
    signal = pyqtSignal(dict)
    nointernet = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        logging.info("Iniciando Reader...")
    
    def run(self):
        continue_reading = True        
        logging.info("Iniciando Lector...")
        MIFAREReader = MFRC522.MFRC522()
        logging.info("Lector iniciado...")
        
        while continue_reading:
    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                logging.info("Tarjeta leida...")
                rfid = ''.join([str(hex(i))[2:] if i>16 else '0'+ str(hex(i))[2:] for i in uid ])[:-2]
                rfid = rfid.upper()
                logging.info('rfid: {0}'.format(rfid))
                soundpath = "/home/pi/redlabgui/sounds/"
                song = "JohnCenaShort.wav" if rfid == "CFCAA9B9" else "alert.wav"
                #song = "alert.wav"
                logging.info('Enviando sonido de alerta...')
                p = pygame.mixer.Sound(soundpath+song)
                p.play()
                logging.info('Sonido de alerta ejecutado...')
                time.sleep(0.001)                
                if checkInternet.check():
                    logging.info('Conexión a internet checked...')
                    #Check if user exists on Airtable
                    #req = requests.post(CONSTANTS["RECORDS"], {'rfid' : rfid,'lab_id' : CONSTANTS["ID"]}, headers=credentials.totem_credential).json()
                    req = {
                        'rfid': rfid,
                        'lab_id': CONSTANTS["ID"],
                        'totem_cred': credentials.totem_credential,
                        'action': 'New entry'
                    }
                    #Send information to HandleResponse in gui.py
                    logging.info("Enviando señal desde reader...")
                    self.signal.emit(req)
                    logging.info("Señal enviada desde reader...")
                    time.sleep(1)
                    GPIO.cleanup()
                else:
                    logging.info('triggering local db')                    
                    self.nointernet.emit(rfid)


if __name__ == "__main__":
	r = Reader()
	r.run()
