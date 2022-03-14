# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
import tkutils as tku


colors = ['red', 'yellow', 'blue', 'green', 'pink', 'slateblue', 'lawngreen', 'orange', 'gold', 'cyan',
		  'cyan', 'brown', 'gray', 'royalblue', 'magenta', 'olive', 'black']

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
		  
class Window:
	def __init__(self, parent, pack_code,message,message1,flag):
		self.root = tk.Toplevel()
		self.parent = parent
		if flag==0:
			self.root.geometry("%dx%d" % (250, 100))
		if flag==1:
			self.root.geometry("%dx%d" % (550, 400))
		if flag==2:
			self.root.geometry("%dx%d" % (350, 200))
		tku.center_window(self.root)
		self.root.title("提示")
		self.root.grab_set()
		self.root.resizable(True, True)
		#self.pack_code = pack_code
		self.body(message,message1,flag)
	# 绘制窗体组件
	def body(self,message,message1,flag):
	
		if flag==0:   #显示提示
			self.title(self.root,message).pack(fill=tk.X)
			
		if flag==1:   #显示训练日志
			self.title1(self.root,message).pack(expand=tk.YES, fill=tk.BOTH)
			
		if flag==2:   #显示识别麦穗数量
			self.title2(self.root,message,message1).pack(expand=tk.YES, fill=tk.BOTH)
			

		#self.main(self.root).pack(expand=tk.YES, fill=tk.BOTH)

		self.bottom(self.root).pack(fill=tk.X)
	
	def title(self,parent,message):
		def label(frame, text, size=12, bold=True, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg,font=_ft(size, bold))
		frame = tk.Frame(parent, width=100, bg="#E0EEEE")
		label(frame,message,10,True).pack(anchor=tk.W, padx=30, pady=10)
		return frame
	def title1(self,parent,message):
		def label(frame, text, size=12, bold=True, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg,font=_ft(size, bold))
		frame = tk.Frame(parent, width=100, bg="#E0EEEE")
		S = tk.Scrollbar(frame)
		T = tk.Text(frame, height=5, width=100)
		S.pack(side=tk.RIGHT, fill=tk.BOTH)
		T.pack(side=tk.LEFT, fill=tk.BOTH)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert('end', message)
		#label(frame,message,10,True).pack(anchor=tk.W, padx=30, pady=10)
		return frame
	def title2(self,parent,message,message1):
		def label(frame, text, size=12, bold=True, fg="black"):
			return tk.Label(frame, text=text, bg="white", fg=fg,font=_ft(size, bold))
		frame = tk.Frame(parent, width=100, bg="#E0EEEE")
		label(frame,message,15,True).pack(anchor=tk.W, padx=30, pady=10)
		label(frame,message1,15,True).pack(anchor=tk.W, padx=30, pady=10)
		return frame
	def destroy(self):
		self.root.destroy()
	def bottom(self, parent):
		frame = tk.Frame(parent, width=50, bg="#E0EEEE")
		ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)
		tk.Button(frame, text="确定",bg="#22C9C9",height=1,width=12,font=ft2,fg="white",command=self.destroy).pack(anchor=tk.W, padx=130, pady=20)
		#.pack(fill=tk.X)
		return frame

	
