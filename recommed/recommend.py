from pprint import pprint

from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
import redis

pool = redis.ConnectionPool(host='192.168.188.20', port=6379)
redis_client = redis.Redis(connection_pool=pool)


def getRecommendByUserID(uid, cnt):
    sc = SparkContext(master='local[*]')
    try:
        movie_model = MatrixFactorizationModel.load(sc, 'file:///root/movie/movie_model')
        result = movie_model.recommendProducts(uid, cnt)
        temp = ''
        for r in result:
            # pprint(f'user:{r.user},movie_info:{movie_data[r.product]}')
            temp += str(r.product) + ','
        # print(temp)
        redis_client.set(uid, temp)
        print('successfully!!!')
    except Exception as e:
        print(' error' + str(e))
    sc.stop()


