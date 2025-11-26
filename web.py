from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebKitWidgets import QWebView , QWebPage
import sys
class Browser(QWebView):
    def __init__(self):
        self.view = QWebView.__init__(self)

    def load(self,url):
        self.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Browser()  
    view.showMaximized()
    view.load("https://google.com")
    app.exec_()
