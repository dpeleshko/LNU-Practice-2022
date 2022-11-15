from PyQt6.QtWidgets import QTextEdit,QTextBrowser, QRadioButton, QCheckBox, QMainWindow,QApplication, QLineEdit,QWidget, QLabel, QPushButton, QGraphicsView, QMenuBar, QStatusBar, QGraphicsItem, QGraphicsPixmapItem
from PyQt6 import uic
import sys
from Attempt2 import *
from PyQt6.QtGui import QPixmap, QImage,QIcon

class ItemWindow(QMainWindow):
    def __init__(self,routers,i, MainWindow):#index of router
        super(ItemWindow,self).__init__()
        self.setWindowTitle("Router Search")
        self.setWindowIcon(QIcon("logo.png"))
        
        uic.loadUi("ModelPage.ui",self)
        self.main = MainWindow
        self.item = routers[i]
        self.returnButton = self.findChild(QPushButton,"returnButton")
        self.image = self.findChild(QLabel,"image")
        self.search_button = self.findChild(QPushButton,"searchButton")
        self.model_title = self.findChild(QLabel,"modelTitle")
        self.av_stars = self.findChild(QLabel,"avStars")
        self.key_words = self.findChild(QLineEdit,"keyWords")
        self.is_long = self.findChild(QCheckBox, 'isLong')
        self.text_review = self.findChild(QTextEdit,"textReview")
        self.stars = []
        for j in range(5):
            self.stars.append(self.findChild(QRadioButton, f'star{j+1}'))
        #Actions
        self.search_button.clicked.connect(self.searchReview)
        self.returnButton.clicked.connect(self.returnToMain)
        self.image.setPixmap(QPixmap(self.item.image_path))
        self.model_title.setText(self.item.title)
        self.av_stars.setText(str(self.item.av_stars))
        self.show()
    
    def searchReview(self):
        key_words = self.key_words.text()
        stars = None
        for i in range(5):
            if self.stars[i].isChecked():
                stars = i+1
        is_long = self.is_long.isChecked()
        review = self.item.getReviewFromCriterias(key_words, stars, is_long)
        if review:
            self.text_review.setPlainText(review.comment)
        else:
            self.text_review.setPlainText("No review found")
    def returnToMain(self):
        self.main.show()
        self.hide()
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        uic.loadUi('AlphaForRouterSearch.ui', self)
        
        self.setWindowTitle("Router Search")
        self.setWindowIcon(QIcon("logo.png"))
        #Define the UI elements
        self.search_text = self.findChild(QLineEdit, 'lineEdit')
        self.searchButton=self.findChild(QPushButton, 'pushButton')
        self.nextButton=self.findChild(QPushButton, 'nextButton')
        self.model_title=self.findChild(QLabel, 'modelTitle')
        self.previousButton=self.findChild(QPushButton, 'previousButton')
        self.image = self.findChild(QLabel, 'image')
        self.changeWindowButton = self.findChild(QPushButton, 'changeWindowButton')
        
        #For tracking
        self.routers=[]
        self.i=0
        
        #self.image=self.findChild(QGraphicsView, 'imageView')
        
        #Actions
        self.searchButton.clicked.connect(self.search)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)
        self.changeWindowButton.clicked.connect(self.changeWindow)
        #self.image.mouseReleaseEvent = self.changeWindow()
        self.show()
    
    def changeWindow(self):
        if len(self.routers)==0:
            return
        self.routers[self.i].downloadReviews()
        self.itemWindow = ItemWindow(self.routers,self.i,self)
        self.itemWindow.show()
        self.hide()
    def previous(self):
        if len(self.routers)==0:
            return
        try:
            self.i-=1
            if(self.i<0):
                self.i=len(self.routers)-1
            self.showRouter(self.i)
        except:
            self.noRoutersFound()
            pass
        
    def noRoutersFound(self):
        self.model_title.setText("No routers found")
        self.pixmap = QPixmap("crying_cat.jpg")
        self.image.setPixmap(self.pixmap)
        
    def showRouter(self,i):
        self.model_title.setText(self.routers[i].title)
        self.pixmap = QPixmap(self.routers[i].image_path)
         #add pixmap to label
        self.image.setPixmap(self.pixmap)
        
    def next(self):
        if len(self.routers)==0:
            return
        try:
            self.i+=1
            if(self.i>=len(self.routers)):
                self.i=0
            self.showRouter(self.i)
        except:
            self.noRoutersFound()
    def search(self):
        self.routers = []
        URL = "https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q="+formatingSearch(self.search_text.text())
        addFormatedItems(getHTMLtext(URL),self.routers)
        try:
            self.model_title.setText(self.routers[0].title)
            self.showRouter(0)
        except:
            self.noRoutersFound()
        
        
createFolder("Images")     
#initiate the app
app = QApplication(sys.argv)
UIWindow = MainWindow()

# search_text = "Xiaomi 4A"
# URL = "https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q="+formatingSearch(search_text)
# routers = []
# addFormatedItems(getHTMLtext(URL),routers)
# routers[0].downloadReviews()
# form = ItemWindow(routers,0,UIWindow)

app.exec()

deleteImages()
