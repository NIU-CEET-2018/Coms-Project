
# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLabel, QGridLayout, QWidget,
                            QApplication, QPushButton, QDesktopWidget,
                            QMessageBox, QLineEdit)
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt, QTimer, QThread
# sys.path.insert(0, './Leap_asl_Andrew_Windows')
from LEAP_Controler import read_char
import time

class proctor(QWidget):

    def __init__(self):
        QWidget.__init__(self)
    
        self.initUI()
        
    def initUI(self):
        
        centralWidget = qWidget(self)
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        
        self.resize(400, 300)        
        self.setWindowTitle('Make the gesture for ' + str(text))
        
        proctorLabel = QLabel("Make the letter " + str(text), self)
        proctorLabel.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(proctorLabel, 0, 0)
        
        self.show()
        

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qle = None
        self.initUI()
        
    def initUI(self):
        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        
        prompt = QLabel('Enter a letter', self)
        prompt.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(prompt, 0, 0)
            
        self.qle = QLineEdit(self)
        self.qle.setAlignment
        
        self.qle.textChanged[str].connect(self.onChanged)
        
        
        
        #qle.textChanged[str].connect(self.onChanged)
                
        #Geometry, Naming and positioning       
        self.resize(400, 300)        
        self.setWindowTitle('Data Collector')
        self.center()
        self.show()

    #Action taken on changed text
    def onChanged(self, text):
               
        self.w = proctor()
        self.w.show()
        
        read_char(text)
        self.w.close()
        
        QLineEdit.clear(self.qle)


    #closeEvent
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    
     #Centers the window on the screen           
    def center(self):
        
        qr = self.frameGeometry()
        
        #Finds the center of the screen from QDesktopWidget
        cp = QDesktopWidget().availableGeometry().center()
        
        #Centers on the center of the screen
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    collector = Collector()
    collector.show()
    sys.exit(app.exec_())

