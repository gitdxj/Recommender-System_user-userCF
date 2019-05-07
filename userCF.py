import readFile
from simiCal import *
import bias
from sklearn.model_selection import train_test_split

'''
使用协同过滤的方法进行对打分进行预测
'''

def set_split(user_item_rating, size):
    '''
    划分训练集和验证集
    '''
    full_set = list()  # 先把全部的数据变为tuple的形式 (userID, itemID, rating)
    for userID in user_item_rating:
        for itemID in user_item_rating[userID]:
            rating = user_item_rating[userID][itemID]
            full_set.append((userID, itemID, rating))
    print("full_set所有的元素一共有：" + str(len(full_set)))
    train_set, vali_set = train_test_split(full_set, test_size=size)
    return tuple2dict(train_set), tuple2dict(vali_set)


def tuple2dict(tuple_list):
    user_item_rating = {}
    for each in tuple_list:
        userID = each[0]
        itemID = each[1]
        rating = each[2]
        if userID not in user_item_rating:
            user_item_rating[userID] = {}
            user_item_rating[userID][itemID] = rating
        elif itemID not in user_item_rating[userID]:
            user_item_rating[userID][itemID] = rating
    return user_item_rating


def predict_bias(train_dict, vali_dict):
    prediction = dict()
    m = bias.global_rating_mean  # 用来计算bxi
    item_mean = bias.read_mean("item_bias.txt")  # item_bias[itemID]为该item的bias
    user_mean = bias.read_mean("user_bias.txt")  # user_bias[userID]为该user的bias
    for userID_x in vali_dict:
        for itemID in vali_dict[userID_x]:
            mean_x = user_mean[userID_x]
            mean_i = item_mean[itemID]
            b_x_i = mean_x + mean_i - m
            rating_pred = 0  # 预测的打分
            deno = 0  # 分母的部分
            user_simi = top_k_similar_user(train_dict, userID_x, 100, 0)  # 和userID有最高的相似度的user
            for userID_y in user_simi:
                mean_y = user_mean[userID_y]
                b_y_i = mean_y + mean_i - m
                if itemID in train_dict[userID_y]:  # 如果userID_y对itemID打过分
                    rating_pred += user_simi[userID_y]*train_dict[userID_y][itemID] - b_y_i
                    deno += user_simi[userID_y]
            if deno != 0:
                rating_pred = rating_pred/deno
            else:
                rating_pred = 0
                print("没有相似用户对该item打过分")
            rating_pred += b_x_i
            if userID_x not in prediction:
                prediction[userID_x] = dict()
            prediction[userID_x][itemID] = rating_pred
            true_rating = vali_dict[userID_x][itemID]
            string = "true: " + str(true_rating) + '\n' + "pred: " + str(rating_pred) + '\n'
            print(string)
    print("hhhhhhhh")
    return prediction



def predict(train_dict, vali_dict):
    item_attr_dict = readFile.get_item_attribute_dict()
    attr_item_dict = readFile.get_item_attribute_cluster_dict()
    print("attr")
    prediction = dict()
    for userID_x in vali_dict:
        for itemID in vali_dict[userID_x]:
            rating_pred = 0  # 预测的打分
            deno = 0  # 分母的部分
            user_simi = top_k_similar_user(train_dict, userID_x, 100)  # 和userID有最高的相似度的user
            for userID_y in user_simi:
                if itemID in train_dict[userID_y]:  # 如果userID_y对itemID打过分
                    item_rating = train_dict[userID_y][itemID]
                else:  # userID_y没有对itemID打过分，则用item_attribute把对应的打分估计出来
                    item_rating = item_rating_estimate(attr_item_dict, item_attr_dict, train_dict[userID_y], itemID)
                    if None == item_rating:
                        continue
                rating_pred += user_simi[userID_y] * item_rating
                deno += user_simi[userID_y]
            if deno != 0:
                rating_pred = rating_pred/deno
            else:
                rating_pred = 0
                print("没有相似用户对该item打过分，甚至连相似的item找上也不行")
            if userID_x not in prediction:
                prediction[userID_x] = dict()
            prediction[userID_x][itemID] = rating_pred
            true_rating = vali_dict[userID_x][itemID]
            string = "true: " + str(true_rating) + '\n' + "pred: " + str(rating_pred) + '\n'
            print(string)
    print("hhhhhhhh")
    return prediction


def predict_attr_bias(train_dict, vali_dict):
    m = bias.global_rating_mean  # 用来计算bxi
    item_mean = bias.read_mean("item_bias.txt")  # item_bias[itemID]为该item的bias
    user_mean = bias.read_mean("user_bias.txt")  # user_bias[userID]为该user的bias
    item_attr_dict = readFile.get_item_attribute_dict()
    attr_item_dict = readFile.get_item_attribute_cluster_dict()
    print("attr")
    prediction = dict()
    for userID_x in vali_dict:
        for itemID in vali_dict[userID_x]:
            mean_x = user_mean[userID_x]
            mean_i = item_mean[itemID]
            b_x_i = mean_x + mean_i - m
            rating_pred = 0  # 预测的打分
            deno = 0  # 分母的部分
            user_simi = top_k_similar_user(train_dict, userID_x, 100)  # 和userID有最高的相似度的user
            for userID_y in user_simi:
                mean_y = user_mean[userID_y]
                b_y_i = mean_y + mean_i - m
                if itemID in train_dict[userID_y]:  # 如果userID_y对itemID打过分
                    item_rating = train_dict[userID_y][itemID]
                else:  # userID_y没有对itemID打过分，则用item_attribute把对应的打分估计出来
                    item_rating = item_rating_estimate(attr_item_dict, item_attr_dict, train_dict[userID_y], itemID)
                    if None == item_rating:
                        continue
                rating_pred += user_simi[userID_y] * item_rating - b_y_i
                deno += user_simi[userID_y]
            if deno != 0:
                rating_pred = rating_pred/deno + b_x_i
            else:
                rating_pred = -1
                print("没有相似用户对该item打过分，甚至连相似的item找上也不行")
            if userID_x not in prediction:
                prediction[userID_x] = dict()
            prediction[userID_x][itemID] = rating_pred
            true_rating = vali_dict[userID_x][itemID]
            string = "true: " + str(true_rating) + '\n' + "pred: " + str(rating_pred) + '\n'
            print(string)
    print("hhhhhhhh")
    return prediction


def predict_part_bias(train_dict, vali_dict):
    m = bias.global_rating_mean  # 用来计算bxi
    item_mean = bias.read_mean("item_bias.txt")  # item_bias[itemID]为该item的bias
    user_mean = bias.read_mean("user_bias.txt")  # user_bias[userID]为该user的bias
    item_attr_dict = readFile.get_item_attribute_dict()
    attr_item_dict = readFile.get_item_attribute_cluster_dict()
    print("attr")
    prediction = dict()
    for userID_x in vali_dict:
        for itemID in vali_dict[userID_x]:
            mean_x = user_mean[userID_x]
            mean_i = item_mean[itemID]
            b_x_i = mean_x + mean_i - m
            rating_pred = 0  # 预测的打分
            deno = 0  # 分母的部分
            user_simi = top_k_similar_user(train_dict, userID_x, 100)  # 和userID有最高的相似度的user
            for userID_y in user_simi:
                if itemID in train_dict[userID_y]:  # 如果userID_y对itemID打过分
                    item_rating = train_dict[userID_y][itemID]
                else:  # userID_y没有对itemID打过分，则用item_attribute把对应的打分估计出来
                    item_rating = item_rating_estimate(attr_item_dict, item_attr_dict, train_dict[userID_y], itemID)
                    if None == item_rating:
                        continue
                rating_pred += user_simi[userID_y] * item_rating
                deno += user_simi[userID_y]
            if deno != 0:
                rating_pred = rating_pred
            else:
                rating_pred = b_x_i
                print("没有相似用户对该item打过分，甚至连相似的item找上也不行")
            if userID_x not in prediction:
                prediction[userID_x] = dict()
            if rating_pred < 0:
                rating_pred = 0
            if rating_pred > 100:
                rating_pred = 100
            prediction[userID_x][itemID] = rating_pred
            true_rating = vali_dict[userID_x][itemID]
            string = "true: " + str(true_rating) + '\n' + "pred: " + str(rating_pred) + '\n'
            print(string)
    print("hhhhhhhh")
    return prediction


if __name__ == '__main__':
    ui = readFile.read_train()
    train, test = set_split(ui, 1e-4)
    prediction = predict_part_bias(train, test)
    file = open('pred.txt', 'w')
    for userID in test:
        for itemID in test[userID]:
            pred_rating = prediction[userID][itemID]
            true_rating = test[userID][itemID]
            string = str(true_rating) + ':' + str(pred_rating) + '\n'
            file.write(string)
