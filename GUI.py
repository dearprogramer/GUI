# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import  matplotlib.pyplot as plt
import pandas as pd
import sys
import cv2
import os
import threading
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold=False

    def getmin(self,a, b):
        if a > b:
            return b
        else:
            return a

    def getmax(self,a, b):
        if a < b:
            return b
        else:
            return a

    def drawPic(self,data, title):
        t=data[:,0]
        data1=data[:,1]
        data2=data[:,2]
        color = 'tab:red'
        self.axes.set_xlim([0,600])
        self.axes.set_xlabel('epoch (200)')
        self.axes.set_ylabel('loss', color=color)
        self.axes.plot(t, data1, color=color)
        self.axes.tick_params(axis='y', labelcolor=color)
        ax2 = self.axes.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('acurrate rate', color=color)  # we already handled the x-label with ax1
        ax2.plot(t, data2, color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        self.axes.set_title("loss and acurate graph")

    def drawLine(self,data,title):
        pn=data.shape[0]
        self.axes.cla()
        xx=np.linspace(0,1,pn)
        color = 'tab:red'
        self.axes.set_xlabel("posiztion (m)")
        self.axes.set_ylabel("value (m/s)")
        self.axes.set_title(title)
        self.axes.plot(xx,data,color=color)
        self.draw()



class DataDeal:
    def __init__(self):
        self.fileurl=""
        self.size=0
        self.rows=0

    def readFile(self):
        rf=open(self.fileurl)
        self.df = pd.read_csv(rf, index_col=[0])
        self.size=self.df.shape[0]
        self.cols=self.df.shape[1]

    def setFile(self,filename):
        self.fileurl=filename
        self.size=0

    def getDatasize(self):
        return self.size

    def getCols(self):
        return self.cols

    def getRows(self):
        return self.size

    def getLine(self,index):
        return self.df.index[index] ,self.df.values[index,:]

class MainWin(QMainWindow):
    def __init__(self,parent=None):
        super(MainWin, self).__init__(parent)
        self.picwidth=600
        self.picheight=400
        self.isload=0
        self.background = "back.png"
        self.dt=1000
        self.index=0
        self.state=0
        self.isload=0
        self.rows=0
        self.timer=QTimer()
        self.timer.timeout.connect(self.play)
        self.dataPro=DataDeal()
        self.initialMainFrame()

    def initialMainFrame(self):
        self.setWindowTitle("数据显示")
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        self.reserveinfoitems = 0
        self.menu = QMenuBar()
        self.fileMenu=self.menu.addMenu("文件")
        self.addfile=self.fileMenu.addAction("添加数据")
        self.addfile.triggered.connect(self.loadFile)
        self.excuteAction=QPushButton("播放")
        self.excuteAction.clicked.connect(self.excute)
        self.excuteParame=QLabel()
        self.excuteParame.setText("数据未加载，不能播放")
        self.mid_Hlayout=QHBoxLayout()
        self.mid_Hlayout.addWidget(self.excuteParame)
        self.mid_Hlayout.addWidget(self.excuteAction)
        self.canval=QGraphicsView()
        self.scen=QGraphicsScene()
        self.grapscen=QGraphicsScene()
        self.canval.setScene(self.scen)
        self.conentFrame = QFrame()
        self.total_Vlayout = QVBoxLayout()
        self.picLable = QLabel()
        self.displayImage(self.background)
        self.canvalinit(self.background)
        self.setMenuBar(self.menu)
        self.total_Vlayout.addWidget(self.canval)
        self.total_Vlayout.addLayout(self.mid_Hlayout)
        self.conentFrame.setLayout(self.total_Vlayout)
        self.setCentralWidget(self.conentFrame)
        self.fig = MyMplCanvas()

    def canvalinit(self,filename):
        picdata = self.cv_imread(filename)
        picdata = cv2.cvtColor(picdata, cv2.COLOR_BGR2RGB)
        self.backpic = cv2.resize(picdata, (self.picwidth, self.picheight))
        self.pic = QImage(self.backpic.data,self.picwidth, self.picheight, QImage.Format_RGB888)
        self.scen.addPixmap(QPixmap.fromImage(self.pic))

    def cv_imread(self,file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return cv_img

    def displayImage(self,filename):
        picdata = self.cv_imread(filename)
        picdata = cv2.cvtColor(picdata, cv2.COLOR_BGR2RGB)
        picdata= cv2.resize(picdata, (self.picwidth, self.picheight))
        tempic = QImage(picdata,self.picwidth, self.picheight, QImage.Format_RGB888)
        self.scen.clear()
        self.scen.addPixmap(QPixmap.fromImage(tempic))

        self.canval.setScene(self.scen)
        self.canval.show()

    def initFig(self):
        self.grapscen.clear()
        self.grapscen.addWidget(self.fig)
        self.canval.setScene(self.grapscen)
        self.canval.show()

    def updateGraph(self,data,title):
        self.fig.drawLine(data,title)
        #self.grapscen.update()
        #self.canval.update()
        #self.canval.show()

    def drawGragh(self,data,title):
        self.grapscen.clear()
        tfigure = MyMplCanvas()
        #tfigure.drawPic(data,title)
        tfigure.drawLine(data,title)
        self.grapscen.addWidget(tfigure)
        self.canval.setScene(self.grapscen)
        self.canval.show()


    def play(self):
        title=""
        if self.index<self.rows:
            t, data = self.dataPro.getLine(self.index)
            title=title+"time= "+str(t)+" the gragh of the u"
            #self.drawGragh(data,title)
            self.updateGraph(data,title)
            self.index=self.index+1
        else :
            self.state=3
            self.excuteAction.setText("重播")
            self.timer.stop()



    def excute(self):
        if(self.isload):
            if self.state==0:
                self.index=0
                self.excuteAction.setText("暂停")
                self.state=1
                self.timer.start(self.dt)
            else:
                if self.state==1:
                    self.timer.stop()
                    self.excuteAction.setText("播放")
                    self.state=2
                else:
                    if self.state==2:
                        self.timer.start(self.dt)
                        self.excuteAction.setText("暂停")
                        self.state = 1
                    else:
                        if self.state==3:
                            self.index=0
                            self.timer.start(self.dt)
                            self.excuteAction.setText("暂停")
                            self.state=1



    def loadFile(self):
        self.datafiles = QFileDialog.getOpenFileName(self, '模拟数据', './', "data files(*.csv)")[0]
        if self.datafiles != "":
            if not self.isload:
                self.dataPro.setFile(self.datafiles)
                self.dataPro.readFile()
                self.rows=self.dataPro.getRows()
                self.isload=1
                self.excuteParame.setText("数据已加载 文件地址："+self.datafiles)
                self.initFig()
            else:
                self.timer.stop()
                self.state=0
                self.excuteAction.setText("播放")
                self.excuteParame.setText("数据已加载 文件地址：" + self.datafiles)
                self.index=0
                self.dataPro.setFile(self.datafiles)
                self.dataPro.readFile()
                self.rows=self.dataPro.getRows()

        else:
            self.excuteParame.setText("数据加载错误" )




if __name__ == "__main__":
    app = QApplication(sys.argv)    #创建QApplication类的实例
    dia =MainWin()              #创建DumbDialog类的实例
    dia.show()                      #显示程序主窗口
    app.exec_()