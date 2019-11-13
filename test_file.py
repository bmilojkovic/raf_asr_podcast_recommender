# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:57:40 2019

@author: sicTa
"""

import AudioAnalyzer
import numpy
from RestrictedBoltzmannMachine import RBM
from DeepBeliefNetwork import DBN



#rbm = RBM(39, 2048, num_gibbs_samplings = 1)
dbn = DBN(2, 39, [1000, 1000], 44, 1, 1e-3)
#
#print(rbm.weights)

analyzer = AudioAnalyzer.AudioAnalyzer()
features = analyzer.normalized_feature_vector('OSR_us_000_0061_8k.wav')



dbn.train(features, 10)

#rbm.contrastive_divergence(features, 1)

#print(rbm.weights)

'''
x = numpy.asarray(features[0]).reshape((len(features[0]), 1))
_, hid = rbm.sample_hidden(x)
vis, vis2 = rbm.sample_visible(hid)

x = (np.random.binomial(size=x.shape,   # discrete: binomial
                                       n=1,
                                       p=x))


'''




print(sum(abs(vis2 - x)))