#! /usr/bin/env python
# coding=utf8

import datetime
import _mysql
import numpy as np
import pandas as pd

from sample_processing import process_samples

ad_dimension = 'image_mode, rit, content_type'
flow_dimension = 'pt, age, gender'
av_dimension = 'av'
test_point_dimension = ['click', 'cost', 'ctr2', 'cpm2']
#point_dimension = ['count', 'cost', 'send', 'show_cnt', 'click', 'convert', 'bid', 'install_finish', 'download_start', 'click_start_detail', 'click_start', 'download_finish']

MYSQL_HOST = '10.3.34.27'
MYSQL_PORT = 3309

class DruidHandler(object):
    def __init__(self):
        self.ad_dimension = ad_dimension
        self.flow_dimension = flow_dimension
        self.av_dimension = av_dimension
        self.test_point_dimension = test_point_dimension
        return

    def get_all_dimension(self):
        return self.ad_dimension + ', ' + self.flow_dimension + ', ' + self.av_dimension

    def get_ad_dimension(self):
        return self.ad_dimension
    
    def get_flow_dimension(self):
        return self.flow_dimension

    def get_av_dimension(self):
        return self.av_dimension

    # 添加默认过滤条件
    def get_default_where_condition(self, start_version, end_version, pt):
        where_condition = []
        # rit限制
        where_condition.append("rit < '800000000'")
        # 版本处理
        start_version = str(start_version)
        end_version = str(end_version)
        if pt == "android":
            start_version = '.'.join(start_version)
            end_version = '.'.join(end_version)
        where_condition.append("(av >= '{start_version}') and (av < '{end_version}')".
                               format(start_version=start_version, end_version=end_version))
        return where_condition


    def format_search_sql(self, start_time, end_time, start_version, end_version, pt):
        aggregation_sql = self.get_aggregation_sql(self.test_point_dimension)
        sql = """select TIME_BUCKET(__time,P1D, 'Asia/Shanghai'), {current_dimension}, {aggregation_sql} from ad_fluctuation
               where {where_condition} and __time >= '{start_date}' and __time < '{end_date}'
               group by TIME_BUCKET(__time,P1D,'Asia/Shanghai'), {current_dimension}
               """.format(where_condition=' and '.join(self.get_default_where_condition(start_version, end_version, pt)),
                          current_dimension=self.ad_dimension + ', ' + self.flow_dimension + ', ' + self.av_dimension,
                          aggregation_sql=aggregation_sql, start_date=start_time, end_date=end_time)
        print sql
        return sql

    def search(self, start_time, end_time, start_version, end_version, pt):
        db = _mysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, db="information_schema")
        db.query(self.format_search_sql(start_time, end_time, start_version, end_version, pt))
        searchresult = db.use_result().fetch_row(0)
        db.close()
        columns = self.get_dataFrame_columns()
        if len(searchresult) > 0:
            data = pd.DataFrame(list(searchresult), columns=columns)
            return process_samples(data)
        else:
            print '\033[1;35m Data Not Enough  \033[0m'
            return pd.DataFrame()
    
    def get_dataFrame_columns(self):
        columns = ['Time_Str', ]
        columns.extend((self.ad_dimension + ', ' + self.flow_dimension + ', ' + self.av_dimension).replace(' ','').split(','))
        columns.extend(test_point_dimension)
        return columns

    def get_aggregation_sql(self, aggregation):
        """
        根据维度生成sql
        :param aggregation:
        :return:
        """
        aggregation_sql = []
        for aggr in aggregation:
            if aggr in ('cost', 'send', 'show_cnt', 'click'):
                aggregation_sql.append(' sum({target}) as {target} '.format(target=aggr))
            elif aggr in ('show/send'):
                aggregation_sql.append(' sum(show_cnt)/sum(send) as show_send ')
            elif aggr in ('ctr2'):
                aggregation_sql.append(' sum(click)/sum(show_cnt) as ctr2 ')
            elif aggr in ('cpm2'):
                aggregation_sql.append(' sum(cost)/(sum(show_cnt)*100) as cpm2 ')
            elif aggr in ('acp'):
                #aggregation_sql.append(' (case when sum(click)=0 then 0 else  sum(cost)/(sum(click)*100000) end) as acp ')
                aggregation_sql.append(' sum(cost)/(sum(click)*100000) as acp ')

        aggregation_str = ','.join(aggregation_sql)
        return aggregation_str
