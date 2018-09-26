
# coding: utf-8

# In[1]:



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLabel, QGridLayout, QWidget,
                            QApplication, QPushButton, QDesktopWidget,
                            QMessageBox)
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt, QTimer, QThread
import time

#Training session popup
class trainingSession(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        letter = 0
        timerTime = QTimer(self)
        timerTime.timeout.connect(self.updateLetter)
        timerTime.start(1000)
    
        self.initUI()
        
    def initUI(self):
        
        centralWidget = qWidget(self)
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        
        self.resize(400, 300)        
        self.setWindowTitle('Training Session')
        self.show()
        
    def updateLetter(self):
        proctor = QLabel('Make the letter ' + str(alphabet[letter]),self)
        proctor.setAlignment(Qt.AlignCenter)
        gridLayout.addWidget(proctor, 0, 0)
        letter += 1
        
        

#class trainingLoop(QThread):
   # letterSignal = pyqtSignal(dict)
    #def __init__(self, parent=None)
     #   alphabet = ['a', 'b', 'c', 'd', 'e', 'f',
      #    'm', 'n', 'o', 'p', 'q', 'r',
       #   's', 't', 'u', 'v', 'w', 'x'
        # 'y', 'z']
        #super(trainingLoop, self).__init__(parent=parent)
        #letter = 0
        
   # def run(self):
        
        #while True:
                
        
        #for letter in alphabet:
         #   for r in range(5):
          #      proctor.setText("Make the letter " + letter +
           #                   " " + str(r))
            #    time.sleep(1)
class Collector(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)
        
        prompt = QLabel('Hello. Click Start to begin', self)
        prompt.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(prompt, 0, 0)
            
        start = QPushButton('Start', self)
        start.setToolTip('Begin taking data')
        start.move(150, 200)
        start.clicked.connect(self.train)
                
        #Geometry, Naming and positioning       
        self.resize(400, 300)        
        self.setWindowTitle('Data Collector')
        self.center()
        self.show()

    #Open Popup
    def train(self):
        self.w = trainingSession()
        self.w.show()
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

