from PyQt6.QtWidgets import QMainWindow,QApplication, QLineEdit,QWidget, QLabel, QPushButton, QGraphicsView, QMenuBar, QStatusBar
from PyQt6 import uic
import sys
from Attempt2 import *

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        uic.loadUi('AlphaForRouterSearch.ui', self)
        
        #For info
        self.routers = []
        #Define the UI elements
        self.search_text = self.findChild(QLineEdit, 'lineEdit')
        self.searchButton=self.findChild(QPushButton, 'pushButton')
        self.nextButton=self.findChild(QPushButton, 'nextButton')
        self.model_title=self.findChild(QLabel, 'modelTitle')
        
        #Actions
        self.searchButton.clicked.connect(self.search)
        self.show()
        
    def search(self):
        self.routers=[]
        addFormatedItems(getHTMLtext(self.search_text.text()),self.routers)
        try:
            self.model_title.setText(self.routers[0].title)
        except:
            self.model_title.setText("No routers found")
createFolder("Images")     
#initiate the app
app = QApplication(sys.argv)
UIWindow = UI()


app.exec()

deleteImages()
