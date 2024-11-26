from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QColor
from ButLeft import ButLeft
from FrameBase import CroDBase,col
import numpy as np , scipy.io as sio
import math
from PyQt5 import QtCore, QtGui, QtWidgets

class M_Lable(CroDBase):
    qtimer = QtCore.QTimer()
    cont = 1
    pointset = None
    buffer_image = None
    bufp = None
    sleep = 33
    def __init__(self):
        super().__init__()
        self.xmax=8
        self.ymax=8
        self.qtimer.timeout.connect(self.to)
        self.qtimer.start(self.sleep)

    def paintEvent(self,a0):
        self.paintBeg()

        if self.buffer_image == None:
            self.buffer_image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
            self.buffer_image.fill(QtCore.Qt.black)
            self.bufp = QtGui.QPainter(self.buffer_image)

        if self.pointset !=None:
            try:
                # print(self.bufp.begin(self))
                cord =self.Line(*self.pointset[0],*self.pointset[1], juestcord=True)
                self.bufp.setPen(QColor(*self.pointset[2],128))
                cord = tuple(map(int,cord))
                self.bufp.drawPoint(*cord[:2])
                self.bufp.drawPoint(*cord[2:])
                self.bufp.drawLine(*cord )
                # self.bufp.end()
            except:
                pass

        self.qp.drawImage(0,0,self.buffer_image)
        color = int(self.cont)%0xFFF
        G = (((color>>4)&0xF) <<4)+ 0xF
        R  = (((color >> 11) & 0xF) << 4 )| 0x70
        B  = ((color & 0xF) << 4 )+ 0xF

        # print(color,R,G,B)

        nc = QColor( R,G,B,255)
        angs = np.array([  (i*2-1) for i in range(1,7)])
        angs *=np.array([(-1)**int(i) for i in range(len(angs)) ])

        sus= np.array([1/i for i in angs])

        sus = sus * (8/np.abs(sus).sum())
        c2xy = lambda arg: np.array([arg[0] * math.cos(arg[1]), arg[0] * math.sin(arg[1])])
        points =  list(map(c2xy,list(zip(sus, angs * self.cont * np.pi * 2 / 133))))
        old= np.zeros(2)
        self.Point(0,0)

        for p in points:
            newc = old+p
            self.Line(*old, *newc, unlim=False, col=nc   ,arror=True)
            self.Point(*newc)
            old=newc
        self.pointset =  (tuple(old),tuple(old-p),(R,G,B))

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
