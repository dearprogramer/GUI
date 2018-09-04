# coding=utf-8
import pandas as pd
import numpy as np
class DataDeal:
    def __init__(self,filename):
        self.fileurl=filename
        self.size=0
        self.rows=0

    def readFile(self):
        rf=open(self.fileurl)
        self.df = pd.read_csv(rf, index_col=[0])
        self.size=self.df.shape[0]
        self.rows=self.df.shape[1]

    def setFile(self,filename):
        self.fileurl=filename
        self.size=0

    def getDatasize(self):
        return self.size

    def getLine(self,index):
        self.readFile()
        return self.df.index[index],self.df.values[index,:]

dd=DataDeal("data.csv")
time,rs=dd.getLine(0)
pn=rs.shape[0]
ds=np.linspace(0,1,pn)
print(ds)