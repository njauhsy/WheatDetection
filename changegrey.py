# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 19:15:02 2019

@author: 术玉
"""

import cv2
import numpy as np
import os

#img_path = 'E:/SRT/negdata/'
#save_path = 'E:/SRT/greyneg/'

def changegrey(img_path,save_path):
        if not os.path.exists(save_path):  
            os.makedirs(save_path) 
        img_list=os.listdir(img_path)  
        i=0
        for file in img_list:
            i=i+1
            img=cv2.imread(img_path+file)
            graypictures=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(save_path+str(file), graypictures)    
        print("批量处理负样本完成")
