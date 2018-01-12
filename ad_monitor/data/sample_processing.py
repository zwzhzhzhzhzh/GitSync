#! /usr/bin/env python
# coding=utf8

import numpy as np
import pandas as pd

pt_dict={'android':'1','iphone':'2','ipad':'4','ios':'6','wap':'8','web':'16'}
defaultValue_dict={'show_send':'100000000','ctr2':'100000000','cpm2':'100000000'}

def convertPt2Float(pt):
    if pt_dict.has_key(pt):
        return pt_dict[pt]
    else:
        return '0'

def convertNone2DefalutValue(x, header):
    if x == None:
        if defaultValue_dict.has_key(header):
            return defaultValue_dict[header]
        else:
            return '0'
    else:
        return x

def convertAv2Float(av):
    return av.replace('.','0')

def process_samples(data):
    columns = data.columns

    for header in columns:
        #丢弃存在None值的行
        #data = data[data[header].isnull() == False]
        
        #将None值替换成相应的值
        data[header] = data[header].apply(convertNone2DefalutValue, args={header,})
    
    if 'pt' in columns:
        data['pt'] = data['pt'].apply(convertPt2Float)

    if 'av' in columns:
        data['av'] = data['av'].apply(convertAv2Float)

    if 'click' in columns:
        data = data[data['click'].astype('Float64') >= 20000]

    if 'cost' in columns:
        data = data[data['cost'].astype('Float64') >= 100000000]

    if 'show_cnt' in columns:
        data = data[data['show_cnt'].astype('Float64') >= 100000]

    # 验证中间结果
    # totalCount = len(data.index)
    # index = 0
    # data_dict = {}
    # while index < totalCount:
    #     sample = data[index:index+1]
    #     key_array = []
    #     inner_columes = ['image_mode', 'rit', 'content_type', 'pt', 'age', 'gender']
    #     for attr in inner_columes:
    #         key_array.append(sample[attr].values[0])
    #     k = '|'.join(key_array)
    #     v = sample['av'].values[0] + '|ctr2:' + sample['ctr2'].values[0] + '|cpm2:' + sample['cpm2'].values[0]
    #     if data_dict.get(k, []):
    #         old_v = data_dict[k]
    #         old_v.append(v)
    #     else:
    #         dv = []
    #         dv.append(v)
    #         data_dict[k] = dv
    #     index += 1
    #
    # for k, v in data_dict.items():
    #     print k, v

    return data
