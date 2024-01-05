# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 22:20:37 2022

@author: sgirt
"""
from collections import defaultdict

# At the end of video 1.1 for decision trees

def test_split(df):
    df_test = []
    for row in df:
        if row[0] == '-1':
            df_test.append(row)
        else:
            continue      
    return df_test 

def train_split(df):
    df_train = []
    for row in df:
        if row[0] != '-1':
            df_train.append(row)
        else:
            continue   
    return df_train

def get_split_pts(data):
    split_pts = []
    data = data.sort()
    for i in range(len(data) - 1):
        if data[i] == data[i + 1]:
            continue
        else:
            point = (data[i] + data[i + 1]) / 2
            split_pts.append(point)
    return split_pts



# Read data in
f = open('Data/input21.txt')
file = f.readlines()
#data = sys.stdin.readlines()

data = []
for i in file:
    data.append(i.split())
#    truth.append(i.split()[0])
#    prediction.append(i.split()[1])

test = test_split(data)
train = train_split(data)


train = [[row.split(':') for row in col]for col in train]
train_labels = []
for row in train:
    train_labels.append(row[0][0])


train_data = defaultdict(list)
for row in train:
    for col in range(1, len(row)):
        train_data[row[col][0]].append(row[col][1])



