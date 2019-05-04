import readFile

# 这个值是使用global_mean函数计算出来的，这里我们直接作为一个常量用
global_rating_mean = 49.54496554631943

def user_item_transpose(user_item_rating):
    '''
    之前的字典dict[userID][itemID] = rating
    现在要换成dict[itemID][userID] = rating
    是为了计算单独一个item的bias方便
    '''
    T = {}
    for userID in user_item_rating:
        for itemID in user_item_rating[userID]:
            rating = user_item_rating[userID][itemID]
            if itemID not in T:
                T[itemID] = {}
                T[itemID][userID] = rating
            elif userID not in T[itemID]:
                T[itemID][userID] = rating
    return T


def write_user_mean(user_item_rating):
    file = open("user_bias.txt", 'w+')
    user_bias = {}
    for userID in user_item_rating:
        bias = 0
        for rating in user_item_rating[userID].values():
            bias += rating
        bias = bias/len(user_item_rating[userID].values())
        user_bias[userID] = bias
    for userID in user_bias:
        bias = user_bias[userID]
        string = str(userID) + ' ' + str(bias) + '\n'
        file.write(string)
    print("user bias 写入完成")


def write_item_mean(item_user_rating):
    file = open("item_bias.txt", 'w+')
    item_bias = {}
    for itemID in item_user_rating:
        bias = 0
        for rating in item_user_rating[itemID].values():
            bias += rating
        bias = bias/len(item_user_rating[itemID].values())
        item_bias[itemID] = bias
    for itemID in item_bias:
        bias = item_bias[itemID]
        string = str(itemID) + ' ' + str(bias) + '\n'
        file.write(string)
    print("item bias 写入完成")


def read_mean(filename):
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    bias_dict = {}
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(' ')
        ID = int(line[0])
        rating = float(line[1])
        bias_dict[ID] = rating
    file.close()
    return bias_dict


def global_mean(user_item_rating):
    n_rating = 0  # 总的打分个数
    for userID in user_item_rating:
        n_rating += len(user_item_rating[userID].values())
    mean_rating = 0  # 全局打分的平均值
    for userID in user_item_rating:
        for itemID in user_item_rating[userID]:
            rating = user_item_rating[userID][itemID]
            mean_rating += rating/n_rating
    return mean_rating



if __name__ == '__main__':
    user_item_rating = readFile.read_train('train.txt')
    print(global_mean(user_item_rating))