
import os
import cv2
import time
import win_user
import win_multi2
import changesize
import changegrey
import train_hog
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk


#filename='123.txt'
contral=0
img_wide='70'
img_high='100'
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


def tkimg_resized(img, w_box, h_box, keep_ratio=True):
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

	img1 = img.resize((width, height), Image.ANTIALIAS)
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
	def __init__(self, parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
		center_window(self.root)                   # 将窗体移动到屏幕中央
		self.root.title("机器学习")                 # 窗体标题
		self.root.iconbitmap("images\\Money.ico")  # 窗体图标
		#self.root.grab_set()
		#self.default_code = "1.pack(side='left', expand='no', anchor='w', fill='y', padx=5, pady=5)\n"
		self.body()      # 绘制窗体组件
		self.root.update()#刷新窗口

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

		label(frame, "人工智能应用平台", 16, True).pack(side=tk.LEFT, padx=10)
		#label(frame, "图像模型定制", 12).pack(side=tk.LEFT, padx=100)
		#label(frame, "联系我们", 12).pack(side=tk.LEFT, padx=0)
		#label(frame, "定制模型", 12).pack(side=tk.LEFT, padx=100)
		#label(frame, "", 12).pack(side=tk.RIGHT, padx=20)
		#label(frame, "管理员验证", 12).pack(side=tk.RIGHT, padx=20)
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
		v_seperator(frame, 30).pack(side=tk.RIGHT, fill=tk.Y)
		self.main_right(frame).pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

		return frame

	def main_top(self, parent):
		def label(frame, text, size=12):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(size))

		frame = tk.Frame(parent, bg="white", height=150)

		image_label(frame, "images\\img_title.png", width=240, height=120, keep_ratio=False) \
			.pack(side=tk.LEFT, padx=10, pady=10)

		self.main_top_middle(frame).pack(side=tk.LEFT)

		label(frame, "收起^").pack(side=tk.RIGHT, padx=10)

		frame.propagate(False)
		return frame

	def main_top_middle(self, parent):
		str1 = "定制图像分类模型，可以识别一张图片上的目标物体。"
		str2 = "先对正负样本集进行处理,再对样本文件进行训练,训练结束后可对得到的分类器进行校验。"

		def label(frame, text):
			return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

		frame = tk.Frame(parent, bg="white")

		self.main_top_middle_top(frame).pack(anchor=tk.NW)

		label(frame, str1).pack(anchor=tk.W, padx=10, pady=2)
		label(frame, str2).pack(anchor=tk.W, padx=10)

		return frame

	def main_top_middle_top(self, parent):
		def label(frame, text, size=12, bold=True, fg="blue"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

		frame = tk.Frame(parent, bg="white")

		label(frame, "图像分类模型", 20, True, "black").pack(side=tk.LEFT, padx=10)
		label(frame, "操作文档").pack(side=tk.LEFT, padx=10)
		label(frame, "教学视频").pack(side=tk.LEFT, padx=10)
		label(frame, "常见问题").pack(side=tk.LEFT, padx=10)
		#ttk.Button(frame, text="wenti",width=12).pack(side=tk.LEFT, padx=10)
		#ttk.Button(frame, text="wenti",width=12).pack(side=tk.LEFT, padx=10)
		return frame
	def open_xml(self):
		global contral
		global filename
		filename=tkinter.filedialog.askopenfilename(filetypes=( ("TXT files", "*.txt*"),("XML file", "*.xml*"))) #打开模型或模型的训练文档
		contral=1
		self.root.destroy()
		Window(self.root)
	def found(self):
		self.root.destroy()
		global contral
		contral=0
		Window(self.root)
	def popup(self,message,message1,flag):   #显示提示信息
	
		all_code = self.controls.get(0.0, tk.END)
		win_multi2.Window(self.root, all_code,message,message1,flag)
	
	def test_xml(self):
		self.root.destroy()
		win_user.Window(self.root)
	def manage_data(self):
		self.root.destroy()
		global contral
		contral=2
		Window(self.root)
	def open_data(self):
		def labels(frame, image):
			return tk.Label(frame, image=image)
		global imagepath
		global contral
		#filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","bmp")])
		#filename=tkinter.filedialog.askopenfilename(defaultextension="") #打开任意格式的图片
		#filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","*.bmp*"),("jpg格式","*.jpeg*;.jpeg"),("png格式","*.png")])
		filename = tkinter.filedialog.askdirectory() #打开文件夹
		#print(mypath)
		if filename=='': return
		imagepath =filename
		contral=3
		self.root.destroy()
		Window(self.root)
	def train_xml(self):
		#train_hog.Train()  #增加判断条件,如果已经训练过无需再次训练
		self.root.destroy()
		global contral
		global xmlpath
		contral=4
		#train_hog.Train()  #增加判断条件,如果已经训练过无需再次训练
        #将得到的分类器放到用户所使用的分类器文件夹中
		#filename1="hog_svm/SVM_Test/test.txt"
		
		Window(self.root)
	
	
	
		
		
		
		

	def main_left(self, parent):
		def label(frame, text, size=10, bold=False, bg="white"):
			return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

		frame = tk.Frame(parent, width=180, bg="white")

		label(frame, "模型训练", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)
		tk.Button(frame, text="我的模型",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.open_xml).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="创建模型",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.found).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="训练模型",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.train_xml).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="校验模型",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.test_xml).pack(anchor=tk.W, padx=20, pady=10)
		#label(frame, "校验模型").pack(anchor=tk.W, padx=40, pady=5)
		#label(frame, "发布模型").pack(anchor=tk.W, padx=40, pady=5)

		h_seperator(frame, 10)

		label(frame, "数据处理", 12, True).pack(anchor=tk.W, padx=20, pady=10)
		tk.Button(frame, text="管理数据集",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.manage_data).pack(anchor=tk.W, padx=20, pady=10)
	    #添加一段提示的话,在添加两个按钮,对正负样本进行尺寸的调整,及灰度的转化
		tk.Button(frame, text="查看数据集",bg="slateblue",height=1,width=12,font=ft2,fg="white",command=self.open_data).pack(anchor=tk.W, padx=20, pady=10)  
		#对样本的进行查看,将图片显示在界面上

		frame.propagate(False)
		return frame

	def main_right(self, parent):
	
		def label(frame, text, size=10, bold=False, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))
		def labels(frame, image):
			return tk.Label(frame, image=image)

		def space(n):
			s = " "
			r = ""
			for i in range(n):
				r += s
			return r

		frame = tk.Frame(parent, width=200, bg="white")
		
		if contral==0:
			def mkdir(path):
			# 去除首位空格
				path=path.strip()
			# 去除尾部 \ 符号
				path=path.rstrip("\\")
			# 判断路径是否存在
			# 存在     True
			# 不存在   False
				isExists=os.path.exists(path)
				# 判断结果
				if not isExists:
					#如果不存在则创建目录
					#创建目录操作函数
					os.makedirs(path)
					print (path+' 创建成功')
					return True
				else:
					# 如果目录存在则不创建，并提示目录已存在
					print (path+' 目录已存在')
					return False
			def mkdir_txt(name):
				# 创建txt文件
				while True:
					fname=name
					if os.path.exists(fname):
						print ("Error:'%s' already exists" %fname)
						break 
					else:
						break
				#也即open函数在打开目录中进行检查，如果有则打开，否则新建
				fobj=open(fname,'w')
				fobj.close()	
			def write_txt(name,message5):
					fobj=open(name,'a')  # 这里的a意思是追加这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
					try:
						fobj=open(name,'a')                 # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
					except IOError:
						message6='*** file open error:'
						self.popup(message6,nonestr,0)
					else:
						fobj.write(message5)   #  这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
						fobj.close()                              #   特别注意文件操作完毕后要close
				
				
			#global xml_path
			def rtnkey():      #用于获取文本框输入的字符串
				print(e.get())
				xml_path=e.get()
				path1=xml_path+'//'
				name=e1.get()
				path2=path1+name
				mkdir(xml_path)
				mkdir_txt(path2)
				message5=e2.get()
				write_txt(path2,message5)
				message7='模型说明文档创建成功'
				self.popup(message7,nonestr,0)
			
			e = StringVar()
			e1= StringVar()    
			e2= StringVar()
			#entry = Entry(root, validate='key', textvariable=e, width=50)
			#entry.pack()
			#entry.bind('<Return>', rtnkey)

			label(frame, "创建模型说明文档", 12, True).pack(anchor=tk.W, padx=20, pady=5)

			h_seperator(frame)
			

			f1 = tk.Frame(frame, bg="white")
			label(f1, space(8) + "模型类别:").pack(side=tk.LEFT, pady=5)
			label(f1, "图像识别").pack(side=tk.LEFT, padx=20)
			f1.pack(fill=tk.X)

			f2 = tk.Frame(frame, bg="white")
			label(f2, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
			label(f2, "模型名称:").pack(side=tk.LEFT)
			tk.Entry(f2, bg="white", font=_ft(10), width=25,textvariable=e1).pack(side=tk.LEFT, padx=20)
			f2.pack(fill=tk.X)

			f3 = tk.Frame(frame, bg="white")
			label(f3, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
			label(f3, "存放位置:").pack(side=tk.LEFT)
			tk.Entry(f3, bg="white", font=_ft(10), width=25,textvariable=e).pack(side=tk.LEFT, padx=20)
			f3.pack(fill=tk.X)

			'''
			f4 = tk.Frame(frame, bg="white")
			label(f4, space(5) + "*", fg="red").pack(side=tk.LEFT, anchor=tk.N, pady=5)
			label(f4, "功能描述:").pack(side=tk.LEFT, anchor=tk.N, pady=5)
			text=tk.Text(f4, bg="white", font=_ft(10), height=10,width=40).pack(side=tk.LEFT, padx=20, pady=5)
			message0=text.insert(INSERT,'I Love')
			f4.pack(fill=tk.X)
			
			'''
			f4 = tk.Frame(frame, bg="white")
			label(f4, space(5) + "*", fg="red").pack(side=tk.LEFT, pady=5)
			label(f4, "功能描述:").pack(side=tk.LEFT)
			tk.Entry(f4, bg="white", font=_ft(10),width=35,textvariable=e2).pack(side=tk.LEFT, padx=20)   #如何获取text的文本内容,尝试将entry换成text
			f4.pack(fill=tk.X)
			

			ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)
			tk.Button(frame, text="创建训练文档", width=12,bg="#22C9C9", font=ft2,fg="white",command=rtnkey).pack(anchor=tk.W, padx=112, pady=5)
			self.controls = tk.Text(frame, font=ft2)
			
			#self.controls.pack(expand='yes', fill='both', padx=5, pady='10')
			#self.controls.insert(tk.END, self.default_code)

		frame.propagate(False)
		if contral==1:
			
			frame = tk.Frame(parent, width=200, bg="#E0EEEE")
			global filename
			if filename.strip()=='':
				filename="model/test.txt"
			#f = open(filename, 'rb')              #文件为123.txt
			f = open(filename,encoding='gb18030', errors='ignore')
			str1 = f.read()     #将txt文件的所有内容读入到字符串str中
			#label(frame,str1,15,True).pack(anchor=tk.W, padx=80, pady=10)
			S = tk.Scrollbar(frame)    #增加滚动条显示
			T = tk.Text(frame, height=4, width=150)
			S.pack(side=tk.RIGHT, fill=tk.BOTH)
			T.pack(side=tk.LEFT, fill=tk.BOTH)
			S.config(command=T.yview)
			T.config(yscrollcommand=S.set)
			T.insert('end', str1)
				
			
		if contral==2:  #对数据集进行处理
			def size():      #用于获取文本框输入的字符串
				print(e.get())
				global img_wide
				global img_high
				#global message3
				source_path1=e.get()
				source_path=source_path1+"/"
				target_path1=e1.get()
				target_path=target_path1+"/"
				img_wide=e2.get()
				img_wide=int(img_wide)
				img_high=e3.get()
				img_high=int(img_high)
				if not os.path.exists(source_path):
					message3="路径不存在,请重新输入:"
					self.popup(message3,nonestr,0)
				else :
					changesize.changesize(source_path,target_path,img_wide,img_high)
					message4="图片尺寸已经更改完成:"
					self.popup(message4,nonestr,0)
			def grey():      #用于获取文本框输入的字符串
				#print(e.get())
				global img_wide
				global img_high
				#global message3
				source_path1=e.get()
				source_path=source_path1+"/"
				target_path1=e1.get()
				target_path=target_path1+"/"
				if not os.path.exists(source_path):
					message3="路径不存在,请重新输入:"
					self.popup(message3,nonestr,0)
				else :
					changegrey.changegrey(source_path,target_path)
					message4="图片已经转为灰度图:"
					self.popup(message4,nonestr,0)
			
			e = StringVar()
			e1= StringVar()
			e2= StringVar()
			e3= StringVar()
			#e2= IntVar()
			#e3= IntVar()
			message1="Tips: 输入需要处理前的图片所在的文件夹,及处理后图片所在的文件夹"
			label(frame,message1,15,True).pack(anchor=tk.W, padx=80, pady=20)
			
			t1 = tk.Frame(frame, bg="white")
			label(t1, space(20) + "*", fg="red").pack(side=tk.LEFT, pady=15)
			label(t1, "图片处理前所在文件夹:",12,True).pack(side=tk.LEFT)
			tk.Entry(t1, bg="white", font=_ft(10), width=25,textvariable=e).pack(side=tk.LEFT, padx=20)
			t1.pack(fill=tk.X)
			
			t2 = tk.Frame(frame, bg="white")
			label(t2, space(20) + "*", fg="red").pack(side=tk.LEFT, pady=15)
			label(t2, "图片处理后所在文件夹:",12,True).pack(side=tk.LEFT)
			tk.Entry(t2, bg="white", font=_ft(10), width=25,textvariable=e1).pack(side=tk.LEFT, padx=20)
			t2.pack(fill=tk.X)
			
			message2="Tips: 点击按钮,选择相应的处理方法"
			label(frame,message2,15,True).pack(anchor=tk.W, padx=80, pady=20)
			
			t3 = tk.Frame(frame, bg="white")
			label(t3, space(20) + "*", fg="red").pack(side=tk.LEFT, pady=15)
			label(t3, "更改图片wide为:",12,True).pack(side=tk.LEFT)
			tk.Entry(t3, bg="white", font=_ft(10), width=25,textvariable=e2).pack(side=tk.LEFT, padx=20)
			t3.pack(fill=tk.X)
			
			t4 = tk.Frame(frame, bg="white")
			label(t4, space(20) + "*", fg="red").pack(side=tk.LEFT, pady=15)
			label(t4, "更改图片high为:",12,True).pack(side=tk.LEFT)
			tk.Entry(t4, bg="white", font=_ft(10), width=25,textvariable=e3).pack(side=tk.LEFT, padx=20)
			t4.pack(fill=tk.X)
			
			
			ft2 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
			#tk.Button(frame, text="更改尺寸",bg="#22C9C9", width=12,font=ft2,fg="white",command=rtnkey).pack(anchor=tk.W, padx=100,pady=50)
			tk.Button(frame, text="更改尺寸",bg="#22C9C9", width=13,font=ft2,fg="white",command=size).pack(side=tk.LEFT, padx=100,pady=50)
			tk.Button(frame, text="转为灰度",bg="#22C9C9", width=13,font=ft2,fg="white",command=grey).pack(side=tk.LEFT, padx=100)
			self.controls = tk.Text(frame, font=ft2)
		if contral==3:   #可以一次性显示多张图片
			frame = tk.Frame(parent, width=200, bg="#E0EEEE")
			global imagepath
			global img_wide
			global img_high
			img_wide=int(img_wide)
			img_high=int(img_high)
			imagepath=imagepath+'/'
			img_list=os.listdir(imagepath) 
 
			i=0
			for file in img_list:
				i=i+1
			#for i in range(1,7):
				#t=str(i)
				#image=Image.open(imagepath+'/'+t+'.jpeg')   #改变尺寸
				image=Image.open(imagepath+file)
				image1=image.resize((img_high, img_wide),Image.ANTIALIAS)
				img = ImageTk.PhotoImage(image1)
				#需要改变图像的尺寸,及将非png格式的图片转化为png格式的图片
				lable1=labels(frame, img)
				lable1.image=img
				#lable1.place(x=0,y=0)
				lable1.pack()
				if i==7:
					break
		if contral==4:
          
		
			def progress():
			# 填充进度条
				train_hog.Train()  #增加判断条件,如果已经训练过无需再次训练
				fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
				x = 500  # 未知变量，可更改
				n = 465 / x  # 465是矩形填充满的次数
				for i in range(x):
					n = n + 465 / x
					canvas.coords(fill_line, (0, 0, n, 60))
					frame.update()
					time.sleep(0.001)  # 控制进度条流动的速度
				
				'''
				# 清空进度条
				fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
				x = 500  # 未知变量，可更改
				n = 465 / x  # 465是矩形填充满的次数
 
				for t in range(x):
					n = n + 465 / x
					# 以矩形的长度作为变量值更新
					canvas.coords(fill_line, (0, 0, n, 60))
					frame.update()
					time.sleep(0)  # 时间为0，即飞速清空进度条
				'''
			def show_txt():
				file='hog_svm_data/train1.log'
				f = open(file, 'r')              #文件为123.txt
				str0 = f.read()     #将txt文件的所有内容读入到字符串str中
				#label(frame,str0,10,True).pack(anchor=tk.W, padx=80, pady=10)
				self.popup(str0,nonestr,1)
			def xml_path():
				xmlpath='hog_svm_data/xml/'
				self.popup(xmlpath,nonestr,0)
            
			
					
			#显示训练的结果(打印出训练日志,输出训练结果的存储路径)
			frame = tk.Frame(parent, width=200, bg="#E0EEEE")
			
			ft4 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
			tk.Label(frame, text='训练进度:', bg="white", fg="black",font=ft4).place(x=80, y=20)
			canvas = tk.Canvas(frame, width=465, height=25, bg="white")
			canvas.place(x=160, y=20)
			
			
			ft3 = tkFont.Font(family="微软雅黑", size=12, weight=tkFont.BOLD)
			tk.Button(frame, text="开始训练",bg="#22C9C9",height=1, width=10,font=ft3,fg="white",command=progress).pack(anchor=tk.W, padx=180,pady=80)
			
			message8="Tips: 点击开始训练后,当训练的进度条满了之后,便可查看训练日志"
			label(frame,message8,15,True).pack(anchor=tk.W, padx=80, pady=10)
			tk.Button(frame, text="查看训练日志",bg="#22C9C9", height=1,width=10,font=ft3,fg="white",command=show_txt).pack(anchor=tk.W, padx=180,pady=30)  #pady表示在y方向的间隔
			
			message9="Tips: 点击开始训练后,当训练的进度条满了之后,便可查看训练模型的路径"
			label(frame,message9,15,True).pack(anchor=tk.W, padx=80, pady=10)
			tk.Button(frame, text="查看模型路径",bg="#22C9C9", height=1,width=10,font=ft3,fg="white",command=xml_path).pack(anchor=tk.W, padx=180,pady=30)
			#btn_download = tk.Button(window, text='启动进度条', command=progress)
			#btn_download.place(x=400, y=105)
			self.controls = tk.Text(frame, font=ft3)
				
		return frame
