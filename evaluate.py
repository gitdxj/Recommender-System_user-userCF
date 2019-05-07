import math

def read_pred(filename):
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    lines = file.readlines()
    prediction = list()
    for line in lines:
        line = line.strip()
        line = line.split(':')
        true = int(line[0])
        pred = float(line[1])
        true_pred_pair = (true, pred)
        prediction.append(true_pred_pair)
    return prediction

def rmse_cal(prediction):
    N = len(prediction)
    rmse = 0
    for each in prediction:
        true = each[0]
        pred = each[1]
        rmse += (true - pred)*(true - pred)/N
    rmse = math.sqrt(rmse)
    return rmse


if __name__ == '__main__':
    prediction = read_pred('pred.txt')
    rmse = rmse_cal(prediction)
    print(rmse)
    # line = "0:8.551823527436209"
    # print(line.strip().split(':'))