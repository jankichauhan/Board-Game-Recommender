import pandas as pd
import mysql.connector
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder


config = {
    'user': '',
    'password': '!',
    'host': '127.0.0.1',
    'database': 'recommender',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()


class ALS:
    MODEL_NAME = 'ALS'
    COUNT_LIMIT = 100

    def __init__(self):
        print("in init")
        self.spark = SparkSession.builder.config("spark.rpc.message.maxSize", 1024).getOrCreate()
        self.user_ratings = pd.read_csv('../data/bgg_user_ratings.csv', index_col=0)
        self.spark_df = self.spark.createDataFrame(self.user_ratings)

        self.train, self.test = self.spark_df.randomSplit([.8, .20], seed=42)

        self.factor_model = ALS(
            itemCol='name',
            userCol='user',
            ratingCol='rating',
            nonnegative=True,
            regParam=0.05,
            maxIter=15,
            rank=5)


    def transform(self):

        self.recommender = self.factor_model.fit(self.spark_df)

        train_tr = self.recommender.transform(self.train)
        test_tr = self.recommender.transform(self.test)

        evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="rating", metricName="rmse")

        rmse_train = evaluator.evaluate(train_tr)
        rmse_test = evaluator.evaluate(test_tr)
        print('Train RMSE', rmse_train)
        print('Test RMSE', rmse_test)


    def gridCV(self):
        param_grid = ParamGridBuilder() \
            .addGrid(self.factor_model.rank, [5, 10, 15, 20]) \
            .addGrid(self.factor_model.maxIter, [10, 15, 20, 30, 35]) \
            .addGrid(self.factor_model.regParam, [0.05, 0.1, 0.15, 0.2]) \
            .build()

        evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="rating", metricName="rmse")

        grid_model = TrainValidationSplit(
            estimator=self.factor_model,
            estimatorParamMaps=param_grid,
            evaluator=evaluator)

        model = grid_model.fit(self.train)
        best_model = model.bestModel
        print('rank', best_model.rank)
        print('max iter', best_model._java_obj.parent().getMaxIter())
        print('reg param', best_model._java_obj.parent().getRegParam())
