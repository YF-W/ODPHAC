import scipy.io as scio
from pandas.core.frame import DataFrame
import time
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import hamming_loss
from sklearn.metrics import jaccard_score
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import median_absolute_error
import AntModel
import os
import gc
import warnings


# warnings.filterwarnings("ignore")


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()


def save_report_row(y_true, y_predict_type, y_predict_scores):
    report_row = []

    # accuracy_score
    report_row.append(accuracy_score(y_true, y_predict_type))
    # metrics
    report_row.append(metrics.precision_score(y_true, y_predict_type, average='micro'))
    report_row.append(metrics.precision_score(y_true, y_predict_type, average='macro'))
    # recall
    report_row.append(metrics.recall_score(y_true, y_predict_type, average='micro'))
    report_row.append(metrics.recall_score(y_true, y_predict_type, average='macro'))
    # F1
    report_row.append(metrics.f1_score(y_true, y_predict_type, average='weighted'))
    # kappa score
    report_row.append(cohen_kappa_score(y_true, y_predict_type))
    # ROC
    report_row.append(roc_auc_score(y_true, y_predict_scores))
    # 距离
    # 海明距离
    report_row.append(hamming_loss(y_true, y_predict_type))
    # Jaccard距离
    report_row.append(jaccard_score(y_true, y_predict_type))
    # 回归
    # 可释方差值（Explained variance score）
    report_row.append(explained_variance_score(y_true, y_predict_type))
    # 平均绝对误差（Mean absolute error）
    report_row.append(mean_absolute_error(y_true, y_predict_type))
    # 均方误差（Mean squared error）
    report_row.append(mean_squared_error(y_true, y_predict_type))
    # 中值绝对误差（Median absolute error）
    report_row.append(median_absolute_error(y_true, y_predict_type))
    # R方值，确定系数
    report_row.append(r2_score(y_true, y_predict_type))
    return report_row


for k in range(18,19):
    gc.collect()
    # load data
    dataFile = 'datasets/glass.mat'  # 修改1：数据集
    dataName = "glass"  # 修改1：数据集
    input_data = scio.loadmat(dataFile)
    X_train = input_data['X']
    y_true = input_data['y']
    report = []

    start_k = 99
    end_k = 100  # 修改2：k值 注意左闭右开

    pointNum = np.shape(X_train)[0]
    info = []
    outlier_num = sum(y_true)[0]
    y_predict_type = [0] * pointNum
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("k=", k)
    algorithm = "Ant"  # 修改3：算法名
    start_time = time.perf_counter()
    # model building
    y_predict_scores = AntModel.antModel(X_train, pointNum-1, k, 1, 3,0.5,0.2)  # (data, k, kap, eta, round,slave_ant_num,master_ant_num)
    # get outlier scores
    end_time = time.perf_counter()

    y_predict_score1 = sorted(y_predict_scores, reverse=True)  # 由高到低排序
    y_predict_confidence = []

    for i in range(0, int(outlier_num)):
        outlier_index = y_predict_scores.index(y_predict_score1[i])
        y_predict_type[outlier_index] = 1

    y_predict_confidence = [-1] * pointNum

    # save result
    report_row = save_report_row(y_true, y_predict_type, y_predict_scores)

    run_time = end_time - start_time
    save_row = [dataName, algorithm, k, run_time]
    save_row.extend(report_row)
    report.append(save_row)
    rownames = np.array(range(1, np.size(y_predict_scores, 0) + 1)).astype(int)  # 点号
    socore_data = np.c_[
        rownames.T, np.array(y_predict_type).T, np.array(y_predict_scores).T, np.array(y_predict_confidence).T]

    # ----------保存每轮的数据---------
    # 点号；预测类型；预测得分；预测置信度
    if not os.path.exists("scoreData/" + dataName + "/" + algorithm):
        os.makedirs("scoreData/" + dataName + "/" + algorithm)
    print("------save scoreData------")
    np.savetxt("scoreData/" + dataName + "/" + algorithm + "/" + str(k) + ".csv", socore_data, delimiter=',',
               comments='', header="pointNum,type,score,confidence")

    # 混淆矩阵
    if not os.path.exists("confusionMatrix/" + dataName + "/" + algorithm):
        os.makedirs("confusionMatrix/" + dataName + "/" + algorithm)
    print("------save confusionMatrix------")
    np.savetxt("confusionMatrix/" + dataName + "/" + algorithm + "/" + str(k) + ".csv",
               confusion_matrix(y_true, y_predict_type), delimiter=',', comments='', header="0,1")
    # --x--------保存每轮的数据-------x--

    # ----------保存所有轮的数据----------
    report_dataFrame = DataFrame(report)

    report_dataFrame.columns = ["dataName", "algorithm", "k", "run_time", "accuracy_score", "metrics_micro",
                                "metrics_macro", "recall_micro", "recall_macro", "F1", "kappa_score", "ROC",
                                "Hamming_distance", "Jaccard_distance", "Explained_variance_score",
                                "Mean_absolute_error",
                                "Mean_squared_error", "Median_absolute_error", "r2_score"]

    if not os.path.exists("Report/" + dataName + "/" + algorithm):
        os.makedirs("Report/" + dataName + "/" + algorithm)
        print("------save Report------")
        with open("Report/" + dataName + "/" + algorithm + "/" + str(start_k) + "_" + str(end_k) + ".csv", 'ab') as f:
            np.savetxt(f, report_dataFrame, delimiter=',', fmt='%s', comments='',
                       header="dataName, algorithm, k, run_time, accuracy_score, metrics_micro,metrics_macro, recall_micro, recall_macro, F1, kappa_score, ROC,Hamming_distance, Jaccard_distance, Explained_variance_score, Mean_absolute_error,Mean_squared_error, Median_absolute_error, r2_score")
        # --x--------保存所有轮的数据--------x--
    print("------save Report------")
    with open("Report/" + dataName + "/" + algorithm + "/" + str(start_k) + "_" + str(end_k) + ".csv", 'ab') as f:
        np.savetxt(f, report_dataFrame, delimiter=',', fmt='%s', comments='')
    # --x--------保存所有轮的数据--------x--dat
