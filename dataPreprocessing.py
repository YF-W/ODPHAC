import matplotlib.pyplot as plt
import numpy as np  # 调用 numpy 包作为 np 使用
from scipy.spatial import distance  # 调用distance函数求距离矩阵
import math

def loadData(filename):
    """
    加载数据
    :param filename: 文件名
    :return: 数据集 numpy集合的形式
    """
    data = np.loadtxt(filename)  # 加载数据
    return data


def scatterPlot(data):
    """
    数据可视化（散点图）
    :param data: 数据集
    :return: 无返回
    """
    x = data[:, 0]
    y = data[:, 1]
    n = np.arange(data.shape[0])

    fig, ax = plt.subplots()
    ax.scatter(x, y)

    for i, txt in enumerate(n):
        ax.annotate(txt + 1, (x[i], y[i]))
    plt.show()


def distanceMatrix(matrix):
    """
    距离矩阵
    :param matrix: 原始坐标数据构成的矩阵
    :return: dis_matrix: 距离矩阵
    """
    matrix = np.array(matrix, dtype=np.float64)  # 把传入的matrix转化为numpy类型的矩阵( ndarray )
    dis_matrix = distance.cdist(matrix, matrix,
                                'euclidean')  # 调用distance函数，求矩阵AB的距离，A=matrix，B=matrix，‘Euclidean’表示欧式距离
    return dis_matrix  # 返回一个距离矩阵


def neighborPointList(p1, disMatrix):
    """
    得到近邻矩阵里的p1的那一列，依次排列出p1的近邻
    :param p1:要找近邻的点
    :param disMatrix:距离矩阵
    :return:按序排列的p1的近邻
    """
    keys = []  # 创建list
    for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
        keys.append(i)
    a = dict(zip(keys, disMatrix[p1 - 1]))  # 压缩字典
    a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    neighborArr = []  # p1近邻矩阵的那列
    for i in range(1, len(a)):
        neighborArr.append(a[i][0])  # 把返回的值加入的近邻列
    return neighborArr


def neighborListALL(disMatrix):
    """
    得到完整的近邻矩阵
    :param disMatrix:距离矩阵
    :return:近邻矩阵
    """
    res = []
    for i in range(0, disMatrix.shape[1]):  # 把近邻列加入到近邻矩阵内
        sorted_id = sorted(range(len(disMatrix[i])), key=lambda k: disMatrix[i][k], reverse=False)
        temp=sorted_id
        sorted_id=sorted(range(len(temp)), key=lambda k: temp[k], reverse=False)
        res.append(sorted_id)
    return np.array(res)


def pheromonesList(data):
    pointNum = data.shape[0]
    pheList = []
    for i in range(0, pointNum):
        pheList.append(10)
    return pheList


def randomData(mu, sigma, row, col):
    """
    产生高斯分布数据
    :param mu: 均值
    :param sigma: 标准差
    :param row: 行数
    :param col: 列数
    :return: 高斯分布数据集
    """
    return np.random.normal(mu, sigma, [row, col])


def normalize(list, value):
    range = max(list) - min(list)
    if range == 0:
        return 1
    elif value-min(list)==0:
        return 0
    else:
        value2 = math.exp(math.log(value-min(list)) -math.log(range))
        return value2
