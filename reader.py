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
import serial
import json
import threading
import re

class SerialManager:
    def __init__(self):
        self.port = '/dev/serial0'
        self.baudrate = 115200
        self.timeout = 0.01
        
        self.ser = None
        self.lock = threading.Lock()
        
        self.uid = None
        self.uid_flag = 0
        self.client_flag = 0  # 1 para autorizado, 2 para denegado
        self.tid = 0
        self.confirmation_flag = 0
        
        # eventos de control
        self.enable = threading.Event()
        self.stop_event = threading.Event()
        
        #abrir al inicio
        self.open_serial()
        
    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout = self.timeout, rtscts=False, xonxoff=False)
            time.sleep(2)
            print("Serial abierto correctamente.")
            
        except Exception as e:
            print(f"No se pudo abrir el serial: {e}")
            self.ser = None
            
    def reconnect_serial(self):
        try:
            with self.lock:
                if self.ser:
                    self.ser.close()
                print("Intentando reconectar...")
                time.sleep(1)
                self.ser = serial.Serial(self.port, self.baudrate, timeout = self.timeout)
                print("Reconexion exitosa.")
        except Exception as e:
            print(f"Fallo la reconexion: {e}")
            self.ser = None
            time.sleep(2)
            
    def safe_readline(self):
        try:
            with self.lock:
                return self.ser.readline().decode('utf-8', errors='ignore').strip()
        except serial.SerialException as e:
            print(f"Serial desconectado {e}")
            self.reconnect_serial()
            return ""
        except Exception as e:
            print(f"Error inesperado de lectura: {e}")
            return ""
    
    def get_mesage(self, data):
        try:
            json.loads(data)
            return data
        except json.JSONDecodeError:
            # En caso de que el mensaje llegue mal, se puede recuperar la informacion importante
            patron = r'"uid"\s*:\s*"([0-9A-Fa-f]+)"\s*,\s*"tid"\s*:\s*(\d+)'
            match = re.search(patron, data)
            if match:
                uid, tid = match.groups()
                return f'{{"uid":"{uid}","tid":{int(tid)}}}'
            else:
                return ""
        
    def read_loop(self):
        while not self.stop_event.is_set():
            if self.ser is None:
                self.open_serial()
                time.sleep(1)
                continue
            
            if self.confirmation_flag == 0:
                data = self.safe_readline()
                if not data:
                    continue
                
                print(f"RX: {data}")
                try:
                    data = self.get_mesage(data)
                    datos = json.loads(data)
                    self.tid = datos.get("tid")
                    self.uid = datos.get("uid")
                    
                    self.confirmation_flag = 1
                        
                    print("Tarjeta Recibida")
                    print(f"UID: {self.uid} | TID: {self.tid}")
                    self.ser.reset_output_buffer()
                    
                except json.JSONDecodeError:
                    print("JSON invalido recibido")
                    continue
                except Exception as e:
                    print(f"Error procesando datos: {e}")
                    continue
                    
            time.sleep(0.005)
            
    def write_loop(self):
        
        while not self.stop_event.is_set():
            if self.client_flag == 1:
                time.sleep(0.5)
                print("----------------------Tarjeta Autorizada")
                mensaje = f'{{"rpt":2,"tm":{self.tid}}}\n'
                try:
                    with self.lock:
                        self.ser.write(mensaje.encode())
                        self.ser.flush() #Para que el mensaje se envie inmediatamente
                    print(f"TX: {mensaje.strip()}")
                    self.client_flag = 0
                except Exception as e:
                    print(f"Error al escribir: {e}")
                self.enable.clear()
                
            elif self.client_flag == 2:
                self.client_flag = 0
                time.sleep(0.5)
                mensaje = '{"rpt":2,"tm":0}\n'
                
            if self.confirmation_flag == 1:
                time.sleep(0.5)
                print("-----------------------Enviando Confirmacion")
                mensaje = f'{{"rpt":1,"tm":{self.tid}}}\n'
                try:
                    with self.lock:
                        self.ser.write(mensaje.encode())
                        self.ser.flush()
                    print(f"TX: {mensaje.strip()}")
                    self.confirmation_flag = 0
                    self.ser.reset_input_buffer()
                    self.uid_flag = 1
                except Exception as e:
                    print(f"Error al escribir: {e}")
                
                self.enable.clear()
                
            time.sleep(0.01)
                
    def start_threads(self):
        self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.write_thread = threading.Thread(target=self.write_loop,daemon=True)
        self.read_thread.start()
        self.write_thread.start()
        
    def stop(self):
        self.stop_event.set()
        if self.ser:
            self.ser.close()

pygame.init()
class Reader(QThread):
    signal = pyqtSignal(dict)
    nointernet = pyqtSignal(str)

    def __init__(self, serial_manager, parent=None):
        QThread.__init__(self, parent)
        self.serial_manager = serial_manager
        logging.info("Iniciando Reader...")
    
    def run(self):
        
        continue_reading = True        
        while continue_reading:
            if self.serial_manager.uid_flag == 1:
                self.serial_manager.uid_flag = 0 #reseteamos el flag
                
                # Sonido de Jhon Cena para tarjetas especificas
                logging.info("Tarjeta leida...")
                rfid = self.serial_manager.uid
                soundpath = "/home/pi/redlabgui/sounds/"
                song = "JohnCenaShort.wav" if rfid in ["97797673", '6F7161E5']  else "alert.wav"
                
                #song = "alert.wav"
                p = pygame.mixer.Sound(soundpath+song)
                p.play()
                time.sleep(0.001)
                
                if True:
                    if checkInternet.check():
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
                        print('triggering local db')
                        #self.nointernet.emit(rfid)
                else:
                    self.signal.emit({'a':123})


if __name__ == "__main__":
    
    # Testeo
    serial1 = SerialManager()
    serial1.start_threads()
    r = Reader(serial1)
    r.run()
