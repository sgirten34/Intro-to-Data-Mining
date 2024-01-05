# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 21:48:58 2022

@author: sgirt
"""

#import fileinput
import sys
import math


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


# Define functions
def distinct(lst):
    distinct_lst = []
    for x in lst:
        if x not in distinct_lst:
            distinct_lst.append(x)
    
    return len(distinct_lst)


def confusion_matrix(true, pred):
    distinct_true = distinct(true)
    distinct_pred = distinct(pred)
    l = max(distinct_true, distinct_pred)
    
    #truth = len(distinct_values)
    #prediction = len(distinct_values)
    conf_matrix = [[0 for x in range(l)]for y in range(l)]
    
    for i in range(len(true)):
        conf_matrix[true[i]][pred[i]] += 1
    
    return conf_matrix


#n = distinct(truth)
conf_matrix = confusion_matrix(truth, prediction)


# Jaccard Similarity calculations
# Calculate true positive
tp_lst = []
for i in range(len(conf_matrix)):
    n = conf_matrix[i][i]
    if n <= 1:
        tp_lst.append(0)
    else:
        f = math.factorial
        nCr = f(n) / f(2) / f(n - 2)
        tp_lst.append(nCr)

tp = sum(tp_lst)


# Calculate false positive
fp_lst = []
for i in range(0, len(conf_matrix)):
    n = sum(conf_matrix[i])
    if n <= 1:
        fp_lst.append(0)
    else:
        f = math.factorial
        nCr = f(n) / f(2) / f(n - 2)
        fp_lst.append(nCr)

fp = sum(fp_lst) - tp


# Calculate false negative
pred_sum = [sum(i) for i in zip(*conf_matrix)]
fn_lst = []
for i in pred_sum:
    if n <= 1:
        fn_lst.append(0)
    else:
        f = math.factorial
        nCr = f(i) / f(2) / f(i - 2)
        fn_lst.append(nCr)

fn = sum(fn_lst) - tp

jaccard = (tp / (tp + fn + fp))
jaccard2 = '{:.3f}'.format(jaccard)


# Normalized Mutual Information calculation
n_obs = len(truth)
conf_matrix_norm = [[row / n_obs for row in col]for col in conf_matrix]

# column sums
col_sum = [sum(col)/ n_obs for col in conf_matrix]

# row sums
row_sum = [sum(row) / n_obs for row in zip(*conf_matrix)]

# Numerator
row_col_product = [[0 for x in range(len(row_sum))] for y in range(len(col_sum))]

for c in range(len(col_sum)):
    for r in range(len(row_sum)):
        row_col_product[r][c] = row_sum[r] * col_sum[c]


'''
for col in range(len(row_col_product)):
    for row in range(col):
        row_col_product[row][col] = col_sum[col] * row_sum[row]
'''



I_x_y = [[0 for x in range(len(row_sum))] for y in range(len(col_sum))]
for c in range(len(conf_matrix_norm)):
    for r in range(len(conf_matrix_norm[c])):
        if conf_matrix_norm[r][c] == 0:
            I_x_y[r][c] = 0
        elif row_col_product[r][c] == 0:
            I_x_y[r][c] = 0
        else:
            tmp = conf_matrix_norm[r][c] / row_col_product[r][c]
            I_x_y[r][c] = conf_matrix_norm[r][c] * math.log(tmp)

I_x_y = [sum(c) for c in I_x_y]
I_x_y = sum(I_x_y)
   

# Denominator
H_x = [-1 * i * math.log(i) for i in row_sum]
H_x = sum(H_x)

col_sum = [i for i in col_sum if i != 0]
H_y = [-1 * i * math.log(i) for i in col_sum]
H_y = sum(H_y)

# NMI
nmi = I_x_y / (math.sqrt(H_x * H_y))
nmi2 = '{:.3f}'.format(nmi)

output = nmi2 + " " + jaccard2
sys.stdout.write(output)

"""
# Create partition dictionary, true positive dictionary and num_elements dictionary
part_truth_keys = distinct(truth)
part_truth_val = []
partition_truth = {key: list(part_truth_val) for key in part_truth_keys}

# True positive dict, initialized to 0
true_positive = {key: 0 for key in part_truth_keys}

# Num of elements in a partition, initialized to 0
num_elements = {key: 1 for key in part_truth_keys}


# Insert partition values
for i in range(len(truth)):
    partition_truth[truth[i]].append(int(prediction[i]))
    

# Iterate over partition dictionary to count true positive and num of elements
for k in partition_truth:
    k_lst = partition_truth[k]
    
    for i in range(len(k_lst)- 1):
        if k_lst[i] == k_lst[i + 1]:
            true_positive[k] += 1
        num_elements[k] += 1

# True Positive value
tp_lst = []
for i in true_positive:
    n = true_positive.get(i)
    if n <= 1:
        tp_lst.append(0)
    else:
        f = math.factorial
        nCr = f(n) / f(2) /f(n - 2)
        tp_lst.append(nCr)

tp = sum(tp_lst)

# False Positive - Calculate nCr for num of elements then subtract from true positive
fp_lst = []
for i in num_elements:
    n = num_elements.get(i)
    if n <= 1:
        fp_lst.append(0)
    else:
        f = math.factorial
        nCr = f(n) / f(2) / f(n - 2)
        fp_lst.append(nCr)
        
fp = sum(fp_lst) - tp

# Partition for predictions to calculate false negative 
part_pred_keys = distinct(prediction)
part_pred_val = 0
partition_pred = {key: 0 for key in part_pred_keys}

# Insert count of prediction elements
for i in range(len(prediction)):
    partition_pred[prediction[i]] += 1
    
# False Negative - Calculate nCr for num of elements then subtract from true positive
fn_lst = []
for i in partition_pred:
    n = partition_pred.get(i)
    if n <= 1:
        fn_lst.append(0)
    else:
        f = math.factorial
        nCr = f(n) / f(2) / f(n - 2)
        fn_lst.append(nCr)
        
fn = sum(fn_lst) - tp

jaccard = (tp / (tp + fn + fp))
jaccard = '{:.3f}'.format(jaccard)

"""
    







        
        
