# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 09:32:16 2022

@author: sgirt
"""

#from __future__ import print_function
#from __future__ import division
#import pandas as pd
#import numpy as np
import math as m
from collections import Counter
from scipy.special import comb

# Read data in
f = open('Sample Input 0.txt')
data = f.readlines()

# Create lists for true and prediction
truth = []
prediction = []

for i in data:
    truth.append(i.split()[0])
    prediction.append(i.split()[1])

# Convert strings to ints
truth = [int(i) for i in truth]
prediction = [int(i) for i in prediction]


# Define functions##############################
def Entropy(label):
    count_dict = Counter(label)
    #total = label.count()
    total = len(label)
    H = 0
    for value in count_dict.values():
        p = value/total
        H-= p *m.log(p) 
    return H


def Mutual_information(cluster_label,truth_label):
    cluster_dict = Counter(cluster_label)
    truth_dict = Counter(truth_label)
    #total = cluster_label.count()
    total = len(cluster_label)
    in_label = [(c,t) for c,t in zip(cluster_label,truth_label)]
    in_dict = Counter(in_label)
    I = 0
    for k,v in in_dict.items():
        c,t = k
        pij = v/total
        pc = cluster_dict[c]/total
        pt = truth_dict[t]/total
        I += pij*m.log(pij/(pc*pt))
    return I


def NMI(cluster_label,truth_label):
    I = Mutual_information(cluster_label,truth_label)
    H_c = Entropy(cluster_label)
    H_t = Entropy(truth_label)
    return I/m.sqrt(H_c*H_t)


def Jaccard_coef(cluster_label,truth_label):
    cluster_dict = Counter(cluster_label)
    truth_dict = Counter(truth_label)
    #total = cluster_label.count()
    total = len(cluster_label)
    in_label = [(c,t) for c,t in zip(cluster_label,truth_label)]
    in_dict = Counter(in_label)
    TP = 0
    for k,v in in_dict.items():
        TP += v**2
    TP  = 0.5*(TP - total)
    FN = 0
    for k,v in cluster_dict.items():
        FN += comb(v,2)
    FN -= TP
    FP = 0
    for k,v in truth_dict.items():
        FP += comb(v,2)
    FP -= TP
    Jaccard = TP/(TP+FN+FP)
    return Jaccard


'''
truth = pd.read_csv('partitions.txt',sep=' ',names=['id','label'],index_col=['id'])
clusters = []
for i in range(1,6):
    filename = str(i).join(['clustering_','.txt'])
    clusters.append(pd.read_csv(filename ,sep=' ',names=['id','label'],index_col=['id']))
'''
f = open('Sample Input 0.txt')
data = f.readlines()

# Create lists for true and prediction
truth = []
prediction = []

for i in data:
    truth.append(i.split()[0])
    prediction.append(i.split()[1])

# Convert strings to ints
truth = [int(i) for i in truth]
prediction = [int(i) for i in prediction]

nmi_score = NMI(prediction, truth)
jaccard_score = Jaccard_coef(prediction, truth)

check = Counter(truth)
check2 = Counter(prediction)

#NMI_score = [NMI(cluster['label'],truth['label']) for cluster in clusters]
#Jaccard_score = [Jaccard_coef(cluster['label'],truth['label']) for cluster in clusters]


#scores = pd.DataFrame({'NMI':NMI_score,'Jaccard':Jaccard_score},columns=['NMI','Jaccard'])
#scores.to_csv('scores.txt',sep=' ',header=False,index=False)