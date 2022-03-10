import math
import rouletteModel
import dataPreprocessing


def getSPC(p1, p2, dis, pheList, neighborMatrix):
    """
    获得即点p为中心，与近邻点p1’的从路径信度Subordinate Path Credibility
    :param p1: 第一个点
    :param p2: 第二个点
    :param dis: 距离矩阵
    :param neighborMatrix: 近邻矩阵
    :return: S_pc_<p,p1'> 即以点p为中心，与近邻点p1’的从路径信度Subordinate Path Credibility
    """
    # 信息素
    nowPhe = pheList[p2]
    norPhe = dataPreprocessing.normalize(pheList, nowPhe)

    delta = neighborMatrix[p1][p2]
    nabla = neighborMatrix[p2][p1]
    distance = dis[p1][p2]  # d(p,p1') 即p到p1'的距离，距离矩阵从0开始计数，所以要-1

    factor1 = delta * distance / (nabla + 1)  # 因为前面求的是序号，所以这里要+1，表示第几个
    factor2 = delta * norPhe / (nabla + 1)
    spc = factor1 + factor2
    return spc


def getPPC(p1, p2, kap, dis, neighbor, pheList):
    """
    获得主路径信度Primary Path Credibility
    :param p1: 第一个点。eg：计算第一行数据则输入 1
    :param p2: 第二个点
    :param kap: k'
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :return: PPC: 主路径信度
    """
    nowPhe = pheList[p2]
    factor2 = 0
    sum_spc = 0  # 初始化从路径信度
    getPj = sorted(range(len(neighbor[p2])), key=lambda k: neighbor[p2][k], reverse=False)
    for i in range(0, kap):  # 求从p2到pj的从路径信度，结果累加到sum_pcs上
        pj = getPj[i]
        delta = neighbor[p2][pj]
        slaveNabla = neighbor[pj][p2]
        sum_spc = sum_spc + getSPC(p2, pj, dis, pheList, neighbor)  # p1'的从路径信度
        norPhe = dataPreprocessing.normalize(pheList, nowPhe)
        pj_norPhe = dataPreprocessing.normalize(pheList, pheList[pj])
        if  slaveNabla * (pj_norPhe - norPhe)!=0:
            factor2=factor2+delta/(slaveNabla * (pj_norPhe - norPhe))

    avg_spc = sum_spc / kap  # 计算从路径信度的均值
    avg_factor2 = factor2 / kap
    masterNabla = neighbor[p2][p1]
    factor1 = masterNabla * avg_spc  # 求主路径信度Primary Path Credibility
    PPC = factor1 + avg_factor2
    return PPC


def getMasterAntChoice(p1, k, pheList, dis, neighbor, kap):
    """
    主蚂蚁的选择模型
    :param p1: 出发点
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param kap: k'
    :return: 在k个近邻里，选择要去的那个点
    """
    k=kap
    sum_ppc = 0  # 初始化主路径信度
    ppc = []
    point_list = []
    pheList_index = sorted(range(len(pheList)), key=lambda k: pheList[k])
    for i in list(range(0, int(k / 2))) + list(range(int(len(pheList_index) - k / 2),
                                                       len(pheList_index))):  # 求从p1到pj的主路径信度，结果累加到sum_pcs上 # 2022.2.24修改 以前遍历所有点，现在遍历信息素列表（从小到大）中前、后各(kap/4)个点

        p2 = pheList_index[i]
        now_ppc = getPPC(p1, p2, kap, dis, neighbor, pheList)
        ppc.append(now_ppc)
        point_list.append(p2)
        sum_ppc = sum_ppc + now_ppc  # p1'的主路径信度
    sum_po = 0
    probability = []
    for i in range(0, len(ppc)):  # 2022.2.24改
        if sum_ppc == 0 or ppc[i]:
            now_probability = 0
        else:
            now_probability = math.exp(math.log(ppc[i]) - math.log(sum_ppc))
        probability.append(now_probability)
        sum_po += now_probability

    res = rouletteModel.roulette(probability)
    choice_point = point_list[res]
    return choice_point


def getSlaveAntChoice(p1, k, pheList, dis, neighbor):
    """
    奴隶蚂蚁的选择模型
    :param p1: 出发点 index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :return: 在k个近邻里，选择要去的那个点
    """
    sum_spc = 0  # 初始化从路径信度
    spc = []
    point_list = []
    neighbor_index = sorted(range(len(neighbor[p1])), key=lambda k: neighbor[p1][k])
    for i in range(0, k):  # 求从p1到pj的从路径信度，结果累加到sum_pcs上
        p2 = neighbor_index[i]  # 求p2,p2为index,最小值为0
        now_spc = getSPC(p1, p2, dis, pheList, neighbor)
        spc.append(now_spc)
        point_list.append(p2)
        sum_spc = sum_spc + now_spc  # p1'的从路径信度
    sum_po = 0
    probability = []
    for i in range(0, k):
        if sum_spc == 0 or spc[i] == 0:
            now_probability = 0
        else:
            now_probability = math.exp(math.log(spc[i]) - math.log(sum_spc))
        probability.append(now_probability)
        sum_po += now_probability
    res = rouletteModel.roulette(probability)
    choice_point = point_list[res]
    return choice_point
