#!/usr/bin/env python
# coding=utf-8

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest

def buildFilter(data):	
	rng = np.random.RandomState(79)
	Filter = IsolationForest(n_estimators=100,
                      n_jobs=-1,
                      verbose=0,
                      contamination=0.05,
                      random_state=rng,)
	Filter.fit(data)
	return Filter

def FilterPredict(Filter,data,batch):
	shape = data.shape[0]
	batch = 10**6
	all_pred = []
	for i in range(shape/batch+1):
    		start = i * batch
    		end = (i+1) * batch
    		test = data[start:end]
    		pred = Filter.predict(test)
		all_pred.extend(pred)
	return all_pred

def FilterCalcAuc(Filter,data,batch,dataFlag = None):	
	shape = data.shape[0]
	all_score = []
	for i in range(shape/batch+1):
    		start = i * batch
    		end = (i+1) * batch
    		test = data[start:end]
		test = sklearn.utils.check_array(test)
		score = Filter.decision_function(test)
		all_score.extend(score)
	y_scores = all_score
        value=None
        '''
	print "y_scores:"
	print y_scores
        '''
        if dataFlag is not None:
            y_true = dataFlag.values
            '''
            print "y_true:"
	    print y_true
            '''
            fpr,tpr,thresholds = sklearn.metrics.roc_curve(y_true,y_scores,pos_label = 0)
            value = sklearn.metrics.auc(fpr,tpr)
            '''
            print "fpr:"
	    print fpr
	    print "tpr:"
	    print tpr
	    print "thresholds:"
	    print thresholds
            '''
	return y_scores,value

if __name__ == '__main__':
    data = pd.read_csv('./testData/data.csv', index_col="id")
    data = data.fillna(0)
    X_cols = ["age","salary","sex","pt","ctr", "cpm"]
    Filter = buildFilter(data[X_cols])

    batch = 10**6
    data['pred'] = FilterPredict(Filter,data[X_cols],batch)
    #all_score,value = FilterCalcAuc(Filter,data[X_cols],batch)
    all_score,value = FilterCalcAuc(Filter,data[X_cols],batch,data['flag'])
    data['score'] = all_score
    data.to_csv('./testData/outliers.csv', columns=["score","pred",], header=False)
    print value
