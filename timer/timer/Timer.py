#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
from threading import Thread
import sys

class Timer(QDialog):
    timeout = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.time=0
        self.timeInterval = 1000 #默认秒

        self.timerUp = QTimer()
        self.timerUp.setInterval(self.timeInterval)
        self.timerUp.timeout.connect(self.updateUptime)

        self.timerDown = QTimer()
        self.timerDown.setInterval(self.timeInterval)
        self.timerDown.timeout.connect(self.updateDowntime)

        self.initUi()

        self.buttonStart.clicked.connect(self.timerUp.start)
        self.buttonStop.clicked.connect(self.timerUp.stop)
        self.buttonReset.clicked.connect(self.reset)
        self.buttonCountDown.clicked.connect(self.timerDown.start)
        self.buttonStopAlarm.clicked.connect(self.timerDown.stop)
        self.timeSpinBox.valueChanged.connect(self.settimer)


    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.groupBox = QGroupBox("unit")
        self.radioButton1 = QRadioButton("s")
        self.radioButton1.toggled.connect(self.setUnit)
        self.radioButton2 = QRadioButton("0.1s")
        self.radioButton2.toggled.connect(self.setUnit)
        self.radioButton3 = QRadioButton("0.01s")
        self.radioButton3.toggled.connect(self.setUnit)
        self.radioButton4 = QRadioButton("1ms")
        self.radioButton4.toggled.connect(self.setUnit)
        self.radioButton1.setChecked(True)
        self.unitLayout = QHBoxLayout()
        self.unitLayout.addWidget(self.radioButton1)
        self.unitLayout.addWidget(self.radioButton2)
        self.unitLayout.addWidget(self.radioButton3)
        self.unitLayout.addWidget(self.radioButton4)
        self.groupBox.setLayout(self.unitLayout)
        mainLayout.addWidget(self.groupBox)

        self.buttonStart = QPushButton(self.tr("start"))
        mainLayout.addWidget(self.buttonStart)


        self.buttonStop = QPushButton(self.tr("stop"))
        mainLayout.addWidget(self.buttonStop)

        self.timeViewer = QLCDNumber()
        self.timeViewer.setFixedHeight(45)
        mainLayout.addWidget(self.timeViewer)

        self.timeForHuman = QLabel()
        mainLayout.addWidget(self.timeForHuman)


        self.buttonReset = QPushButton(self.tr("reset"))
        mainLayout.addWidget(self.buttonReset)

        self.timeSpinBox = QSpinBox()
        self.timeSpinBox.setRange(0,10000)
        mainLayout.addWidget(self.timeSpinBox)
        self.buttonCountDown = QPushButton(self.tr("countdown"))
        mainLayout.addWidget(self.buttonCountDown)
        self.buttonStopAlarm = QPushButton(self.tr("stopalarm"))
        mainLayout.addWidget(self.buttonStopAlarm)



    def setUnit(self):
        if self.radioButton1.isChecked():
            self.timeInterval = 1000
        elif self.radioButton2.isChecked():
            self.timeInterval = 100
        elif self.radioButton3.isChecked():
            self.timeInterval = 10
        elif self.radioButton1.isChecked():
            self.timeInterval = 1
        self.timerUp.setInterval(self.timeInterval)
        self.timerDown.setInterval(self.timeInterval)


    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)
        print(self.time)

    def updateDowntime(self):
        self.time =self.time-1
        self.settimer(self.time)
        print(self.time)
        if self.time == 0:
            self.timeout.emit()


    def settimer(self,int):
        self.time=int
        self.timeViewer.display(self.time)

        if self.timeInterval ==1000:
            self.timeForHuman.setText(time.strftime('%H hour %M minute %S second',time.gmtime(self.time)))
        elif self.timeInterval ==100:
            self.timeForHuman.setText(time.strftime('%H hour %M minute %S second',time.gmtime(self.time/10)))
        elif self.timeInterval ==10:
            self.timeForHuman.setText(time.strftime('%H hour %M minute %S second',time.gmtime(self.time/100)))
        elif self.timeInterval ==1:
            self.timeForHuman.setText(time.strftime('%H hour %M minute %S second',time.gmtime(self.time/1000)))


    def reset(self):
        self.time=0
        self.settimer(self.time)

if sys.platform == "win32":
    import winsound
    def beep(a,b):
        '''make a sound , ref: http://stackoverflow.com/questions/16573051/python-sound-alarm-when-code-finishes
        you need install  ``apt-get install sox``

        :param a: frenquency
        :param b: duration

        create a background thread,so this function does not block the main program
        '''
        def _beep(a,b):
            winsound.Beep(a,b*1000)
        thread = Thread(target=_beep,args=(a,b))
        thread.daemon = True
        thread.start()

elif sys.platform == 'linux':
    def beep(a,b):
        '''make a sound , ref: http://stackoverflow.com/questions/16573051/python-sound-alarm-when-code-finishes
        you need install  ``apt-get install sox``

        :param a: frenquency
        :param b: duration

        create a background thread,so this function does not block the main program
        '''
        import os
        def _beep(a,b):
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (b,a))
        thread = Thread(target=_beep,args=(a,b))
        thread.daemon = True
        thread.start()


@pyqtSlot()
def simple_beep():
    beep(400,5)

def main():
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    timer = Timer()

    timer.timeout.connect(simple_beep)
    timer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
