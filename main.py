import sys
import os

#script_dir = os.path.dirname(os.path.abspath(__file__))
#os.chdir(script_dir)

import logging

# Configurar el logging
log_dir = "/home/pi/redlabgui/logs"
os.makedirs(log_dir, exist_ok=True)

log_filepath = os.path.join(log_dir, "main.log")

logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,  # Ajusta el nivel según tus necesidades (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.info("Iniciando aplicación...")

import reader
import gui

#logging.info("AAAAAAAAAAAAAAAAAAAAAAAAA")
app = gui.QApplication(sys.argv)
#logging.info("BBBBBBBBBBBBBBBBBBBBBBBBB")
mwin = gui.MWindow()
#loggin.info("CCCCCCCCCCCCCCCCCCCCCCCCCC")
mwin.show()
sys.exit(app.exec_())