import sys
import reader
import guipyqt



app = guipyqt.QApplication(sys.argv)
mwin = guipyqt.MWindow()
mwin.show()
sys.exit(app.exec_())