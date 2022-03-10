import numpy as np
def getTau(dis, toReachPoint, fromReachPoint, localdensity_k):
    toTau = np.mean(sorted(dis[toReachPoint])[0:localdensity_k])
    fromTau = np.mean(sorted(dis[fromReachPoint])[0:localdensity_k])
    now_tau = toTau-fromTau
    return now_tau