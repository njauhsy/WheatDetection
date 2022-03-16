# WheatDetection
基于HAAR+Adaboost与LBP+Adaboost的麦穗识别
基于机器学习的麦穗识别系统分为用户使用和管理员使用两个模块：

1.1 用户使用平台

该部分主要面向用户使用，用户可以加载小麦图片进行相关预处理并进行麦穗检测。

  	用户可以选择需要识别检测的小麦图片。
  
  	用户可以选择对图片进行预处理，处理步骤有:图片去噪，图片均衡化。
  
  	用户可以选择对加载的图片进行麦穗识别，有三种识别模型可以选择
	
 	用户可以在对加载的图片检测过后，在结果分析中查看识别结果
	 
1.2 管理员使用平台

该部分主要面向后台管理人员，能够创建新的训练模型。

  	管理员在训练模型前可以创建训练文档，对训练的模型进行说明。
	
  	管理员可训练自己的图像识别模型。
	
  	管理员可在训练模型前对自己的图像数据进行处理，分别有统一尺寸与灰度化。
	
1.3运行环境

基于机器学习的麦穗识别系统运行环境：

	（1）开发环境：pycharm、python 3.6、opencv
	
	（2）运行环境： 需要在含有python 3.6及其以上的环境下运行
	
下图为用户使用平台

![image](https://user-images.githubusercontent.com/45091118/158158037-5c1a0a18-d42c-4c89-b4d9-3c0ee976e8c7.png)

点击加载图片的按钮可以选择任意英文路径文件夹下的图片，并点击三种检测方法中的一种便可以对加载的小麦图片进行麦穗检测

![image](https://user-images.githubusercontent.com/45091118/158159025-3c675eb2-4ebf-40bd-a196-56dd3c9fee51.png)

点击识别结果的按钮,可以查看使用某种检测方法后识别出来的麦穗的数量

![image](https://user-images.githubusercontent.com/45091118/158159110-f58e8fb0-d691-4ce8-9062-46364cf03f65.png)

分类器的训练过程可以参考：[级联分类器的训练](https://blog.csdn.net/uncle_ll/article/details/122669365?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~aggregatepage~first_rank_ecpm_v1~rank_v31_ecpm-1-122669365.pc_agg_new_rank&utm_term=OpenCV%E8%AE%AD%E7%BB%83%E6%9E%84%E5%BB%BA%E5%88%86%E7%B1%BB%E5%99%A8&spm=1000.2123.3001.4430)





