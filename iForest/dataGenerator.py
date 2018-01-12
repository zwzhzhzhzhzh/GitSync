#!/usr/bin/env python
# coding=utf-8

import numpy as np
import pandas as pd

def dataGenerator(DataFormat,Cols):
    data=pd.DataFrame(columns = ([Cols[0],]+Cols[2:]))
    data[Cols[0]] = np.ones(DataFormat[1])*DataFormat[0]
    for i in range(len(Cols)-2):
        data[Cols[i+2]] = np.random.normal(DataFormat[i+2][0],DataFormat[i+2][1],DataFormat[1])
    return data

if __name__ == '__main__': 
    Cols = ["type","number","value1","value2"]
    #type,number,model(aver,s_dev),...
    DataFormat1 = (1,1000, (10.0,2.0),(10.0,2.0))
    DataFormat2 = (2,700, (20.0,3.0),(20.0,3.0))
    DataFormat3 = (3,100,(0.0,2.0),(0.0,2.0))
    data1 = dataGenerator(DataFormat1,Cols)
    data2 = dataGenerator(DataFormat2,Cols)
    data3 = dataGenerator(DataFormat3,Cols)
    data = pd.concat([data1,data2,data3])
    data["index"] = range(data.shape[0]) 
#   可以选择某一类数据进行测试
#    data = data[(data["type"] == 2)]
#   重置index的方式
#    data = data.reset_index(drop=True)
    data.set_index("index")
    data.to_csv('./testData/outdata.csv',header=True,index=False)
#    print data
