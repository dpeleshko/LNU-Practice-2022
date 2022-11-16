from PyQt6.QtWidgets import QStackedWidget ,QTextEdit,QTextBrowser, QRadioButton, QCheckBox, QMainWindow,QApplication, QLineEdit,QWidget, QLabel, QPushButton, QGraphicsView, QMenuBar, QStatusBar, QGraphicsItem, QGraphicsPixmapItem
from PyQt6 import uic
import sys
from Attempt2 import *
from PyQt6.QtGui import QPixmap, QImage,QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        uic.loadUi("UI.ui",self)
        
        self.setWindowTitle("Router Search")
        self.setWindowIcon(QIcon("logo.png"))
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
        self.search_text.returnPressed.connect(self.search)
        # self.nextButton.clicked.connect(self.next)
        # self.previousButton.clicked.connect(self.previous)
        # self.changeWindowButton.clicked.connect(self.changeWindow)
        self.central_widget = self.findChild(QStackedWidget,"stackedWidget")
        self.homePage()
        #Define the UI elements
        
    def searchReview(self):
        key_words = self.key_words.text()
        is_long = self.is_long.isChecked()
        stars = None
        if self.allstars.isChecked():
            self.reviews = self.item.getReviewFromCriterias(key_words, None, is_long)
        else:
            for i in range(5):
                if self.stars[i].isChecked():
                    stars = i+1
                    break
            self.reviews = self.item.getReviewFromCriterias(key_words, stars, is_long)
        self.review_index = 0
        if self.reviews:
            self.nextReviewButton.clicked.connect(self.nextReview)
            self.previousReviewButton.clicked.connect(self.previousReview)
            self.showReview(self.reviews, self.review_index)
           # self.star_ico_review.setHidden(False)
        else:
            self.noReview()
    def showReview(self,reviews,index):
        self.username.setText(reviews[index].username)
        self.star_user.setText(str(reviews[index].stars))
        self.text_review.setPlainText(reviews[index].comment)
        #self.star_ico_review.setHidden(False)
    def nextReview(self):
        if len(self.reviews)==0:
            return
        try:
            self.review_index+=1
            if(self.review_index>=len(self.reviews)):
                self.review_index=0
            self.showReview(self.reviews,self.review_index)
        except:
            self.noReview()
    def previousReview(self):
        if len(self.reviews)==0:
            return
        try:
            self.review_index-=1
            if(self.review_index<0):
                self.review_index=len(self.reviews)-1
            self.showReview(self.reviews,self.review_index)
        except:
            self.noReview()
    def returnToMain(self):
        self.homePage()
        
    def homePage(self):
        #uic.loadUi('AlphaForRouterSearch.ui', self)
        self.central_widget.setCurrentWidget(self.findChild(QWidget,"home_page"))
    def noReview(self):
        self.text_review.setPlainText("No review found")
        self.username.setText("")
        self.star_user.setText("")
        #self.image.mouseReleaseEvent = self.changeWindow()
        #self.show()
    def itemPage(self):
        # super(ItemWindow,self).__init__()
        # self.setWindowTitle("Router Search")
        # self.setWindowIcon(QIcon("logo.png"))
        
        self.central_widget.setCurrentWidget(self.findChild(QWidget,"item_page"))
        #self.main = MainWindow
        self.item = self.routers[self.i]
        self.returnButton = self.findChild(QPushButton,"returnButton")
        self.image2 = self.findChild(QLabel,"image_2")
        self.search_button = self.findChild(QPushButton,"searchButton")
        self.model_title2 = self.findChild(QLabel,"modelTitle_2")
        self.av_stars = self.findChild(QLabel,"avStars")
        self.key_words = self.findChild(QLineEdit,"keyWords")
        self.is_long = self.findChild(QCheckBox, 'isLong')
        self.text_review = self.findChild(QTextEdit,"textReview")
        self.username = self.findChild(QLabel,"usernameReview")
        self.star_user = self.findChild(QLabel,"starReview")
        self.star_ico_review = self.findChild(QLabel,"starIcoReview")
        self.nextReviewButton = self.findChild(QPushButton,"nextReviewButton")
        self.previousReviewButton = self.findChild(QPushButton,"previousReviewButton")
        self.allstars = self.findChild(QRadioButton,"starAll")
        self.stars = []
        for j in range(5):
            self.stars.append(self.findChild(QRadioButton, f'star{j+1}'))
        #Actions
        self.key_words.returnPressed.connect(self.searchReview)
        self.search_button.clicked.connect(self.searchReview)
        self.returnButton.clicked.connect(self.returnToMain)
        self.image2.setPixmap(QPixmap(self.item.image_path))
        self.model_title2.setText(self.item.title)
        self.av_stars.setText(str(self.item.av_stars))
        self.noReview()
        self.text_review.setPlainText("")
        #self.star_ico_review.setHidden(True)
        #self.show()
    
    def changeWindow(self):
        if len(self.routers)==0:
            return
        self.routers[self.i].downloadReviews()
        self.itemPage()
        
        #self.hide()
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
            self.nextButton.clicked.connect(self.next)
            self.previousButton.clicked.connect(self.previous)
            self.changeWindowButton.clicked.connect(self.changeWindow)
        except:
            self.noRoutersFound()
        

if __name__ == "__main__":
    createFolder("Images")
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    # routers = []
    # home_page = MainWindow(routers)
    # item_page = ItemWindow(routers,0,)
    
    # window_stack = QStackedWidget()
    # window_stack.addWidget(home_page)
    # window_stack.addWidget(item_page)
    # home_page.changeWindowButton.clicked.connect(lambda: window_stack.setCurrentIndex(1))
    
    # window_stack.show()
    app.exec()
    
    deleteImages()
# createFolder("Images")     
# #initiate the app

# app = QApplication(sys.argv)
# UIWindow = MainWindow()

# # search_text = "Xiaomi 4A"
# # URL = "https://hotline.ua/ua/computer/besprovodnoe-oborudovanie/?q="+formatingSearch(search_text)
# # routers = []
# # addFormatedItems(getHTMLtext(URL),routers)
# # routers[0].downloadReviews()
# # form = ItemWindow(routers,0,UIWindow)

# app.exec()

# deleteImages()
