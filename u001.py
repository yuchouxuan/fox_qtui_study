from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QColor
from ButLeft import ButLeft
from FrameBase import CroDBase,col
import numpy as np , scipy.io as sio

from PyQt5 import QtCore, QtGui, QtWidgets

class M_Lable(CroDBase):
    qtimer = QtCore.QTimer()
    cont = 1
    pointset = None
    buffer_image = None
    bufp = None
    fs = None
    da = None
    dps = 1000
    sleep = 33
    pdl = 0.030
    def __init__(self):
        super().__init__()
        self.xmax=8
        self.ymax=8
        self.qtimer.timeout.connect(self.to)
        self.qtimer.start(self.sleep)
        self.fs,self.da = sio.wavfile.read('./os.wav', 'r')
        self.dps = self.fs*self.sleep//1000
        self.pdl = int(self.fs *self.pdl)
        self.da = np.array(self.da)
        self.da = self.da/self.da.max()*7
        self.da *=-1

    def paintEvent(self,a0):
        if self.buffer_image == None :
            self.buffer_image= QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
            self.bufp = QtGui.QPainter(self.buffer_image)
        self.buffer_image.fill(QtCore.Qt.black)

        if len(self.da) /self.dps < self.cont:
            self.cont = 1
        pstart = self.cont*self.dps - self.pdl
        pstart = 0 if pstart < 0 else pstart
        pprint = self.da[pstart:self.cont*self.dps][::-1]
        for i  in  range(1,len(pprint)):

            alpha = int(255 - i/self.pdl*255)
            if alpha <= 0:
                break

            self.bufp.setPen(QColor(alpha, 200, 255 - alpha, int(alpha * .75)))
            cord = self.Line(*pprint[i], *pprint[i - 1], juestcord=True)
            self.bufp.drawLine(*cord)

            cord = self.Point(*pprint[i],justCord=True)
            self.bufp.setPen(QtGui.QPen(QColor(alpha,200,  255-alpha),2 ))
            self.bufp.drawPoint(*cord)

        self.paintBeg()
        self.qp.drawImage(0, 0, self.buffer_image)
        self.cont+=1
        self.paintEnd()

    def to(self):
        self.update()

    def __del__(self):
        self.qtimer.stop()
        # super.__del__()


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1021, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.label =M_Lable()
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
