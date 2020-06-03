import mysql.connector
import pandas as pd
import csv

config = {
    'user': '',
    'password': '!',
    'host': '127.0.0.1',
    'database': '',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()


class PopularityRecommender:
    MODEL_NAME = 'Popularity'

    def __init__(self, popularity_type):
        self.popularity_type = popularity_type


    def get_model_name(self):
        return self.MODEL_NAME

    def recommend_items(self, topn=10):
        sql_query = "select name, year, rating, max_player, min_player, playing_time, age from board_game where id in (select * from (select id from board_game_detail where " + self.popularity_type + " > 0 order by " + self.popularity_type + " Limit " + str(topn) + " ) as t1) order by users_rated DESC;"
        recommendations_df = pd.read_sql_query(sql_query, cnx)

        return recommendations_df
