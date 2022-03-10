import numpy as np
import dataPreprocessing
from sklearn import preprocessing


def pheromonesUpdata(oldPheromones, delta, nabla, dis, toPoint, frompoint, tauTrainlist, pheList):
    """
    信息素更新

    """
    # --------factor4-----------
    # 对pheList初始化
    # maxPhe = max(pheList)
    # minPhe = min(pheList)
    # oldPhe = oldPheromones
    normalizedPhe = dataPreprocessing.normalize(pheList,oldPheromones)
    # Get factor4
    factor4 = normalizedPhe
    # --X------factory4---------X--

    considerneighbor_num = max(delta, nabla)
    factor3 = avgdistance(frompoint, toPoint, dis, considerneighbor_num)
    # factor3 = 1
    factor2 = (nabla+1) / (delta+1)

    range_min = -10
    range_max = 10
    k = (range_max - range_min) / (max(tauTrainlist) - min(tauTrainlist))
    transform_value = [k * (x - min(tauTrainlist)) + range_min for x in tauTrainlist]

    # k = (range_max - range_min) / (max(tauTrainlist) - min(tauTrainlist))
    # transform_value = [(range_max - range_min) * (x - min(tauTrainlist)/ (max(tauTrainlist) - min(tauTrainlist)) ) + range_min for x in tauTrainlist]



    factor1 = transform_value[-1]

    newPheromones = oldPheromones + factor1 * factor3 + factor2  * factor4

    return newPheromones


def avgdistance(frompoint, toPoint, dis, considerneighbor_num):
    if considerneighbor_num == 0:  # 表示两个点之间无其他点
        return 1
    else:
        neardisarray_from=0
        neardisarray_to=0
        sortdis_from = dis[frompoint].argsort()  # 获取距离从小到大的近邻序号
        sortdis_to = dis[toPoint].argsort()
        for i in range(0,considerneighbor_num):
            neardisarray_from=neardisarray_from+dis[frompoint][sortdis_from[i]]
            neardisarray_to=neardisarray_to+ dis[toPoint][sortdis_to[i]]
        # neardisarray_from = dis[frompoint][sortdis_from[1:considerneighbor_num]]  # 获取前considerneighbor_num个最近的距离
        pointdismean_from = np.mean(neardisarray_from)  # 计算平均距离
        pointdismean_to = np.mean(neardisarray_to)
        if pointdismean_to==0 or pointdismean_to==0:
            return 1
        factor3 = (pointdismean_to+1) / (pointdismean_from+1)
        return factor3





def map(data, MIN, MAX):
    """
    归一化映射到任意区间
    :param data: 数据
    :param MIN: 目标数据最小值
    :param MAX: 目标数据最小值
    :return:
    """
    d_min = np.max(data)  # 当前数据最大值
    d_max = np.min(data)  # 当前数据最小值
    return MIN + (MAX - MIN) / (d_max - d_min) * (data - d_min)
