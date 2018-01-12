#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from dataGenerator import *
from iForestFunc import *

def GerData():
    Cols = ["type","number","value1","value2"]
    #type,number,model(aver,s_dev),...
    DataFormat1 = (1,10, (10.0,2.0),(10.0,2.0))
    DataFormat2 = (2,7, (20.0,3.0),(20.0,3.0))
    DataFormat3 = (3,5,(0.0,2.0),(0.0,2.0))
    data = pd.DataFrame()
    data1 = dataGenerator(DataFormat1,Cols)
    data2 = dataGenerator(DataFormat2,Cols)
    data3 = dataGenerator(DataFormat3,Cols)
    data = pd.concat([data,data1])
    data = pd.concat([data,data2])
    data = pd.concat([data,data3])
    data["index"] = range(data.shape[0]) 
    data.set_index("index")
    data.to_csv('./testData/outdata.csv',header=True,index=False)

def DealData():

    data = pd.read_csv('./testData/outdata.csv', index_col="index")
    data = data.fillna(0)
#   可以通过筛选选择某一类数据进行检测
#    data = data[(data["type"] == 2)]
    X_cols = ["type","value1","value2"]
    Filter = buildFilter(data[X_cols])

    batch = 10**6
    data['pred'] = FilterPredict(Filter,data[X_cols],batch)
    all_score,value = FilterCalcAuc(Filter,data[X_cols],batch)
    #all_score,value = FilterCalcAuc(Filter,data[X_cols],batch,data['flag'])
    data['score'] = all_score
    errorindex = data['pred'] == -1
    #print (errorindex == False)
    data.to_csv('./testData/outliers.csv', header=True, index=False)
    print data[(data['pred'] == -1) & (data['type'] == 2.0)]
    #print value

if __name__ == '__main__':
    print "Generating Data"
    GerData()
    print "Dealing Data"
    DealData()
    print "Done"
