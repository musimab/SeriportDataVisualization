# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Arge2/Desktop/SeriPort-main/pythonSerial/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBoxSeriaPortLists = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxSeriaPortLists.setObjectName("comboBoxSeriaPortLists")
        self.gridLayout.addWidget(self.comboBoxSeriaPortLists, 0, 0, 1, 1)
        self.comboBoxBaudRates = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxBaudRates.setObjectName("comboBoxBaudRates")
        self.gridLayout.addWidget(self.comboBoxBaudRates, 0, 1, 1, 1)
        self.pushButton_connect = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.gridLayout.addWidget(self.pushButton_connect, 0, 2, 1, 1)
        self.pushButton_disconnect = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.gridLayout.addWidget(self.pushButton_disconnect, 0, 3, 1, 1)
        self.pushButton_open = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_open.setObjectName("pushButton_open")
        self.gridLayout.addWidget(self.pushButton_open, 1, 2, 1, 1)
        self.pushButton_send = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_send.setObjectName("pushButton_send")
        self.gridLayout.addWidget(self.pushButton_send, 1, 3, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_clear = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.verticalLayout_2.addWidget(self.pushButton_clear)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkbox_save_txt = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkbox_save_txt.setObjectName("checkbox_save_txt")
        self.horizontalLayout_2.addWidget(self.checkbox_save_txt)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_enter_command = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_enter_command.setObjectName("lineEdit_enter_command")
        self.verticalLayout.addWidget(self.lineEdit_enter_command)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_3.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Device "))
        self.pushButton_connect.setText(_translate("MainWindow", "connect"))
        self.pushButton_disconnect.setText(_translate("MainWindow", "disconnect"))
        self.pushButton_open.setText(_translate("MainWindow", "open"))
        self.pushButton_send.setText(_translate("MainWindow", "send"))
        self.label_2.setText(_translate("MainWindow", "File path"))
        self.pushButton_clear.setText(_translate("MainWindow", "clear"))
        self.checkbox_save_txt.setText(_translate("MainWindow", "Save txt"))
        self.label.setText(_translate("MainWindow", "Command"))

