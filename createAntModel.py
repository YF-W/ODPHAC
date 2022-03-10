def antCreat(m, var_sigma, sigma):
    """
    蚂蚁创建模型
    :param m: 点的数量
    :param var_sigma:  ς 限制奴隶蚂蚁的数量 0<var_sigma<0.5
    :param sigma: σ 限制大蚂蚁的数量 0<sigma_indes<0.2*var_sigma
    :return: n_s奴隶蚂蚁数量  n_m大蚂蚁数量
    """
    # if var_sigma > 0.5 or var_sigma < 0:  # 要保证 0<var_sigma<0.5
    #     print("传入参数有误\n应该满足0<var_sigma<0.5")
    # if sigma < 0 or sigma > 0.2 * var_sigma:  # 要保证 0<sigma_indes<0.2*var_sigma
    #     print("传入参数有误\n应该满足0<sigma<0.2*var_sigma")
    # else:
    n_s = int(var_sigma * m)  # 奴隶蚂蚁数量，为了防止小数所以对结果取整
    n_m = int(sigma * m)  # 主蚂蚁数量，为了防止小数所以对结果取整
    if n_s == 0:
        n_s += 1
    if n_m == 0:
        n_m += 1
    return n_s, n_m

# 测试数据
# num_slave, num_master = antCreat(20, 0.5, 0.1)
# print(num_slave, num_master)
