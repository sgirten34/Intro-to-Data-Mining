# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 21:47:08 2022

@author: sgirt
"""

import sys
import csv
#from collections import Counter

# Begin functions
def test_split(df):
    df_test = []
    for row in df:
        if row[-1] == '-1':
            df_test.append(row)
        else:
            continue      
    return df_test 

def train_split(df):
    df_train = []
    for row in df:
        if row[-1] != '-1':
            df_train.append(row)
        else:
            continue   
    return df_train

def calc_P_y(lab):
    return len(lab)/train_num_obs
 
def calc_P_xy(lab):
    P_xy = []
    for i in range(train_num_attr):
        if i != 12:
            ct_0 = 0
            ct_1 = 0
            for r in lab:
                if r[i] == '0':
                    ct_0 += 1
                else:
                    ct_1 += 1
            prob = ((ct_0 + 0.1) / (len(lab) + 0.2), 
                    (ct_1 + 0.1) / (len(lab) + 0.2))
            P_xy.append(prob)
        else:
            leg_0 = leg_2 = leg_4 = leg_5 = leg_6 = leg_8 = 0
            for r in lab:
                if r[i] == '0': leg_0 += 1
                elif r[i] == '2': leg_2 += 1
                elif r[i] == '4': leg_4 += 1
                elif r[i] == '5': leg_5 += 1
                elif r[i] == '6': leg_6 += 1
                elif r[i] == '8': leg_8 += 1
            prob = ((leg_0 + 0.1) / (len(lab) + 0.6),
                    (leg_2 + 0.1) / (len(lab) + 0.6),
                    (leg_4 + 0.1) / (len(lab) + 0.6),
                    (leg_5 + 0.1) / (len(lab) + 0.6),
                    (leg_6 + 0.1) / (len(lab) + 0.6),
                    (leg_8 + 0.1) / (len(lab) + 0.6))
            P_xy.append(prob)
    return P_xy
                
def separate_classes(df):
    sep_class = {}
    for i in range(len(df)):
        values = df[i]
        label = values[-1]
        if (label not in sep_class):
            sep_class[label] = list()
        sep_class[label].append(values)
    return sep_class

def class_summary(sep_class):
    summary = {}
    for cls_val, r in sep_class.items():
        P_xy = calc_P_xy(r)
        P_y = calc_P_y(r)
        summary[cls_val] = [P_xy, P_y]
    return summary

def class_probabilities(nbc_model, test_data):
    probs = {}
    for value, summary in nbc_model.items():
        probs[value] = summary[1]
        for i in range(train_num_attr):
            probs[value] *= summary[0][i][int(test_data[i])]
    return probs

def nbc_predict(nbc_model, test_data):
    probs = class_probabilities(nbc_model, test_data)
    return max(probs, key = probs.get)

# Read data in 
#file = open('Data/input4.txt')
file = sys.stdin.read().splitlines()
csvreader = csv.reader(file)
col_names = next(csvreader)
data = []
for row in csvreader:
    data.append(row)

file.close()

# Delete animal name from data and from column names
for col in data:
    del col[0]
    
del col_names[0]

# Split into test and training sets
test = test_split(data)
train = train_split(data)

# Total number of observations for training data and number of values
train_num_obs = len(train)
train_num_attr = len(train[0]) - 1

sep_class = separate_classes(train)
"""
for k, v in sep_class.items():
    print(k)
    print(v)
"""

nbc_model = class_summary(sep_class)
"""
for k, v in nbc_model.items():
    print(k),
    print(v)
"""

# Stopped on video 2.one Naive Bayes Classifier at time of 7:52

#class_probabilities(nbc_model, test[0])
#nbc_predict(nbc_model, test[0])

predictions = []
for row in test:
    prediction = nbc_predict(nbc_model, row)
    predictions.append(prediction)

#predictions

for prediction in predictions:
    print(prediction)

