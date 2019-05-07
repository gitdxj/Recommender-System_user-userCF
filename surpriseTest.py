from surprise import *
from surprise.model_selection import cross_validate
from surprise import Dataset
from surprise import Reader
import os

if __name__ == '__main__':
    file_path = os.path.expanduser("C://Users/Frank Lee/PycharmProjects/recommenderSystem/surprise_train.txt")
    reader = Reader(line_format='user item rating', sep=' ', rating_scale=(0,100))
    data = Dataset.load_from_file(file_path, reader=reader)
    algo = KNNWithZScore()
    cross_validate(algo, data, measures=['RMSE'], cv=5, verbose=True)