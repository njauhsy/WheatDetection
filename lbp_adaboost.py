# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:52:12 2019

@author: 术玉
"""

import cv2
import sys
import tkinter.filedialog
import os
from PIL import Image, ImageTk


def detect(imagePath):
# Get user supplied values
    img_wide=500
    img_high=450 
    '''
    filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","bmp")])
    if filename=='': return
    imagePath =filename
    '''
    #imagePath ='test4.jpg'
    #cascPath = "BananaCascade.xml"
    cascPath = "lbp_adaboost_data//xml//cascade_lbp20_3575.xml"
# Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
    oldimage = cv2.imread(imagePath)
    img=Image.open(imagePath)   #改变尺寸
    w,h=img.size
    if w>2000 and h>2000:
        image=cv2.resize(oldimage,(0,0),fx=0.185,fy=0.185,interpolation=cv2.INTER_CUBIC)   #可识别出11.5个
    else:
        image=cv2.resize(oldimage,(img_wide,img_high),0,0,cv2.INTER_CUBIC)   #可识别出7个
    
    #image=cv2.resize(oldimage,(0,0),fx=0.155,fy=0.155,interpolation=cv2.INTER_CUBIC)   #可识别出9个
    #image=cv2.resize(oldimage,(0,0),fx=0.165,fy=0.165,interpolation=cv2.INTER_CUBIC)   #可识别出11个
    #image=cv2.resize(oldimage,(0,0),fx=0.175,fy=0.175,interpolation=cv2.INTER_CUBIC)   #可识别出10个
    #image=cv2.resize(oldimage,(0,0),fx=0.185,fy=0.185,interpolation=cv2.INTER_CUBIC)   #可识别出11.5个
    #image=cv2.resize(oldimage,(0,0),fx=0.195,fy=0.195,interpolation=cv2.INTER_CUBIC)   #可识别出10个
    #image=cv2.resize(oldimage,(0,0),fx=0.135,fy=0.135,interpolation=cv2.INTER_CUBIC)   #可识别出3个
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    


# Detect faces in the image
    '''
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
    #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    '''
  
    wheat = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(30, 30),
            maxSize=(100, 100),
    #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    print("Found {0} wheat!".format(len(wheat)))
    num=format(len(wheat))
    print(num)

# Draw a rectangle around the faces
    for (x, y, w, h) in wheat:
        #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #cv2.imshow("find wheat", image)
    #global i
    cv2.imwrite('user_data//result//lbp_'+os.path.basename(imagePath),image)  #先保存为png格式,可以改变
    imagepath1='user_data//result//lbp_'+os.path.basename(imagePath)
    #i=i+1
	#按照路径存储
	#cv2.imwrite('user_data//result//lbp_'+os.path.basename(imagepath),iamge)
	#imagepath1='user_data//result//lbp_'+os.path.basename(imagepath)
    cv2.waitKey(0)
    return imagepath1,num