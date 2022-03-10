import random
import dataPreprocessing
import antRun
import createAntModel
import numpy as np
# import pandas as pd
# import getDeltaNabla


def antModel(data, k, kap, eta, round,slave_ant_proportion,master_ant_proportion):
    """
    找孤立点
    :param data: 数据集
    :param k:k近邻
    :param kap: k'
    :param eta: eta，控制蚂蚁生命
    :param round: 执行几轮，每轮由一次主蚂蚁跑+一次奴隶蚂蚁跑
    :param slave_ant_proportion: 奴隶蚂蚁在数据集中的占比
    :param master_ant_proportion: 主蚂蚁在数据集中的占比
    :return:
    """
    dis = dataPreprocessing.distanceMatrix(data)  # 求距离矩阵
    dis = (dis - np.min(dis)) / (np.max(dis) - np.min(dis))  # 距离矩阵归一化
    neighborMatrix = dataPreprocessing.neighborListALL(dis)  # 求近邻矩阵
    pheList = dataPreprocessing.pheromonesList(data)  # 求信息素矩阵
    n_s, n_m = createAntModel.antCreat(data.shape[0], slave_ant_proportion, master_ant_proportion)  # 求奴隶蚂蚁数、主蚂蚁数

    # #-------- analysis-----------------------
    # 定义分析数据
    dataAnal = [0] * data.shape[0]
    # 主蚂蚁和奴隶蚂蚁交替跑
    for i in range(0, round):
        # print("***************这是第", i + 1, "轮***************")
        for l in range(0, int(n_s)):  # 奴隶蚂蚁跑，修改：不能用变量k
            # print("***************这是第", l + 1, "只蚂蚁SA***************")
            antRun.slaveAntPathExpansionModel(k, pheList, dis, neighborMatrix, eta, dataAnal)
        for j in range(0, int(n_m)):  # 主蚂蚁跑
            # print("***************这是第", j + 1, "只蚂蚁MA***************")
            antRun.masterAntPathExpansionModel( k, pheList, dis, neighborMatrix, eta, kap, dataAnal)
    return pheList
