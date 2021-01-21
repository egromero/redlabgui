# import RPi.GPIO as GPIO
# import MFRC522
import requests
# from soundplayer import SoundPlayer
import time
import credentials
from const import CONSTANTS
from PyQt5.QtCore import QThread, pyqtSignal

class Reader(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    
    def run(self):
        rfid = "a"
        request = requests.post(CONSTANTS["RECORDS"], {'rfid' : rfid,'lab_id' : CONSTANTS["ID"]}, headers=credentials.totem_credential).json()
        #request = {'type': 'nonexistent', 'data': {'rfid': 'sa'}}
        self.signal.emit(request)
        # continue_reading = True
        
        # MIFAREReader = MFRC522.MFRC522()
        
        # while continue_reading:
    
        #     (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                
        #     (status,uid) = MIFAREReader.MFRC522_Anticoll()

        #     if status == MIFAREReader.MI_OK:
                
        #         rfid = ''.join([str(hex(i))[2:] if i>16 else '0'+ str(hex(i))[2:] for i in uid ])[:-2]
        #         rfid = rfid.upper()

        #         p = SoundPlayer("/home/pi/guiPythonLABFAB/sounds/BeepIn.mp3", 0)

        #         p.play(1)

        #         time.sleep(0.001)
        #         req = requests.post(CONSTANTS["RECORDS"], {'rfid' : rfid,'lab_id' : CONSTANTS["ID"]}, headers=credentials.totem_credential).json()

        #         self.signal.emit(req)
        #         time.sleep(5) 
                         
        #         GPIO.cleanup()

