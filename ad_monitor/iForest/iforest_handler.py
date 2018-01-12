#! /usr/bin/env python
# coding=utf8

import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.utils import check_array


class IForestHandler(object):

    def __init__(self):
        self.rng = np.random.RandomState(79)
        self.ilf = IsolationForest(n_estimators=100,
                                   n_jobs=-1,
                                   verbose=0,
                                   contamination=0.03,
                                   random_state=self.rng
                                   )

    def predict(self, X):
        X = check_array(X, accept_sparse='csr')
        is_inlier = np.ones(X.shape[0], dtype=int)
        score = self.ilf.decision_function(X)
        # print "thres:", ilf.threshold_
        # print v
        d = score <= self.ilf.threshold_
        # print d
        is_inlier[d] = -1
        return score,is_inlier
