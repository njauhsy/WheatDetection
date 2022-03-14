# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 11:39:47 2018

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
    cascPath = "haar_adaboost_data//xml//cascade.xml"
# Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
    oldimage = cv2.imread(imagePath)
    
    img=Image.open(imagePath)   #改变尺寸
    w,h=img.size
    if w>2000 and h>2000:
        image=cv2.resize(oldimage,(0,0),fx=0.175,fy=0.175,interpolation=cv2.INTER_CUBIC)   #可识别出14个
    else :
        image=cv2.resize(oldimage,(img_wide,img_high),0,0,cv2.INTER_CUBIC)  #可识别出13个
    #image=cv2.resize(oldimage,(img_wide,img_high),0,0,cv2.INTER_CUBIC)  #可识别出13个
    #image=cv2.resize(oldimage,(0,0),fx=0.155,fy=0.155,interpolation=cv2.INTER_CUBIC)   #可识别出12个
    #image=cv2.resize(oldimage,(0,0),fx=0.175,fy=0.175,interpolation=cv2.INTER_CUBIC)   #可识别出14个
    #image=cv2.resize(oldimage,(0,0),fx=0.195,fy=0.195,interpolation=cv2.INTER_CUBIC)   #可识别出13个
    #image=cv2.resize(oldimage,(0,0),fx=0.135,fy=0.135,interpolation=cv2.INTER_CUBIC)   #可识别出10个
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #equ = cv2.equalizeHist(gray)
    
   


# Detect wheat in the image

  
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
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)    #分别代表蓝绿红
    #cv2.imshow("find wheat", image)
    cv2.imwrite('user_data//result//haar_'+os.path.basename(imagePath),image)
    imagepath1='user_data//result//haar_'+os.path.basename(imagePath)
    cv2.waitKey(0)
    return imagepath1,num