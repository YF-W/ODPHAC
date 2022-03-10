import AntChoice
import getTau
import pheromonesUpdate

getTaopara = 4
tauTrainlist = []


def slaveAntPathExpansionModel(k, pheList, dis, neighbor, eta, dataAnal):
    """

    :param p1:起始点的index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param eta: eta，控制蚂蚁死亡
    :param dataAnal: 记录每个点被选择成为下一个爬行的点的次数
    :return:
    """

    p1 = pheList.index(min(pheList))
    epsilon = []
    reachPoint = [p1]  # index
    tau = []
    i = 0
    while eta > 0:
        if len(set(reachPoint)) == dis.shape[0] or len(reachPoint) == dis.shape[0]:  # 修改1：条件1：确定跑完所有点（需要去重复）；条件2：遍历达到一定次数.结束遍历
            break
        nextpoint = AntChoice.getSlaveAntChoice(reachPoint[-1] , k, pheList, dis, neighbor)  # 选择下一个要去的点
        dataAnal[nextpoint] += 1
        reachPoint.append(nextpoint)  # 把它加入到达点的列表
        distance = dis[reachPoint[-2]][nextpoint - 1]  # 算出p1 p2的距离
        epsilon.append(distance)  # 计算epsilon
        if i >= 1:
            now_tau = getTau.getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)  # 计算现在的τ
            tauTrainlist.append(now_tau)
            tau.append(now_tau)  # 把现在的τ添加到τ列表里面
            new_eta = etaUpdate(eta, epsilon, now_tau)  # 计算蚂蚁的eta
            eta = new_eta
            nowReachPoint = reachPoint[i + 1]
            oldPhe = pheList[nowReachPoint]
            delta=neighbor[reachPoint[-2],reachPoint[-1]]
            nabla=neighbor[reachPoint[-1],reachPoint[-2]]
            pheList[nowReachPoint - 1] = pheromonesUpdate.pheromonesUpdata(oldPhe, delta, nabla, dis, nowReachPoint,
                                                                           reachPoint[-2], tauTrainlist,
                                                                           pheList)  # 更新信息素列表

        tauTrainElem = getTau.getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)
        tauTrainlist.append(tauTrainElem)
        eta = eta - 0.3
        i = i + 1
    return


def masterAntPathExpansionModel(k, pheList, dis, neighbor, eta, kap, dataAnal):
    """
    :param p1:起始点 index
    :param k: k近邻
    :param pheList: 信息素列表
    :param dis: 距离矩阵
    :param neighbor: 近邻矩阵
    :param eta: eta，控制蚂蚁死亡
    :param kap: k'，p2的k近邻
    :param dataAnal: 记录每个点被选择成为下一个爬行的点的次数
    :return:
    """
    p1 = pheList.index(min(pheList))
    i = 0
    epsilon = []
    reachPoint = [p1]
    tau = []
    while eta > 0:  # 蚂蚁活着时
        if len(list(set(reachPoint))) == dis.shape[0] or len(reachPoint) == dis.shape[
            0]:  # 修改1：条件1：确定跑完所有点（需要去重复）；条件2：遍历达到一定次数.结束遍历
            break
        nextpoint = AntChoice.getMasterAntChoice(reachPoint[-1], k, pheList, dis, neighbor,
                                                 kap)  # 修改2：不采用p1的计算方法，统一用reachPoint数组取值。这里选择下一个要去的点
        dataAnal[nextpoint] += 1
        reachPoint.append(nextpoint)  # 把它加入到达点的列表
        distance = dis[reachPoint[-2]][nextpoint]  # 算出p1 p2的距离
        epsilon.append(distance)  # 计算epsilon
        if i >= 1:
            now_tau = getTau.getTau(dis, reachPoint[-1], reachPoint[-2], getTaopara)  # 计算现在的τ
            tau.append(now_tau)  # 把现在的τ添加到τ列表里面
            new_eta = etaUpdate(eta, epsilon, now_tau)  # 计算蚂蚁的eta
            eta = new_eta
            nowReachPoint = reachPoint[i]  # 新到的点
            oldPhe = pheList[nowReachPoint - 1]  # oldPhe是指reachPoint数组最新（最后）的一个点的信息素
            delta=neighbor[reachPoint[-2],reachPoint[-1]]
            nabla=neighbor[reachPoint[-1],reachPoint[-2]]
            pheList[nowReachPoint - 1] = pheromonesUpdate.pheromonesUpdata(oldPhe, delta, nabla, dis, nowReachPoint,
                                                                           reachPoint[-2], tauTrainlist,
                                                                           pheList)  # 更新信息素列表
        eta = eta - 0.3
        i = i + 1
    return


def etaUpdate(eta, epsilonList, now_tau):
    """
    eta更新
    :param eta:旧的eta
    :param epsilonList:epsilon列表
    :param now_tau: 现在的tau
    :return: 更新后的eta
    """
    sum_eps = 0  # 算出总的epsilon
    for i in range(0, len(epsilonList)):
        sum_eps += epsilonList[i]
    avg_eps = sum_eps / len(epsilonList)
    if avg_eps==0:
        return 0
    else:
        new_eta = eta + now_tau / avg_eps
        return new_eta
