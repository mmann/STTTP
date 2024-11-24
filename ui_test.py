#This Python file tests some user interface (UI) functions in PyQt5
#https://www.riverbankcomputing.com/static/Docs/PyQt5/

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsPixmapItem, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QSize

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 100
        self.top = 200
        self.width = 520
        self.height = 520
        self.initUI()
  
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Create the boards picture
        # Create widget
        label = QLabel('Label')
        #pixmap = QtGui.QPixmap('board.png')
        pixmap = QtGui.QPixmap('board.jpeg')
        label.setPixmap(pixmap)
        #self.resize(pixmap.width(),pixmap.height())

        #vb = graphicsLayoutWidget.addViewBox(h,v)
        #vb.setFixedHeight(pixmap.height())
        #vb.setFixedWidth(pixmap.width())
        #vb.setDefaultPadding(0)
        #vb.setMouseEnabled(False,False)
        #vb.addItem(qpi)

        #Create buttons
        """ for j in range(9):#row number
            for i in range(9):#column number
                button = QPushButton('%d%d'%(i,j), self)
                button.setFixedSize(QSize(30, 30))
                button.setToolTip('This is an example button')
                button.move(100 + 30*i,70 + 30*j)
                button.clicked.connect(self.on_click)"""
        
        #Pop up the UI
        self.show() 

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())