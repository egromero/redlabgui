from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QWidget,  QMessageBox
from PyQt5.QtTest import QTest
from functools import partial
from itertools import cycle



class LocalW(QMainWindow):
    def __init__(self, rfid):
        super(LocalW, self).__init__()
        self.rfid = rfid
        self.setup_init()
    
    def setup_init(self):
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.nointernet= QLabel()
        self.nointernet.setText("NO HAY CONEXIÓN A INTERNET DISPONIBLE")
        self.nointernet.setStyleSheet("background: red; color:white;")
        self.nointernet.setAlignment(QtCore.Qt.AlignCenter)
        self.generalLayout.addWidget(self.nointernet)
        self.labeltitle = QLabel()
        self.generalLayout.addWidget(self.labeltitle)
        self.labeltitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labeltitle.setText("RFID:%s\nIngrese su RUN"%self.rfid)
        self._createDisplay()
        self._createButtons()
        self.popUpMsj = QMessageBox()
        self.popUpMsj.setWindowTitle("Error!")
        self.popUpMsj.setIcon(QMessageBox.Critical)
        self.controller = Controller(self)


    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setAlignment(QtCore.Qt.AlignCenter)
        self.display.setStyleSheet("font-size: 40px;")
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {'1': (0, 0),
                   '2': (0, 1),
                   '3': (0, 2),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '7': (2, 0),
                   '8': (2, 1),
                   '9': (2, 2),
                   '0': (3, 1),
                   'K': (3, 2),
                   'Enviar': (3, 4),
                   'Borrar': (0, 3)
                  }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(130, 50)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')
    
    def send(self):
        run = self.display.text()
        if self.checkRun(run):
            self.setDisplayText(run[:-1]+'-'+run[-1])
        else:
            self.popUpMsj.setText("RUT no valido.")
            self.popUpMsj.exec_()
            self.clearDisplay()


    def checkRun(self, run):
        if len(run)>9:
            return False
        run = run.upper()
        run = run.replace("-","")
        run = run.replace(".","")
        aux = run[:-1]
        dv = run[-1:]
        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11

        if str(res) == dv:
            return True
        elif dv=="K" and res==10:
            return True
        else:
            return False
        

class Controller:
    def __init__(self, view):
        self._view = view
        self._connectSignals()

    def _buildExpression(self, sub_exp):
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'Borrar', 'Enviar'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        self._view.buttons['Enviar'].clicked.connect(self._view.send)
        self._view.buttons['Borrar'].clicked.connect(self._view.clearDisplay)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mwin = LocalW('A')
    mwin.show()
    sys.exit(app.exec_())