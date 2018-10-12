
# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLabel, QGridLayout, QWidget,
                            QApplication, QPushButton, QDesktopWidget,
                            QMessageBox, QLineEdit)
import PyQt5.QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt, QTimer, QThread

sys.path.insert(0, './Leap_asl_Andrew_Windows')
from LEAP_Controler import read_char
import time

#class proctor(QWidget):
#
#    def __init__(self):
#        QWidget.__init__(self)
#    
#        self.initUI()
#        
#    def initUI(self):
#        
#        centralWidget = QWidget(self)
#        #self.setCentralWidget(centralWidget)
#        
#        gridLayout = QGridLayout(self)
#        
#        centralWidget.setLayout(gridLayout)
#        text =0
#        self.resize(400, 300)        
#        self.setWindowTitle('Make the gesture for ' + str(text))
#        
#        proctorLabel = QLabel("Make the letter " + str(text), self)
#        proctorLabel.setAlignment(QtCore.Qt.AlignCenter)
#        gridLayout.addWidget(proctorLabel, 0, 0)
#        
#        self.show()

class Collector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qle = None
        self.initUI()
        
    def initUI(self):
        text=0
        centralWidget = QWidget(self)
        
        
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        #this is just below the text box
        prompt = QLabel('hit any keys(A-Z) to start the Collecting data', self)
        prompt.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(prompt, 0, 0)
        

        #this setup the label that the program will learn
        #self.lbl = QLabel("hit any key to start the Collecting data",self)
        #self.lbl.move(73, 70)
        #self.lbl2 = QLabel(,self)
       # self.lbl2.move(155, 148)
        
        #Qle controls the texbox
        qle = QLineEdit('Ready?',self)        
        qle.move(155, 170)
        qle.textChanged[str].connect(self.onChanged)
        
        
       
                
        #Geometry, Naming and positioning       
        self.resize(400, 300)        
        self.setWindowTitle('Data Collector')
        self
        self.center()
        self.show()
        read_char(text)
    #Action taken on changed text
    def onChanged(self, text):
        
       
       
        #self.lbl2.setText(text)       
        read_char(text)
       
       # self.w.close()
        
    
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

