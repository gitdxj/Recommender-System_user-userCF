import readFile
from simiCal import pearson_similarity_numpy, consine_similarity, top_k_similar_user
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


def predict(train_dict, vali_dict):
    prediction = dict()
    for userID in vali_dict:
        for itemID in vali_dict[userID]:
            rating_pred = 0  # 预测的打分
            deno = 0
            user_simi = top_k_similar_user(train_dict, userID, 100, 0)  # 和userID有最高的相似度的user
            for each_userID in user_simi:
                if itemID in train_dict[each_userID]:
                    rating_pred += user_simi[each_userID]*train_dict[each_userID][itemID]
                    deno += user_simi[each_userID]
            if deno != 0:
                rating_pred = rating_pred/deno
            else:
                rating_pred = 0
                print("没有相似用户对该item打过分")
            if userID not in prediction:
                prediction[userID] = dict()
            prediction[userID][itemID] = rating_pred
            true_rating = vali_dict[userID][itemID]
            string = "true: " + str(true_rating) + '\n' + "pred: " + str(rating_pred) + '\n'
            print(string)
    print("hhhhhhhh")
    return prediction




if __name__ == '__main__':
    ui = readFile.read_train()
    train, test = set_split(ui, 1e-5)
    prediction = predict(train, test)
    for userID in test:
        for itemID in test[userID]:
            pred_rating = prediction[userID][itemID]
            true_rating = prediction[userID][itemID]
            string = "true: " + true_rating + '\n' + "pred: " + pred_rating + '\n'