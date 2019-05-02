import json


def read_train(filename):
    '''
    读取训练数据train.txt
    将train.txt中的数据结构化为一个以userID为index的dictionary
    userID对应的value又为一个以itemID为index的dictionary
    itemID对应的value为该用户对此item的打分
    最后将此结构化的数据保存到formatted_train.txt文件中
    '''
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    lines = file.readlines()
    UserID = 0
    user_item_rating = {}
    for each_line in lines:
        each_line = each_line.strip()  # 去除左右空格
        par_position = each_line.find('|')  # 查找每一行中是否有'|'这一字符，有的话par_position为其下标，没有则为-1
        if -1 == par_position:
            # 若这一行没有'|'则说明这一行是itemID和对应的评分
            item_rating_mapping = each_line.split('  ')
            item_id = int(item_rating_mapping[0])
            item_rating = int(item_rating_mapping[1])
            user_item_rating[userID][item_id] = item_rating
        else:
            # 若这一行中有'|'则说明这一行的格式是这样的：userID|item数量
            userID = int(each_line[0:par_position])
            print("现在userID为： "+str(userID))
            print(each_line)
            rated_item_number = int(each_line[par_position+1:len(each_line)])
            if userID not in user_item_rating:
                user_item_rating[userID] = {}
    file.close()
    print("训练集读取成功")
    return user_item_rating


def read_json_dict(filename):
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    dictionary = json.loads(file.read())
    print(filename + "读取成功")
    return dictionary


def get_train_item_list(user_item_rating):
    '''
    从user对item打分的字典中获得itemID的列表，返回
    :param user_item_rating: user对item的打分字典
    :return: 排序好的itemID列表
    '''
    item_list = []
    for each_user in user_item_rating.values():
        for each_item in each_user.keys():
            if each_item not in item_list:
                item_list.append(int(each_item))
    item_list.sort()
    return item_list


def get_train_user_list(user_item_rating):
    train_uesr_list = []
    for each_user in user_item_rating.keys():
        if each_user not in train_uesr_list:
            train_uesr_list.append(each_user)
    train_uesr_list.sort()
    return train_uesr_list


def read_train_item_list_from_txt(filename):
    '''
    从文件中读取itemID并排序，返回排序好的list，itemID的类型为integer
    :param filename: 文件名
    :return: 返回排序好的item列表
    '''
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    item_list = []
    items = file.readlines()
    for each_item in items:
        each_item = each_item.strip('\n')
        item_list.append(int(each_item))
    item_list.sort()
    return item_list


def read_test(filename):
    '''
    读取测试集的数据
    将其中的数据结构化为一个词典，key为userID，value为itemID组成的列表
    :param filename: 测试集文件（这里取“test.txt”即可）
    最后将此结构化的文件保存到formatted_test.txt当中
    '''
    try:
        file = open(filename, 'r')
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    lines = file.readlines()
    UserID = 0
    test_user_item_mapping = {}
    for each_line in lines:
        each_line = each_line.strip()  # 去除左右空格
        par_position = each_line.find('|')  # 查找每一行中是否有'|'这一字符，有的话par_position为其下标，没有则为-1
        if -1 == par_position:
            # 若这一行没有'|'则说明这一行是itemID
            item_id = int(int(each_line))
            test_user_item_mapping[userID].append(item_id)
        else:
            # 若这一行中有'|'则说明这一行的格式是这样的：userID|item数量
            userID = int(each_line[0:par_position])
            print("现在userID为： "+str(userID))
            print(each_line)
            if userID not in test_user_item_mapping:
                test_user_item_mapping[userID] = []
    file.close()
    print("测试集读取成功")
    return test_user_item_mapping


def get_test_item_list(test_user_item_mapping):
    test_item_list = []
    for each_item_list in test_user_item_mapping.values():
        for each_item in each_item_list:
            if each_item not in test_item_list:
                test_item_list.append(each_item)
    test_item_list.sort()
    return test_item_list


def get_test_user_list(test_user_item_mapping):
    test_user_list = []
    for each_user in test_user_item_mapping.keys():
        if each_user not in test_user_list:
            test_user_list.append(each_user)
    test_user_list.sort()
    return test_user_list


def get_item_attribute_dict():
    file = open("itemAttribute.txt", 'r')
    lines = file.readlines()
    item_attribute = dict()
    for line in lines:
        line = line.strip()
        flag_1 = line.find('|')
        flag_2 = line.find('|', flag_1 + 1)
        itemID = line[0:flag_1]
        attribute1 = line[flag_1+1: flag_2]
        attribute2 = line[flag_2+1: len(line)]
        if attribute1.isdigit() and attribute2.isdigit():
            item_attribute[int(itemID)] = (int(attribute1), int(attribute2))
        else:
            item_attribute[int(itemID)] = None
    return item_attribute


def train_test_user_comparison():
    train = read_train("train.txt")
    test = read_test("test.txt")
    train_user_list = get_train_user_list(train)
    test_user_list = get_test_user_list(test)
    train_file = open("train_user.txt", 'w+')
    test_file = open("test_user.txt", 'w+')
    for user in train_user_list:
        train_file.write(str(user) + '\n')
    for user in test_user_list:
        test_file.write(str(user) + '\n')
    train_file.close()
    test_file.close()
    new_user_list = []
    for user in test_user_list:
        if user not in train_user_list:
            if user not in new_user_list:
                new_user_list.append(user)
    if new_user_list:
        file = open("new_user.txt", 'w+')
        for user in new_user_list:
            file.write(str(user) + '\n')
        file.close()


if __name__ == '__main__':
    item_attribute = get_item_attribute_dict()
    for i in range(20):
        print(item_attribute[i])





'''
随手笔记：
测试集和训练集中的user是完全相同的
itemAttribute.txt中包含所有的item而测试集和训练集中只有一部分
'''