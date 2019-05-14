# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cctv.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import glob
import cv2
import re

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    def __init__(self):
        self.duration = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 40, 321, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(3, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(70, 330, 96, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(70, 360, 96, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(70, 390, 96, 22))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 320, 97, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 85, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 220, 181, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 85, 151, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 300, 161, 17))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(410, 50, 81, 31))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 190, 39, 27))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(150, 190, 39, 27))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 190, 39, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(80, 200, 16, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 200, 21, 17))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(190, 200, 21, 17))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(350, 200, 16, 17))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(310, 190, 39, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(400, 200, 21, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 220, 181, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_5 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(360, 190, 39, 27))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(420, 190, 39, 27))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(460, 200, 21, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayoutWidget.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.checkBox_3.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.textBrowser.raise_()
        self.lineEdit_3.raise_()
        self.lineEdit_4.raise_()
        self.lineEdit.raise_()
        self.label_5.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.lineEdit_2.raise_()
        self.label_10.raise_()
        self.label_3.raise_()
        self.lineEdit_5.raise_()
        self.lineEdit_6.raise_()
        self.label_11.raise_()
        self.comboBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuCCTV_Video_Summarizer = QtGui.QMenu(self.menubar)
        self.menuCCTV_Video_Summarizer.setObjectName(_fromUtf8("menuCCTV_Video_Summarizer"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuCCTV_Video_Summarizer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CCTVVS", None))
        # MainWindow.setStyleSheet("background-color : #e8ebef;")
        self.comboBox.setItemText(0, _translate("MainWindow", "Kriyakalpa", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Intersection", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "CSE Entrance", None))
        self.checkBox.setText(_translate("MainWindow", "Person", None))
        self.checkBox_2.setText(_translate("MainWindow", "Motorbike", None))
        self.checkBox_3.setText(_translate("MainWindow", "Car", None))
        self.pushButton.setText(_translate("MainWindow", "Generate", None))
        self.label.setText(_translate("MainWindow", "Select File name ", None))
        self.label_2.setText(_translate("MainWindow", "Enter start time", None))
        self.label_4.setText(_translate("MainWindow", "Length of input video", None))
        self.label_6.setText(_translate("MainWindow", "Select required objects", None))
        self.label_5.setText(_translate("MainWindow", "h", None))
        self.label_7.setText(_translate("MainWindow", "m", None))
        self.label_8.setText(_translate("MainWindow", "s", None))
        self.label_9.setText(_translate("MainWindow", "h", None))
        self.label_10.setText(_translate("MainWindow", "m", None))
        self.label_3.setText(_translate("MainWindow", "Enter end time", None))
        self.label_11.setText(_translate("MainWindow", "s", None))

        #setting input validations for time
        # regex = QtCore.QRegExp("[0-5][0-9] | [6][0]")
        # self.validator = QtGui.QRegExpValidator(regex,self)
        self.validator = QtGui.QIntValidator()
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setMaxLength(2)
        self.lineEdit_3.setValidator(self.validator)
        self.lineEdit_3.setMaxLength(2)
        self.lineEdit_4.setValidator(self.validator)
        self.lineEdit_4.setMaxLength(2)
        self.lineEdit_2.setValidator(self.validator)
        self.lineEdit_2.setMaxLength(2)
        self.lineEdit_5.setValidator(self.validator)
        self.lineEdit_5.setMaxLength(2)
        self.lineEdit_6.setValidator(self.validator)
        self.lineEdit_6.setMaxLength(2)

        self.menuCCTV_Video_Summarizer.setTitle(_translate("MainWindow", "CCTV Video Summarizer", None))

    def set_combobox(self):
        """
        Get filenames from directory and assign them to dropdown(combobox)
        """
        filenames = glob.glob('./*.mp4')
        j = 0
        ui = Ui_MainWindow()
        print(filenames)
        for i in filenames:
            self.comboBox.setItemText(j, _translate("MainWindow", i[2:], None))
            j += 1
        # print(self.comboBox.currentIndex())
        if self.comboBox.activated.connect(self.cal_length):
            print(self.comboBox.currentIndex())

    def cal_length(self):
        """
        To calculate video length of input video using number of frames and fps.
        """
        x = self.comboBox.currentIndex()
        text = str(self.comboBox.currentText())
        cap = cv2.VideoCapture("./{}".format(text))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = frame_count/fps
        dur = self.duration
        # print(duration)
        self.hour = dur / 3600
        dur = dur % 3600
        self.minute = dur / 60
        dur = dur % 60
        self.sec = dur
        time = "{}:{}:{}".format(int(self.hour),int(self.minute),int(self.sec))
        print(time)
        self.textBrowser.setText(time)

    def press_generate(self):
        """
        1. Check if the entered start and end times are valid. If not, display a pop-up message.
        2. Selects the checked tags.
        """


        #start time
        h1 = self.lineEdit.text()
        m1 = self.lineEdit_3.text()
        sec1 = self.lineEdit_4.text()

        #end time
        h2 = self.lineEdit_2.text()
        m2 = self.lineEdit_5.text()
        sec2 = self.lineEdit_6.text()

        start_in_sec = int(h1) * 3600 + int(m1) * 60 + int(sec1)
        end_in_sec = int(h2) * 3600 + int(m2) * 60 + int(sec2)
        len_entered = end_in_sec - start_in_sec

        self.popup = QtGui.QWidget()

        if int(h1) > self.hour:
            warning = QtGui.QMessageBox.warning(self.popup, "Message", "Start time greater than length of video!")
        elif len_entered > self.duration:
            warning = QtGui.QMessageBox.warning(self.popup, "Message", "Entered length bigger than video length!")
        elif (h2 < h1) or (h2 == h1 and m2 < m1) or (h2 == h1 and m2 == m1 and sec2 < sec1):
            warning = QtGui.QMessageBox.warning(self.popup, "Message", "Start time greater than end time!")
        else:
            print("Correctly entered")

        tags = []
        #selecting tags from checkboxes
        if self.checkBox.isChecked() == True:
            tags.append(self.checkBox.text())
        if self.checkBox_2.isChecked() == True:
            tags.append(self.checkBox_2.text())
        if self.checkBox_3.isChecked() == True:
            tags.append(self.checkBox_3.text())

        print(tags)

        # then use these tags to select tubes stored in the real-time phase.






if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.set_combobox()
    ui.cal_length()
    ui.pushButton.clicked.connect(lambda:ui.press_generate())
    sys.exit(app.exec_())

