# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 15:29:31 2019

@author: 术玉
"""

import os
import sys
import cv2
import logging
import numpy as np
from sum0 import logger_init,load_data_set,load_train_samples,extract_hog,get_svm_detector,train_svm

def train_hog(test, svm_detector, logger):
   
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(svm_detector)  
    # opencv自带的训练好了的分类器
    # hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    #hog.save("svmtest.mat")
    hog.save("hog_svm_data/xml/svmtest.xml")
    #xmlpath="hog_svm_data/xml/svmtest.xml"
    #return xmlpath
    
#if __name__ == '__main__':
def Train():
    logger = logger_init()
    pos, neg, test = load_data_set(logger=logger)
    samples, labels = load_train_samples(pos, neg)
    train = extract_hog(samples, logger=logger)
    logger.info('Size of feature vectors of samples: {}'.format(train.shape))
    logger.info('Size of labels of samples: {}'.format(labels.shape))
    svm_detector = train_svm(train, labels, logger=logger)
    train_hog(test, svm_detector, logger)
#Train()
