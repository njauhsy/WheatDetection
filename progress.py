# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:13:00 2019

@author: 术玉
"""

import tkinter as tk
import time
 
# 创建主窗口
window = tk.Tk()
window.title('进度条')
window.geometry('630x150')
 
# 设置下载进度条
tk.Label(window, text='下载进度:', ).place(x=50, y=60)
canvas = tk.Canvas(window, width=465, height=22, bg="white")
canvas.place(x=110, y=60)
 
# 显示下载进度
def progress():
    # 填充进度条
    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
    x = 500  # 未知变量，可更改
    n = 465 / x  # 465是矩形填充满的次数
    for i in range(x):
        n = n + 465 / x
        canvas.coords(fill_line, (0, 0, n, 60))
        window.update()
        time.sleep(0.02)  # 控制进度条流动的速度
 
    # 清空进度条
    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
    x = 500  # 未知变量，可更改
    n = 465 / x  # 465是矩形填充满的次数
 
    for t in range(x):
        n = n + 465 / x
        # 以矩形的长度作为变量值更新
        canvas.coords(fill_line, (0, 0, n, 60))
        window.update()
        time.sleep(0)  # 时间为0，即飞速清空进度条
 
btn_download = tk.Button(window, text='启动进度条', command=progress)
btn_download.place(x=400, y=105)
 
window.mainloop()