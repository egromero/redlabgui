import sys

import logging

# Configurar el logging
log_filepath = "./logs/main.log"

logging.basicConfig(
    filename=log_filepath,
    level=logging.DEBUG,  # Ajusta el nivel según tus necesidades (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.info("Iniciando aplicación...")

import reader
import gui

app = gui.QApplication(sys.argv)
mwin = gui.MWindow()
mwin.show()
sys.exit(app.exec_())