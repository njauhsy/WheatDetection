# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 20:34:42 2018

@author: 术玉
"""

import cv2
import os

def changesize(source_path,target_path,img_wide,img_high):
    #img_wide=35
    #img_high=75                        #设定尺寸 
    #source_path= 'E:/SRT/posdata/'                  #源文件路径
    #target_path= 'E:/SRT/pos/'        #输出目标文件路径 
    if not os.path.exists(target_path):  
        os.makedirs(target_path) 
    
    img_list=os.listdir(source_path) 
 
    i=0
    for file in img_list:
        i=i+1
        image_source=cv2.imread(source_path+file)#读取图片
        image=cv2.resize(image_source,(img_wide,img_high),0,0,cv2.INTER_CUBIC)
        #cv2.imwrite(target_path+str(i)+".jpg",image)           #重命名并且保存 
        cv2.imwrite(target_path+str(i)+".jpg",image)
    print("图片大小更改完成")
#changesize()
