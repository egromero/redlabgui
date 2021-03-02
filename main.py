import sys
import reader
import gui

app = gui.QApplication(sys.argv)
mwin = gui.MWindow()
mwin.show()
sys.exit(app.exec_())