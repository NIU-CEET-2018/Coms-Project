
# coding: utf-8

# In[6]:


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QLabel, QGridLayout, QWidget,
                            QApplication, QPushButton, QDesktopWidget,
                            QMessageBox, QLineEdit, QDialog)
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize, Qt, QTimer, QThread
import time

class Ui_Proctor(object):
    def setupUi(self, Proctor):
        Proctor.setObjectName("Proctor")
        Proctor.resize(300, 156)
        Proctor.setAutoFillBackground(True)
        self.makeLetter = QtWidgets.QLabel(Proctor)
        self.makeLetter.setGeometry(QtCore.QRect(80, 70, 91, 20))
        self.makeLetter.setAlignment(QtCore.Qt.AlignCenter)
        self.makeLetter.setObjectName("makeLetter")
        self.theLetter = QtWidgets.QLabel(Proctor)
        self.theLetter.setGeometry(QtCore.QRect(170, 73, 47, 20))
        self.theLetter.setText(str(text))
        self.theLetter.setObjectName("theLetter")

        self.retranslateUi(Proctor)
        QtCore.QMetaObject.connectSlotsByName(Proctor)

    def retranslateUi(self, Proctor):
        _translate = QtCore.QCoreApplication.translate
        Proctor.setWindowTitle(_translate("Proctor", "Proctor"))
        self.makeLetter.setText(_translate("Proctor", "Make the letter:")
        

class Collector(QMainWindow):
    def setupUi(self, Collector):
        Collector.setObjectName("MainWindow")
        Collector.resize(385, 207)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.prompt = QtWidgets.QLabel(self.centralwidget)
        self.prompt.setGeometry(QtCore.QRect(80, 80, 231, 20))
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setObjectName("prompt")
        self.letterInput = QtWidgets.QLineEdit(self.centralwidget)
        self.letterInput.setGeometry(QtCore.QRect(170, 110, 51, 20))
        self.letterInput.setObjectName("letterInput")
        Collector.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        Collector.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        letterInput.textChanged[str].connect(self.onChanged)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.prompt.setText(_translate("MainWindow", "Enter the letter you want to collect data on:"))
        
    def onChanged(self, text):
        self.w = Proctor()
        self.w.show()
                                
        QLineEdit.clear(self)
                                
     #closeEvent
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

