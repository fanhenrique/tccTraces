# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:15:50 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import pickle as pkl

def load_sz_data(dataset):
    sz_adj = pd.read_csv(r'T-GCN/data/sz_adj.csv',header=None)
    adj = np.mat(sz_adj)
    sz_tf = pd.read_csv(r'T-GCN/data/sz_speed.csv')
    return sz_tf, adj

def load_los_data(dataset):
    los_adj = pd.read_csv(r'T-GCN/data/los_adj.csv',header=None)
    adj = np.mat(los_adj)
    los_tf = pd.read_csv(r'T-GCN/data/los_speed.csv')
    return los_tf, adj

def load_monitoring_data(dataset):
    los_adj = pd.read_csv(r'out/out_matrices/monitoring_adj.csv',header=None)
    adj = np.mat(los_adj)
    los_tf = pd.read_csv(r'out/out_matrices/monitoring_weigths.csv', header=None)
    tf = np.mat(los_tf)
    return tf, adj



def preprocess_data(data, time_len, rate, seq_len, pre_len):
    train_size = int(time_len * rate)
    train_data = data[0:train_size]
    test_data = data[train_size:time_len]
    
    print('train_data', train_data.shape)
    print('test_data', test_data.shape)
    
    trainX, trainY, testX, testY = [], [], [], []
    for i in range(len(train_data) - seq_len - pre_len):
        a = train_data[i: i + seq_len + pre_len]
        trainX.append(a[0 : seq_len])
        trainY.append(a[seq_len : seq_len + pre_len])
    for i in range(len(test_data) - seq_len -pre_len):
        b = test_data[i: i + seq_len + pre_len]
        testX.append(b[0 : seq_len])
        testY.append(b[seq_len : seq_len + pre_len])
      
    trainX1 = np.array(trainX)
    trainY1 = np.array(trainY)
    testX1 = np.array(testX)
    testY1 = np.array(testY)
    
    print('TrainX', trainX1.shape)
    print('TrainY', trainY1.shape)
    print('TestX', testX1.shape)
    print('TestY', testY1.shape)
    
    return trainX1, trainY1, testX1, testY1
    
