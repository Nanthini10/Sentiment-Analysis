#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:51:09 2017

@author: nanthini
"""

#%% Imports
import pandas as pd
import numpy as np
import random
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB


#%% Loading Data
data = pd.read_csv("data/newsCorpora.csv",usecols=[1,4],
                   names=["title","category"],header=None,delimiter="\t")

data = np.array(data)
X = data[:,0]
y = data[:,1]

Xtrain = X[:int(0.8*X.shape[0])]
ytrain = y[:int(0.8*X.shape[0])]
#%%

with open("data/title_cat.txt","w") as f:
    writer = csv.writer(f,delimiter="\t")
    writer.writerows(data)
    

#%%

cv = CountVectorizer(lowercase=True,stop_words='english')
tf = TfidfTransformer(sublinear_tf=True)
    
#%%Training classifiers

'''
clf = Pipeline([('vect',cv ),('tfidf',tf),
                ('clf',MLPClassifier(hidden_layer_sizes=(15,), 
                                      random_state=1, max_iter=1, 
                                      warm_start=True))
              ])
'''                
clf1 = Pipeline([('vect', cv),('tfidf',tf),('clf',LogisticRegression())
                ])
clf2 = Pipeline([('vect', cv),('tfidf',tf),('clf',MultinomialNB())
                ])    
#clf = clf.fit(Xtrain,ytrain)
clf1 = clf1.fit(Xtrain,ytrain)
clf2 = clf2.fit(Xtrain,ytrain)

#%% IDEA: We can directly scrape headlines and put them into categories

dataTest = np.array(random.sample(data,100000))
Xtest = X[int(0.8*X.shape[0]):]
ytest = y[int(0.8*X.shape[0]):]

#ypred = clf.predict(Xtest)
#print "MLP: ",accuracy_score(ypred,ytest)

ypred = clf1.predict(Xtest)
print "LOG: ",accuracy_score(ypred,ytest)

ypred = clf2.predict(Xtest)
print "MNB",accuracy_score(ypred,ytest)