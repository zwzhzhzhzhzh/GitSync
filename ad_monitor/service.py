#! /usr/bin/env python
# coding=utf8

from data.search_druid import DruidHandler
from iForest.iforest_handler import IForestHandler

import datetime
import logging
import numpy as np
import pandas as pd

#expect_dimension = ['image_mode','rit','content_type','pt','age','gender','av','ctr2','cpm2']
expect_dimension = ['image_mode', 'rit', 'content_type', 'pt', 'ctr2', 'cpm2']
def main():
    # maintainers = ['ranshiwei']
    # from pyutil.program.script import script_init
    # script_init(maintainers)
    # 数据库时间和本地相比晚8个小时
    start_time = datetime.datetime.now() - datetime.timedelta(hours=55)
    end_time = start_time + datetime.timedelta(hours=1)
    tt_start = "2017-11-30 16"
    tt_end = "2017-12-01 16"
    dh = DruidHandler()
    # dh = DruidHandler(start_time=start_time.strftime("%Y-%m-%d %H"), end_time=end_time.strftime("%Y-%m-%d %H"))
    old_version = 600
    processd_matrix = pd.DataFrame()

    while old_version < 700:
        new_version = old_version + 50
        for pt in ('ios', 'android'):
            sample_matrix = dh.search(start_time=tt_start, end_time=tt_end, start_version=old_version, end_version=new_version, pt=pt)
            processd_matrix = pd.concat([processd_matrix, sample_matrix])
        old_version = new_version
     
    #调用算法
    if processd_matrix.shape[0] > 2:
        handler = IForestHandler()
        handler.ilf.fit(processd_matrix[expect_dimension])
        score, result = handler.predict(processd_matrix[expect_dimension])
        processd_matrix['IFor_score'] = score
        errorindex = result == -1
        processd_matrix[errorindex].to_csv('./ErrorOutliers.csv', header=True, index=False)
        processd_matrix[errorindex == False].to_csv('./NormalOutliers.csv', header=True, index=False)

        #打印到屏幕
        '''
        for index, v in enumerate(result):
            if v == -1:
                pass
                #print '\033[1;35m {target} \033[0m'.format(target=str(processd_matrix.iloc[index,]))
            else:
                pass
                #print processd_matrix.iloc[index,]
        '''
    else:
        print "可用数据不足"
    return
if __name__ == '__main__':
    main()
