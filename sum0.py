

# *_*coding:utf-8 *_*

import os
import sys
import cv2
import logging
import numpy as np

def logger_init():
    '''
    自定义python的日志信息打印配置
    :return logger: 日志信息打印模块
    '''

    # 获取logger实例，创建一个logger实体，如果参数为空则返回root logger
    logger = logging.getLogger("PedestranDetect")

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日志
    file_handler = logging.FileHandler("hog_svm_data\\train1.log")
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    #console_handler = logging.StreamHandler(sys.stdout)
    #console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.DEBUG)

    return logger

def load_data_set(logger):
    '''
    导入数据集
    :param logger: 日志信息打印模块
    :return pos: 正样本文件名的列表
    :return neg: 负样本文件名的列表
    :return test: 测试数据集文件名的列表。
    '''
    logger.info('Checking data path!')
    pwd = os.getcwd()
    logger.info('Current path is:{}'.format(pwd))

    # 提取正样本
    pos_dir = os.path.join(pwd, 'hog_svm_data\\posdata1')
    if os.path.exists(pos_dir):
        logger.info('Positive data path is:{}'.format(pos_dir))
        pos = os.listdir(pos_dir)
        logger.info('Positive samples number:{}'.format(len(pos)))

    # 提取负样本
    neg_dir = os.path.join(pwd, 'hog_svm_data\\Negative')
    if os.path.exists(neg_dir):
        logger.info('Negative data path is:{}'.format(neg_dir))
        neg = os.listdir(neg_dir)
        logger.info('Negative samples number:{}'.format(len(neg)))

    # 提取测试集
    test_dir = os.path.join(pwd, 'hog_svm_data\\TestData')
    if os.path.exists(test_dir):
        logger.info('Test data path is:{}'.format(test_dir))
        test = os.listdir(test_dir)
        logger.info('Test samples number:{}'.format(len(test)))

    return pos, neg, test

def load_train_samples(pos, neg):
    '''
    合并正样本pos和负样本pos，创建训练数据集和对应的标签集
    :param pos: 正样本文件名列表
    :param neg: 负样本文件名列表
    :return samples: 合并后的训练样本文件名列表
    :return labels: 对应训练样本的标签列表
    '''
    pwd = os.getcwd()
    pos_dir = os.path.join(pwd, 'hog_svm_data\\posdata1')
    neg_dir = os.path.join(pwd, 'hog_svm_data\\Negative')

    samples = []
    labels = []
    for f in pos:
        file_path = os.path.join(pos_dir, f)
        if os.path.exists(file_path):
            samples.append(file_path)
            labels.append(1.)

    for f in neg:
        file_path = os.path.join(neg_dir, f)
        if os.path.exists(file_path):
            samples.append(file_path)
            labels.append(-1.)

    # labels 要转换成numpy数组，类型为np.int32
    labels = np.int32(labels)
    labels_len = len(pos) + len(neg)
    labels = np.resize(labels, (labels_len, 1))

    return samples, labels

def extract_hog(samples, logger):
    '''
    从训练数据集中提取HOG特征，并返回
    :param samples: 训练数据集
    :param logger: 日志信息打印模块
    :return train: 从训练数据集中提取的HOG特征
    '''
    train = []
    logger.info('Extracting HOG Descriptors...')
    num = 0.
    total = len(samples)
    for f in samples:
        num += 1.
        #logger.info('Processing {} {:2.1f}%'.format(f, num/total*100))
        
        #创建hog
        hog = cv2.HOGDescriptor((64,128), (16,16), (8,8), (8,8), 9) #窗口大小，块大小，块滑动增量，胞元大小，一个胞元（cell）中统计梯度的方向数目
        # hog = cv2.HOGDescriptor()
        img = cv2.imread(f, -1)
        img = cv2.resize(img, (64,128))
        #计算hog特征模块
        descriptors = hog.compute(img)
        #logger.info('hog feature descriptor size: {}'.format(descriptors.shape))    # (3780, 1)
        train.append(descriptors)

    train = np.float32(train)
    train = np.resize(train, (total, 3780))

    return train

def get_svm_detector(svm):
    '''
    导出可以用于cv2.HOGDescriptor()的SVM检测器，实质上是训练好的SVM的支持向量和rho参数组成的列表
    这里我们自行建立svm向量机和参数搭建
    :param svm: 训练好的SVM分类器
    :return: SVM的支持向量和rho参数组成的列表，可用作cv2.HOGDescriptor()的SVM检测器
    '''
    #获取支持向量个数默认  获取支持向量机：矩阵默认是CV_32F
    sv = svm.getSupportVectors()
    #获取alpha和rho  Mat alpha;//每个支持向量对应的参数α(拉格朗日乘子)，默认alpha是float64的
    #Mat svIndex;//支持向量所在的索引svm内参数设置
    
    rho, _, _ = svm.getDecisionFunction(0)
    sv = np.transpose(sv)
    return np.append(sv, [[-rho]], 0)

def train_svm(train, labels, logger):
    '''
    训练SVM分类器
    :param train: 训练数据集
    :param labels: 对应训练集的标签
    :param logger: 日志信息打印模块
    :return: SVM检测器（注意：opencv的hogdescriptor中的svm不能直接用opencv的svm模型，而是要导出对应格式的数组）
    '''
    logger.info('Configuring SVM classifier.')
    svm = cv2.ml.SVM_create()# 创建分类器
    svm.setCoef0(0.0)       #内核函数（POLY/ SIGMOID）的参数
    svm.setDegree(3)        #内核函数POLY的参数
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 1000, 1e-3)#最大迭代次数，结果的精确性
    svm.setTermCriteria(criteria)   #迭代算法的终止准则  
    svm.setGamma(0)
    svm.setKernel(cv2.ml.SVM_LINEAR)# 使用线性核
    svm.setNu(0.5)  #SVM类型（NU_SVC/ ONE_CLASS/ NU_SVR）的参数
    svm.setP(0.1)   # SVM类型 EPSILON_SVR参数
    svm.setC(0.01)  # 惩罚系数
    svm.setType(cv2.ml.SVM_EPS_SVR) #支持向量回归机

    logger.info('Starting training svm.')
    svm.train(train, cv2.ml.ROW_SAMPLE, labels)
    logger.info('Training done.')

    #pwd1 = os.getcwd()   #获得当前'
    pwd='hog_svm_data/xml/'
    isExists=os.path.exists(pwd)
	# 判断结果
    if not isExists:
        os.makedirs(pwd)
    else :
        return False
    model_path = os.path.join(pwd, 'svm.xml')  #
    svm.save(model_path)
    logger.info('Trained SVM classifier is saved as: {}'.format(model_path))

    return get_svm_detector(svm)

