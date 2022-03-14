# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:58:46 2019

@author: 术玉
"""

import os
import sys
import cv2
import logging
import numpy as np
from PIL import Image, ImageTk


target_path= 'E:/'        #输出目标文件路径
i=0

def detect(imagePath):
    
    img_wide=500
    img_high=450 
   
    hog = cv2.HOGDescriptor()
    hog.load("hog_svm_data//xml//svmtest.xml")

    
    
    img1=Image.open(imagePath)   #改变尺寸
    oldimage = cv2.imread(imagePath)
    w,h=img1.size
    if w>800 and h>800:
        img=cv2.resize(oldimage,(0,0),fx=0.175,fy=0.175,interpolation=cv2.INTER_CUBIC)   #可识别出14个
    else :
        img=cv2.resize(oldimage,(img_wide,img_high),0,0,cv2.INTER_CUBIC)  #可识别出13个
    #img=cv2.resize(img,(0,0),fx=0.175,fy=0.175,interpolation=cv2.INTER_CUBIC)   #可识别出10个
    rects, _ = hog.detectMultiScale(img, winStride=(16,16), padding=(0,0), scale=1.12)  #A
    #rects, _ = hog.detectMultiScale(img, winStride=(16,16), padding=(0,0), scale=1.11)
    for (x,y,w,h) in rects:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
    num=format(len(rects))
    print(num)
    #按照路径存储
    cv2.imwrite('user_data//result//hog_'+os.path.basename(imagePath),img)
    imagepath1='user_data//result//hog_'+os.path.basename(imagePath)
    cv2.waitKey(0)
    return imagepath1,num
    


   