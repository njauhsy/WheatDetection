# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:39:18 2019

@author: 术玉
"""
import cv2
import os
import win_multi2
import haar_adaboost
import lbp_adaboost
import hog_svm
import live
import tkinter.filedialog
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk

#imagepath='images//mainbg.png'
imagepath='images//wheatbg.jpg'
num=-1
contral=0
str3="未加载图片,无识别结果,请重新加载图片"
str4="未加载图片,无识别结果,请重新加载图片"
str5="未加载图片,无识别结果,请重新加载图片"
astr3="未加载图片,请重新加载图片"
astr4="未加载图片,请重新加载图片"
astr5="未加载图片,请重新加载图片"
estr3="未选用识别方法,请重新选择"
estr4="未选用识别方法,请重新选择"
estr5="未选用识别方法,请重新选择"
flag='haar'
nonestr=''

def center_window(win, width=None, height=None):
	""" 将窗口屏幕居中 """
	screenwidth = win.winfo_screenwidth()
	screenheight = win.winfo_screenheight()
	if width is None:
		width, height = get_window_size(win)[:2]
	size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/3)
	win.geometry(size)


def get_window_size(win, update=True):
	""" 获得窗体的尺寸 """
	if update:
		win.update()
	return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()


def tkimg_resized(img, w_box, h_box, keep_ratio=True):   #用到后面的按照比例缩放里面
	"""对图片进行按比例缩放处理"""
	w, h = img.size

	if keep_ratio:
		if w > h:
			width = w_box
			height = int(h_box * (1.0 * h / w))

		if h >= w:
			height = h_box
			width = int(w_box * (1.0 * w / h))
	else:
		width = w_box
		height = h_box

	img1 = img.resize((width, height), Image.ANTIALIAS)  #高质量
	tkimg = ImageTk.PhotoImage(img1)
	return tkimg


def image_label(frame, img, width, height, keep_ratio=True):
	"""输入图片信息，及尺寸，返回界面组件"""
	if isinstance(img, str):
		_img = Image.open(img)
	else:
		_img = img
	lbl_image = tk.Label(frame, width=width, height=height)

	tk_img = tkimg_resized(_img, width, height, keep_ratio)
	lbl_image.image = tk_img
	lbl_image.config(image=tk_img)
	return lbl_image


def _font(fname="微软雅黑", size=12, bold=tkFont.NORMAL):
	"""设置字体"""
	ft = tkFont.Font(family=fname, size=size, weight=bold)
	return ft


def _ft(size=12, bold=False):
	"""极简字体设置函数"""
	if bold:
		return _font(size=size, bold=tkFont.BOLD)
	else:
		return _font(size=size, bold=tkFont.NORMAL)


def h_seperator(parent, height=2):  # height 单位为像素值
	"""水平分割线, 水平填充 """
	tk.Frame(parent, height=height, bg="whitesmoke").pack(fill=tk.X)


def v_seperator(parent, width, bg="whitesmoke"):  # width 单位为像素值
	"""垂直分割线 , fill=tk.Y, 但如何定位不确定，直接返回对象，由容器决定 """
	frame = tk.Frame(parent, width=width, bg=bg)
	return frame


class Window:
	def __init__(self,  parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (1100, 700))  # 窗体尺寸
		center_window(self.root)                   # 将窗体移动到屏幕中央
		self.root.title("小麦检测")                 # 窗体标题
		self.root.iconbitmap("images\\Money.ico")  # 窗体图标
		self.root.resizable(True, True)          # 设置窗体可改变大小
		#self.root.grab_set()
		self.body()      # 绘制窗体组件
		self.root.update()#刷新窗口
		#self.root.after(1000)

	# 绘制窗体组件
	def body(self):
		self.title(self.root).pack(fill=tk.X)

		self.main(self.root).pack(expand=tk.YES, fill=tk.BOTH)

		self.bottom(self.root).pack(fill=tk.X)

	def title(self, parent):
		""" 标题栏 """

		def label(frame, text, size, bold=False):
			return tk.Label(frame, text=text, bg="black", fg="white", height=2, font=_ft(size, bold))

		frame = tk.Frame(parent, bg="black")

		label(frame, "麦穗识别系统", 16, True).pack(side=tk.LEFT, padx=10)
		#label(frame, "操作文档", 12).pack(side=tk.LEFT, padx=100)
		#label(frame, "常见问题", 12).pack(side=tk.LEFT, padx=0)
		#label(frame, "联系我们", 12).pack(side=tk.LEFT, padx=100)
		#label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
		#label(frame, "登录用户", 12).pack(side=tk.RIGHT, padx=20)
		image_label(frame, "images\\user.png", 40, 40, False).pack(side=tk.RIGHT)

		return frame

	def bottom(self, parent):
		""" 窗体最下面留空白 """

		frame = tk.Frame(parent, height=10, bg="whitesmoke")
		frame.propagate(True)
		return frame

	def main(self, parent):
		""" 窗体主体 """

		frame = tk.Frame(parent, bg="whitesmoke")

		self.main_top(frame).pack(fill=tk.X, padx=30, pady=15)
		self.main_left(frame).pack(side=tk.LEFT, fill=tk.Y, padx=30)
		#v_seperator(frame, 30).pack(side=tk.RIGHT, fill=tk.Y)
		self.main_right(frame).pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

		return frame

	def main_top(self, parent):
		def label(frame, text, size=12):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(size))

		frame = tk.Frame(parent, bg="white", height=150)

		image_label(frame, "images\\mainbg.png", width=180, height=120, keep_ratio=False) \
			.pack(side=tk.LEFT, padx=10, pady=10)

		self.main_top_middle(frame).pack(side=tk.LEFT)

		#label(frame, "收起^").pack(side=tk.RIGHT, padx=10)

		frame.propagate(False)
		return frame

	def main_top_middle(self, parent):
		str1 = "首先加载图片,可对图片进行预处理,提高识别的准确度"
		str2 = "在图片预处理结束后,可以选择麦穗检测模型,并在结果中心查看识别结果"

		def label(frame, text):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

		frame = tk.Frame(parent, bg="white")

		self.main_top_middle_top(frame).pack(anchor=tk.NW)

		label(frame, str1).pack(anchor=tk.W, padx=10, pady=2)
		label(frame, str2).pack(anchor=tk.W, padx=10)

		return frame
	def path(self):
		#self.root.destroy()
		def labels(frame, image):
			return tk.Label(frame, image=image)
		
		global imagepath
		global contral
		#filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","bmp")])
		#filename=tkinter.filedialog.askopenfilename(defaultextension="") #打开任意格式的图片
		filename=tkinter.filedialog.askopenfilename(filetypes=[("jpg格式","*.jpg*;.jpeg"),("bmp格式","*.bmp*"),("png格式","*.png")])
		if filename=='': return
		imagepath =filename
		#wheatdetect.detect()
		contral=0
		self.root.destroy()
		Window(self.root)
	
	def main_top_middle_top(self, parent):
		def label(frame, text, size=12, bold=True, fg="blue"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

		frame = tk.Frame(parent, bg="white")
		ft1 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
		#label(frame, "麦穗检测模型", 20, True, "black").pack(side=tk.LEFT, padx=10)
		tk.Button(frame, text="HAAR+adaboost实现麦穗检测",bg="#22C9C9",width='25',fg="white",font=ft1,command=self.open).pack(side=tk.LEFT, padx=10)
		tk.Button(frame, text="LBP+adaboost实现麦穗检测",bg="#22C9C9",width='25',fg="white",font=ft1,command=self.open1).pack(side=tk.LEFT, padx=10)
		tk.Button(frame, text="HOG+SVM实现麦穗检测",bg="#22C9C9",width='25',fg="white",font=ft1,command=self.open2).pack(side=tk.LEFT, padx=10)
		return frame
	
	def open(self):   #使用haar进行检测
		#self.root.destroy()
		global imagepath
		global num
		global contral
		global str3
		global estr3,astr3
		global flag
		imagepath,num=haar_adaboost.detect(imagepath)  #下一步将产生的图片放到页面上
		contral=0
		str3= "本图片中使用HAAR+Adboost方法识别出"+str(num)+"个麦穗."
		astr3= "本图片中使用HAAR+Adboost"
		estr3="共识别出"+str(num)+"个麦穗."
		flag='haar'
		self.root.destroy()
		Window(self.root)
	def open1(self):   #使用LBP进行检测
		self.root.destroy()
		global imagepath
		global num
		global contral
		global str4
		global estr4,astr4
		global flag
		imagepath,num=lbp_adaboost.detect(imagepath)  #下一步将产生的图片放到页面上
		contral=0
		str4= "本图片中使用LBP+Adboost方法识别出"+str(num)+"个麦穗。"
		astr4= "本图片中使用LBP+Adboost"
		estr4="共识别出"+str(num)+"个麦穗。"
		flag='lbp'
		Window(self.root)
	def open2(self):   #使用LBP进行检测
		self.root.destroy()
		global imagepath
		global num
		global contral
		global str5
		global estr5,astr5
		global flag
		imagepath,num=hog_svm.detect(imagepath)  #下一步将产生的图片放到页面上
		contral=0
		str5= "本图片中使用HOG+SVM方法识别出"+str(num)+"个麦穗。"
		astr5="本图片中使用HOG+SVM"
		estr5="共识别出"+str(num)+"个麦穗。"
		flag='hog'
		Window(self.root)
	def livedetect(self):
		global num
		global estr6,astr6
		global flag
		global contral
		global imagepath
		imagepath,num=live.livedetect()
		astr6="在实时检测中"
		estr6="共识别出"+str(num)+"个麦穗。"
		flag='live'
		contral=0
		self.root.destroy()
		Window(self.root)
	def median_blur(self):    # 中值模糊，对椒盐噪声有很好的去燥效果
		global imagepath
		global contral
		img = cv2.imread(imagepath)
		dst = cv2.medianBlur(img,3)    #模板大小为5*5
		cv2.imwrite('user_data//de_noise//de_noise'+os.path.basename(imagepath),dst)
		self.root.destroy()
		imagepath='user_data//de_noise//de_noise'+os.path.basename(imagepath)
		Window(self.root)
	def pre_treated(self):   	#直方图均衡化(有问题)
		def threshshold(img,num):
			ret, binary= cv2.threshold(img, num, 255, cv2.THRESH_BINARY)
			return binary
		'''
		图像腐蚀
		'''
		def Erode(img):
			kernel1= cv2.getStructuringElement(cv2.MORPH_RECT, (20,14))    
			closed = cv2.morphologyEx(img,cv2.MORPH_DILATE, kernel1)

			closed = cv2.erode(closed, None, iterations=4)    #细节刻画：分别执行4次形态学腐蚀与膨胀
			closed = cv2.dilate(closed, None, iterations=4)
			return closed
		'''
		图像相减
		'''
		def Substract(srcimg,img):
			img = np.abs(img-srcimg) #得到有效信息部分与部分噪声
			return img
		'''
		膨胀
		'''
		def Dilate(img):
			kernel3 =cv2.getStructuringElement(cv2.MORPH_RECT, (3 , 6))
			img =cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel3)
			return img
		
		global imagepath
		global contral
		'''
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		hist=cv2.equalizeHist(gray)
		'''
		

		#img = cv2.resize(img, None, fx=0.25, fy=0.25)
		img = cv2.imread(imagepath,0)
		# 创建CLAHE对象
		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
		# 限制对比度的自适应阈值均衡化
		hist = clahe.apply(img)
		'''
		img = cv2.imread(imagepath)
		(b, g, r) = cv2.split(img)
		bH = cv2.equalizeHist(b)
		gH = cv2.equalizeHist(g)
		rH = cv2.equalizeHist(r)
		# 合并每一个通道
		hist = cv2.merge((bH, gH, rH))
		'''
		cv2.imwrite('user_data//threshshold//equalization'+os.path.basename(imagepath),hist)
		self.root.destroy()
		imagepath='user_data//threshshold//equalization'+os.path.basename(imagepath)
		Window(self.root)
	def grey(self): 
		global imagepath
		global contral
		img = cv2.imread(imagepath)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		cv2.imwrite('Gray_'+os.path.basename(imagepath),gray)
		self.root.destroy()
		imagepath='Gray_'+os.path.basename(imagepath)
		Window(self.root)
	def result(self):
		global contral
		self.root.destroy()
		contral=1
		Window(self.root)
	def compare(self):
		global contral
		self.root.destroy()
		contral=4
		Window(self.root)
	def popup(self,message,message1,flag):   #显示提示信息
	
		all_code = self.controls.get(0.0, tk.END)
		win_multi2.Window(self.root, all_code,message,message1,flag)
	def muti_result(self):
		global str3
		global astr3,estr3
		
		global str4
		global astr4,estr4
		
		global str5
		global astr5,estr5
		
		
		global astr6,estr6
		global flag
		if flag == 'haar':
				self.popup(astr3,estr3,2)
		if flag == 'lbp':
				self.popup(astr4,estr4,2)
		if flag == 'hog':
				self.popup(astr5,estr5,2)
		if flag == 'live':
				self.popup(astr6,estr6,2) 
		
		
		
	
	
	def main_left(self, parent):
		def label(frame, text, size=10, bold=False, bg="white"):
			return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

		frame = tk.Frame(parent, width=180, bg="white")

		label(frame, "图片处理", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)
		tk.Button(frame, text="加载图片",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.path).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="图片去噪",bg="#22C9C9",height=1,width=12,font=ft2,fg="white",command=self.median_blur).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="均衡化",bg="#22C9C9",height=1,width=12,font=ft2,fg="white",command=self.pre_treated).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="实时检测",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.livedetect).pack(anchor=tk.W, padx=20, pady=10)
		

		h_seperator(frame, 10)

		label(frame, "结果分析", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		
		tk.Button(frame, text="识别结果",bg="#22C9C9",height=1,width=12,font=ft2,fg="white",command=self.muti_result).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="对别检测结果",bg="#22C9C9",height=1,width=12,font=ft2,fg="white",command=self.compare).pack(anchor=tk.W, padx=20, pady=10)
		
		self.controls = tk.Text(frame, font=ft2)
		frame.propagate(False)
		return frame

	def main_right(self, parent):
		'''
		global num  #可将各个机器学期所得到的麦穗数量进行对比
		str3= "本图片中使用HAAR+Adboost方法识别出"+str(num)+"个麦穗。"
		'''
		global str3
		global str4
		global flag
        
	    
		def label(frame, text, size=12, bold=True, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))
		def labels(frame, image):
			return tk.Label(frame, image=image)

		def space(n):
			s = " "
			r = ""
			for i in range(n):
				r += s
			return r
		def resize( w_box, h_box, pil_image): #参数是：要适应的窗口宽、高、Image.open后的图片
			w, h = pil_image.size #获取图像的原始大小   
			f1 = 1.0*w_box/w 
			f2 = 1.0*h_box/h    
			factor = min([f1, f2])   
			width = int(w*factor)    
			height = int(h*factor)    
			#return pil_image.resize((width, height), Image.ANTIALIAS)
			return pil_image.resize((width, height),  Image.NEAREST)   #低质量
		frame = tk.Frame(parent, width=200, bg="#E0EEEE")
		global contral
		#global imagepath
		#num=int(num)
			
		if contral==0 :    #找到一个合适的控制变量
			global imagepath
			image=Image.open(imagepath)   #改变尺寸
			#image1=tkimg_resized(image, 500, 450, False)
			#image1=image.resize((700, 600),Image.ANTIALIAS)
			image1=resize(500,450,image)	   #显示顺序为high,wide
			img = ImageTk.PhotoImage(image1)
			#需要改变图像的尺寸,及将非png格式的图片转化为png格式的图片
			lable1=labels(frame, img)
			lable1.image=img
			#lable1.place(x=0,y=0)
			lable1.pack()
		if contral==1 :
			#global str3
			#str= "本图片中使用HAAR+Adboost方法识别"+str(num)+"个麦穗。"
			if flag == 'haar':
				label(frame,str3,18,True).pack(anchor=tk.W, padx=80, pady=10)
			if flag == 'lbp':
				label(frame,str4,18,True).pack(anchor=tk.W, padx=80, pady=10)
			if flag == 'hog':
				label(frame,str5,18,True).pack(anchor=tk.W, padx=80, pady=10)
		if contral==2:
			label(frame,str4,18,True).pack(anchor=tk.W, padx=80, pady=10)
		if contral==4:
			label(frame,str3,18,True).pack(anchor=tk.W, padx=80, pady=10)
			label(frame,str4,18,True).pack(anchor=tk.W, padx=80, pady=10)
			label(frame,str5,18,True).pack(anchor=tk.W, padx=80, pady=10)
			
			
		return frame
