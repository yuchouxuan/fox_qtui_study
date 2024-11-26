from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QColor
from ButLeft import ButLeft
from FrameBase import CroDBase,col
import numpy as np , scipy.io as sio

class Load(CroDBase):
    qtimer = QtCore.QTimer()
    cont = 1
    pointset=None
    buffer_image = None
    bufp=None
    fs  = None
    da = None
    dps =1000
    sleep = 33
    pdl =0.030

    def __init__(self):
        super().__init__()
        self.xmax=8
        self.ymax=8
        self.qtimer.timeout.connect(self.to)
        self.qtimer.start(self.sleep)
        self.fs,self.da = sio.wavfile.read('z:/ctf/os.wav', 'r')
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
    but={}
    uiclass = {}


    def btPress(self,name=''):

        for i in self.but:
            self.but[i].select = False
        self.but[name].select = True
        # print( self.uiclass[name])
        self.horizontalLayout.removeWidget(self.label)
        try:
            pass
            # del self.label
        except :
            pass
        self.label = self.uiclass[name].Ui_Form(self.centralwidget)
        self.label.setupUi(self.label)
        self.horizontalLayout.addWidget(self.label)
        self.update()



    def add_but(self,name="Butt"):
        tbut = ButLeft(self.centralwidget)
        tbut.initBut(name)
        tbut.setMaximumWidth(150)
        tbut.setMinimumWidth(150)
        tbut.sig.connect(self.btPress)
        self.but[name] = tbut
        self.verticalLayout.addWidget(tbut)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 775)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)

        # 加载插件
        for i in self.ucs :
            try:
                tmp_frame = i.Ui_Form()
                tmp_frame.setupUi(tmp_frame)
                self.add_but(tmp_frame.name)
                self.uiclass[tmp_frame.name] = i
            except:pass


        self.label = Load()
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 20)
        self.horizontalLayout.setStretch(1, 65535)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # self.btPress(self.but.keys()[0])


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "123"))
