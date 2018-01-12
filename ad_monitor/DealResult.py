#!/usr/bin/env python
# coding=utf-8
import sys
import numpy as np
import pandas as pd

mean_list=['ctr2','cpm2']
pt_dict={'android':'1','iphone':'2','ipad':'4','ios':'6','wap':'8','web':'16'}

def func_readData(dataName):
    data = pd.read_csv(dataName)
    return data

'''
功能：统计百分比
输入：局部样本，聚合维度，整体样本
'''
def func_groupPercent(data_part, headers, data_total): 
    print "head Percent " +  str(headers) + " func:"
    result=[]
    headers_series = data_part.groupby(headers).size().astype('Float64')
    
    for index in headers_series.index:
        '''
        index=聚合维度对应值，如维度为av的话，则index可能为60401
        value1=该维度下局部样本的数量占整体样本的数量的比值
        count=该维度下index在整体样本中的数量
        value2=count在整体样本中的比值
        '''
        data = data_total
        for i,header in enumerate(headers):
            data = data[data[header] == index[i]]
        count = data.shape[0]
        #data_total[data_total[header] == index].shape[0]
        value1 = headers_series[index]/count*100
        value2 = count/float(data_total.shape[0])*100
        result.append((index,value1,count,value2))

    if len(result) > 0:
        print pd.DataFrame(result,columns=[str(headers),'SamPercent','TotalCount','TotalPercent']).sort(['SamPercent'],ascending = False).head(20)
    else:
        print "数据不足"

def func_groupSize(data, headers): 
    headers_series = data.groupby(headers).size()
    headers_series.sort(ascending = False)
    print "head Size func:"
    for index in headers_series.index:
        print index
    print headers_series.head(5)

def func_ptData(data,pt):
    if pt_dict.has_key(pt):
        return data[data['pt'].astype('str') == pt_dict[pt]]
    else:
        return data[data['pt'] == 0]

def func_headerMean(data, header):
    print str(header) +" mean:", data[header].astype('Float64').mean()

def func_dataProcess(data_part,data_total): 
    func_groupPercent(data_part, ['av','pt'],data_total)
    for header in mean_list:
        func_headerMean(data_part, header)

def func_processDiffPt(data_part, data_total):
    print "=========total========="
    func_dataProcess(data_part, data_total)
    print "=========android========="
    func_dataProcess(func_ptData(data_part,'android'), func_ptData(data_total,'android'))
    print "=========ios========="
    func_dataProcess(func_ptData(data_part,'ios'),func_ptData(data_total,'ios'))

if __name__ == '__main__': 
    data_error = func_readData('ErrorOutliers.csv')
    data_normal = func_readData('NormalOutliers.csv')
    data_total = pd.concat([data_error,data_normal])
    
    print   "Error Number ",data_error.shape[0]
    print   "Normal Number ",data_normal.shape[0]
    print   "Total Number ",data_total.shape[0]
 
    print '\033[1;35mErrorOutliers.csv\033[0m'
    func_dataProcess(data_error,data_total)

    '''
    func_GroupSize(data_error)

    '''
    print

    print '\033[1;35mNormalOutliers.csv\033[0m'
    func_dataProcess(data_normal,data_total)
