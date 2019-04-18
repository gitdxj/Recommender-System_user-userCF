def readfile(filename):
    '''
    将train.txt中的数据结构化为一个以userID为index的词典
    userID对应的数据又为一个词典
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
    formated_file = open('formated.txt', 'w+')
    formated_file.write(str(user_item_rating))

if __name__ == '__main__':
    readfile("train.txt")

