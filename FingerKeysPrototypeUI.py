# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FingerKeysPrototypeUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self,text):
        self.newText.emit(str(text))
        
class Ui_FingerKeys(object):
    def setupUi(self, FingerKeys):
        FingerKeys.setObjectName("FingerKeys")
        FingerKeys.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(FingerKeys)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.AutoComplete1 = QtWidgets.QPushButton(self.centralwidget)
        self.AutoComplete1.setObjectName("AutoComplete1")
        self.verticalLayout.addWidget(self.AutoComplete1)
        self.Autocomplete2 = QtWidgets.QPushButton(self.centralwidget)
        self.Autocomplete2.setObjectName("Autocomplete2")
        self.verticalLayout.addWidget(self.Autocomplete2)
        self.Autocomplete3 = QtWidgets.QPushButton(self.centralwidget)
        self.Autocomplete3.setObjectName("Autocomplete3")
        self.verticalLayout.addWidget(self.Autocomplete3)
        self.Autocomplete4 = QtWidgets.QPushButton(self.centralwidget)
        self.Autocomplete4.setObjectName("Autocomplete4")
        self.verticalLayout.addWidget(self.Autocomplete4)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.fontComboBox = QtWidgets.QFontComboBox(self.centralwidget)
        self.fontComboBox.setObjectName("fontComboBox")
        self.gridLayout_2.addWidget(self.fontComboBox, 0, 0, 1, 1)
        FingerKeys.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FingerKeys)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        FingerKeys.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FingerKeys)
        self.statusbar.setObjectName("statusbar")
        FingerKeys.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(FingerKeys)
        self.actionLoad.setObjectName("actionLoad")
        self.actionOpen = QtWidgets.QAction(FingerKeys)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(FingerKeys)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(FingerKeys)
        QtCore.QMetaObject.connectSlotsByName(FingerKeys)

        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self,text):
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__

    def retranslateUi(self, FingerKeys):
        _translate = QtCore.QCoreApplication.translate
        FingerKeys.setWindowTitle(_translate("FingerKeys", "Finger Keys"))
        self.AutoComplete1.setText(_translate("FingerKeys", "Autocomplete 1"))
        self.Autocomplete2.setText(_translate("FingerKeys", "Autocomplete 2"))
        self.Autocomplete3.setText(_translate("FingerKeys", "Autocomplete 3"))
        self.Autocomplete4.setText(_translate("FingerKeys", "Autocomplete 4"))
        self.menuFile.setTitle(_translate("FingerKeys", "File"))
        self.actionLoad.setText(_translate("FingerKeys", "Load"))
        self.actionOpen.setText(_translate("FingerKeys", "Open"))
        self.actionSave.setText(_translate("FingerKeys", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FingerKeys = QtWidgets.QMainWindow()
    ui = Ui_FingerKeys()
    ui.setupUi(FingerKeys)
    FingerKeys.show()
    sys.exit(app.exec_())

