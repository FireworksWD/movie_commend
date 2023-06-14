import shutil

from pyspark.sql import SparkSession,Row
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
import os

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext
    rdd1 = sc.textFile('hdfs://mycluster/movie/hits.txt')
    # userid,movieid,nums
    ratingsRDD = rdd1.map(lambda x: x.split('\t'))
    user_row = ratingsRDD.map(lambda x: Row(userid=int(x[0]), movieid=int(x[1]), hitnum=int(x[2])))
    # 将RDD转换为df
    user_df = spark.createDataFrame(user_row)
    # user_df.show()
    user_df.createTempView('test')
    datatable = spark.sql("""select userid,movieid,sum(hitnum) hitnum from test group by userid,movieid""")

    movierdd = datatable.rdd.map(lambda x: (x.userid, x.movieid, x.hitnum))
    # 训练模型
    model = ALS.train(movierdd, 10, 10, 0.01)
    # print(model.recommendProducts(1,3))

    # 保存模型
    if os.path.exists('/root/movie/movie_model'):
        shutil.rmtree('/root/movie/movie_model')
    model.save(sc, 'file:///root/movie/movie_model')
