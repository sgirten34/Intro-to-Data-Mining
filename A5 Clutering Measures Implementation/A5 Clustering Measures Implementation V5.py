# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 22:05:55 2022

@author: sgirt
"""

import math as m
from collections import Counter

# Read data in
f = open('Sample Input 0.txt')
data = f.readlines()
#data = sys.stdin.readlines()


# Create lists for true and prediction
truth = []
prediction = []

for i in data:
    truth.append(i.split()[0])
    prediction.append(i.split()[1])

# Convert strings to ints
truth = [int(i) for i in truth]
prediction = [int(i) for i in prediction]



# Define functions for NMI
def mutual_info(cluster, actual):
    # Get counts of classes for the clustering and truth
    cluster_dict = Counter(cluster)
    actual_dict = Counter(actual)
    # Get total number of observations
    total = len(cluster)
    
    in_label = [(c,t) for c,t in zip(cluster, actual)]
    in_dict = Counter(in_label)
    
    I = 0
    for k, v in in_dict.items():
        c,t = k
        # Calculate probabilities
        prob_ij = v/total
        prob_clust = cluster_dict[c]/total
        prob_actual = actual_dict[t]/total
        # Sum probabilities
        I += prob_ij*m.log(prob_ij / (prob_clust*prob_actual))
    return I


def entropy(labs):
    # Get counts for each class of value
    ct_dict = Counter(labs)
    # Get total number of observations
    total = len(labs)
    H = 0
    for v in ct_dict.values():
        p = v/total
        H-= p *m.log(p) 
    return H

# Calculations for NMI
I_x_y = mutual_info(prediction, truth)
H_x = entropy(prediction)
H_y = entropy(truth)

nmi = I_x_y / m.sqrt(H_x*H_y)
nmi2 = '{:.3f}'.format(nmi)



# Calculate Jaccard coefficient

# Define nCr function to calculate combinations
def comb(n, r):
    f = m.factorial
    return f(n) / f(r) / f(n - r)

# Get counts of classes for the clustering and truth
pred_dict = Counter(prediction)
truth_dict = Counter(truth)
# Get total number of observations
total = len(prediction)

merge_lsts = [(p,t) for p,t in zip(prediction, truth)]
true_dict = Counter(merge_lsts)

# True Positive
tp = 0
for k,v in true_dict.items():
    tp += v**2
tp  = (tp - total) / 2

# False negative
fn = 0
for k,v in pred_dict.items():
    if v <= 1:
        continue
    else:
        fn += comb(v,2)
fn -= tp

# false positive
fp = 0
for k,v in truth_dict.items():
    if v <= 1:
        continue
    else:
        fp += comb(v,2)
fp -= tp

# Calculate coefficient
jaccard = tp / (tp + fn +fp)
jaccard2 = '{:.3f}'.format(jaccard)

output = nmi2 + " " + jaccard2
print(output)

