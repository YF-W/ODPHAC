def getDelta(p1, p2, k, neighborMatrix):
    """
    得到Δ([p1,k],p2]) 在k个近邻内，以p1为主视角，p2是p1的第几近邻
    :param p1: 第一个点 index
    :param p2: 第二个点 index
    :param k: k近邻
    :param neighborMatrix: 近邻矩阵
    :return: Δ([p1,k],p2])
    """
    #
    # keys = []
    # for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
    #     keys.append(i)
    # a = dict(zip(keys, disMatrix[p1]))  # 压缩字典
    # a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    # delta = 0
    # for i in range(0, k):  # 从更新后的排序里找到p2的位置
    #     if neighborMatrix[p1][i] == p2:
    #         delta = i
    # if delta > k:  # 如果没在k近邻内，则Δ为-1
    #     delta = k
    return neighborMatrix[p1,p2]


def getNabla(p1, p2, neighborMatrix):
    """
    得到Nabla([p1,k],p2]) 在k个近邻内，以p2为主视角，p1是p2的第几近邻
    :param p1: 第一个点
    :param p2: 第二个点
    :param k: k近邻
    :param neighborMatrix: 距离矩阵
    :return: Δ([p1,k],p2])
    """
    # keys = []
    # for i in range(1, disMatrix.shape[1] + 1):  # 创建key值
    #     keys.append(i)
    # a = dict(zip(keys, disMatrix[p1 - 1]))  # 压缩字典
    # a = sorted(a.items(), key=lambda x: x[1])  # 更新排序后为列表
    # delta = 0
    # for i in range(1, len(a)):  # 从更新后的排序里找到p2的位置
    #     if a[i][0] == p2:
    #         delta = i
    return neighborMatrix[p2][p1]
