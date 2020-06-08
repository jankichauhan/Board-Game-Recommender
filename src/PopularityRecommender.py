import mysql.connector
import pandas as pd
import csv
import os.path

config = {
    'user': '',
    'password': '!',
    'host': '127.0.0.1',
    'database': 'recommender',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()

# Popular games based on the given category

class PopularityRecommender:
    MODEL_NAME = 'Popularity'

    def __init__(self):
        print('in init')

    def get_model_name(self):
        return self.MODEL_NAME

    def recommend_items(self, popularity_type, topn=10):
        """

        :param popularity_type:
        :param topn:
        :return:
        """
        if os.path.isfile('../data/' + popularity_type + '.csv') == False:
            sql_query = "select name, rating from board_game where id in (select * from (select id from board_game_detail where " + popularity_type + " > 0 order by " + popularity_type + " Limit 100 ) as t1) order by users_rated DESC LIMIT "+ str(
                topn) + " " + " ;"
            recommendation_df = pd.read_sql_query(sql_query, cnx)
            recommendation_df.index.name = 'id'
            recommendation_df.to_csv('../data/' + popularity_type + '.csv')
        else:
            recommendation_df = pd.read_csv('../data/' + popularity_type + '.csv', index_col='id')

        return recommendation_df
