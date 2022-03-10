import random


def roulette(fitness):
    """
    轮盘赌策略 随机接受（Stochastic Acceptance）的实现方法
    参考:https://github.com/mangwang/PythonForFun/blob/master/rouletteWheelSelection.py
    :param fitness:传入的概率数据，可以不按从小到大的顺序排列 (list or tuple)
    :return: 选择的点
    """
    N = len(fitness)  # 概率数据的长度
    maxFit = max(fitness)
    if maxFit==0:
        return -1
    while True:
        # randomly select an individual with uniform probability
        ind = int(N * random.random())
        # with probability wi/wmax to accept the selection
        if random.random() <= fitness[ind] / maxFit:
            return ind

#测试数据
# p = [0.3, 0.2, 0.1, 0.4]
# res = [0, 0, 0, 0]
# for x in range(10000):
#     index = roulette(p)
#     res[index] = res[index] + 1
# print(res)
