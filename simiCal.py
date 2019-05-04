import numpy as np
from math import sqrt
import readFile
import datetime


def pearson_similarity(user_a, user_b):
    '''
    user_a和user_b都是字典类型，字典的key为itemID，value为该uer对该item的打分
    两个user的相似度用pearson相关系数来表示
    '''
    # 首先寻找两个user都打了分的item
    common_item = list()
    for item in user_a.keys():
        if item in user_b:
            common_item.append(item)
    # 计算a,b两个用户的平均打分
    average_a_rating = 0
    for each_rating in user_a.values():
        average_a_rating += each_rating
    average_a_rating = average_a_rating/len(user_a.values())
    average_b_rating = 0
    for each_rating in user_b.values():
        average_b_rating += each_rating
    average_b_rating = average_b_rating/len(user_b.values())
    # 计算两个用户的pearson相关系数
    pearson_simi = 0
    for each_item in common_item:
        r_a = user_a[each_item]
        r_b = user_b[each_item]
        diff_a = r_a - average_a_rating
        diff_b = r_b - average_b_rating
        pearson_simi += diff_a * diff_b
    deno_a = 0
    deno_b = 0
    for rating in user_a.values():
        deno_a += (rating - average_a_rating)*(rating - average_a_rating)
    for rating in user_b.values():
        deno_b += (rating - average_b_rating)*(rating - average_b_rating)
    deno_a = sqrt(deno_a)
    deno_b = sqrt(deno_b)
    deno = deno_a*deno_b
    if 0 == deno and 0 == pearson_simi:
        pearson_simi = 0
    else:
        pearson_simi = pearson_simi/deno
    return pearson_simi


def pearson_similarity_numpy(user_a, user_b):
    '''
    使用numpy来计算pearson相关系数
    和普通版本相比或快或慢，主要看稀疏程度
    '''
    # 首先寻找两个user都打了分的item
    common_item = list()
    for item in user_a.keys():
        if item in user_b:
            common_item.append(item)
    r_a_vector = [value for value in user_a.values()]
    r_b_vector = [value for value in user_b.values()]
    r_a_c_vector = [user_a[item] for item in common_item]
    r_b_c_vector = [user_b[item] for item in common_item]
    r_a_vector = np.array(r_a_vector)  # 用户a的打分向量
    r_b_vector = np.array(r_b_vector)  # 用户b的打分向量
    r_a_c_vector = np.array(r_a_c_vector)  # 用户a对a，b共有项的打分向量
    r_b_c_vector = np.array(r_b_c_vector)  # 用户b对a，b共有项的打分向量
    r_a_mean = np.mean(r_a_vector)
    r_b_mean = np.mean(r_b_vector)
    r_a_mean_vector = np.array([r_a_mean for _ in range(len(r_a_vector))])
    r_b_mean_vector = np.array([r_b_mean for _ in range(len(r_b_vector))])
    r_a_vector = np.subtract(r_a_vector, r_a_mean_vector)
    r_b_vector = np.subtract(r_b_vector, r_b_mean_vector)
    r_a_c_mean_vector = np.array([r_a_mean for _ in range(len(r_a_c_vector))])
    r_b_c_mean_vector = np.array([r_b_mean for _ in range(len(r_b_c_vector))])
    r_a_c_vector = np.subtract(r_a_c_vector, r_a_c_mean_vector)
    r_b_c_vector = np. subtract(r_b_c_vector, r_b_c_mean_vector)
    deno = np.linalg.norm(r_a_vector)*np.linalg.norm(r_b_vector)
    nume = np.matmul(r_b_c_vector, r_a_c_vector.T)
    if deno == 0:
        pearson_simi = 0
    else:
        pearson_simi = nume/deno
    return pearson_simi


def consine_similarity(list_a, list_b):
    # 计算余弦相似度
    if list_a == None or list_b == None:
        print("list 为空")
        return 0
    vector_a = np.array(list_a)
    vector_b = np.array(list_b)
    num = np.matmul(vector_a, vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    if 0 == denom:
        cos = 0
    else:
        cos = num / denom
    return cos


def user_similarity(user_item_rating, userID):
    '''
    对于一个特定的user，计算其与其他所有user的相似度
    然后按照相似度进行排序
    '''
    user_simi = {}
    user = user_item_rating[userID]
    for each_userID in user_item_rating:
        user_i = user_item_rating[each_userID]
        simi = pearson_similarity_numpy(user, user_i)
        user_simi[each_userID] = simi
    user_simi = sorted(user_simi.items(), key = lambda user_simi:user_simi[1], reverse=True)
    return user_simi


def compare():
    a = {1:4, 4:5, 5:1}
    b = {1:5, 2:5, 3:4}
    c = {4:2, 5:4, 6:5}
    print(pearson_similarity(a,b))
    print(pearson_similarity(a,c))
    print(pearson_similarity_numpy(a, b))
    print(pearson_similarity_numpy(a, c))

def write_simi():
    '''
    本来打算将计算好的相似度直接写入文件中
    再次使用时可以直接读取
    但是写出来的文件太大了
    '''
    user_item_rating = readFile.read_train("train.txt")
    file = open("similarity.txt", 'a')
    users = [user for user in user_item_rating.keys()]
    n_users = len(users)
    # 用户i和用户j的相似度
    for i in range(n_users):
        print("计算到" + str(i))
        user_simi = {}
        user_i = user_item_rating[users[i]]
        for j in range(i+1, n_users):
            user_j = user_item_rating[users[j]]
            simi = pearson_similarity_numpy(user_i, user_j)
            index = (users[i], users[j])
            user_simi[index] = simi
        for each_index in user_simi:
            line = str(each_index[0]) + ':' + str(each_index[1]) + ':' + str(round(user_simi[each_index],4)) + '\n'
            file.write(line)
        print("写入完成")
    print("全部完成")


def top_k_similar_user(user_item_rating, userID, K=40, threshold=0.1):
    '''
    给定一个user，计算出其和其他所有用户的相似度
    按照相似度排序，选取前K个并且相似度大于threshold值的用户
    返回一个字典，key为userID，value为相似度
    '''
    user_simi = user_similarity(user_item_rating, userID)
    simi_dict = dict()
    for i in range(K):
        each_tuple = user_simi[i]
        userID = each_tuple[0]
        simi = each_tuple[1]
        if simi > threshold:
            simi_dict[userID] = simi
        else:
            break
    return simi_dict

def item_rating_estimate(attribute_dict, user, itemID_x, K=10):
    '''
    根据某一用户对其他item的打分估计其对某一未打分item的打分
    item之间的相似度用attribute来表示
    user是一个字典，key为itemID，value为rating
    '''
    item_simi = dict()
    if itemID_x not in attribute_dict:
        print("itemAttribute里面没有" + str(itemID_x))
        return None
    attr_x = attribute_dict[itemID_x]
    for itemID_y in user:
        if itemID_y not in attribute_dict:
            print("itemAttribute里面没有" + str(itemID_y))
            continue
        attr_y = attribute_dict[itemID_y]
        simi = consine_similarity(attr_x, attr_y)
        item_simi[itemID_y] = simi
    item_simi = sorted(item_simi.items(), key=lambda item_simi: item_simi[1], reverse=True)
    est_rating = 0
    deno = 0
    if K > len(item_simi):
        K = len(item_simi)
    for i in range(K):
        itemID = item_simi[i][0]
        simi = item_simi[i][1]
        est_rating += user[itemID]*simi
        deno += simi
    est_rating = est_rating/deno
    return est_rating


if __name__ == '__main__':
    simi_dict = top_k_similar_user(301, 40, 0.1)
    for each in simi_dict:
        string = str(each) + ':' + str(simi_dict[each])
        print(string)


