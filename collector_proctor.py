# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_collector_proctor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.theLetter.setText("")
        self.theLetter.setObjectName("theLetter")

        self.retranslateUi(Proctor)
        QtCore.QMetaObject.connectSlotsByName(Proctor)

    def retranslateUi(self, Proctor):
        _translate = QtCore.QCoreApplication.translate
        Proctor.setWindowTitle(_translate("Proctor", "Proctor"))
        self.makeLetter.setText(_translate("Proctor", "Make the letter:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Proctor = QtWidgets.QDialog()
    ui = Ui_Proctor()
    ui.setupUi(Proctor)
    Proctor.show()
    sys.exit(app.exec_())

