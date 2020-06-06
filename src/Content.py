import pandas as pd
import numpy as np
import mysql.connector
import unicodedata
import csv
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

config = {
    'user': '',
    'password': '',
    'host': '127.0.0.1',
    'database': 'recommender',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()


class Content:
    MODEL_NAME = 'Content'

    def __init__(self):
        print("in init")

    def correlation(self):
        print("in correlation")

        sql_query = "select g.id, g.name, d.desinger, d.category, d.meachanics from board_game g join board_game_detail d on g.id = d.id where g.users_rated > 50"
        games_df = pd.read_sql_query(sql_query, cnx)
        games_df = games_df.set_index("id")
        print(games_df.shape)
        games_df.to_csv("../data/content_games.csv")
        features = ['desinger', 'category', 'meachanics']
        for feature in features:
            games_df[feature] = games_df[feature].apply(literal_eval)
            games_df[feature] = games_df[feature].apply(self.get_list())
            games_df[feature] = games_df[feature].apply(self.clean_data())



        games_df = games_df.assign(join=games_df.desinger.astype(str) + ', ' + games_df.category.astype(
            str) + ', ' + games_df.meachanics.astype(str))

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(games_df['join'])

        cosine_sim = cosine_similarity(count_matrix, count_matrix)

        pd.DataFrame(cosine_sim).to_csv("../data/cosine_sim.csv")

        games_df = games_df.reset_index()
        self.indices = pd.Series(games_df.index, index=games_df['name'])
        self.indices.to_pickle('../data/indices')

    def get_list(self, x):
        if isinstance(x, list):
            names = [i['name'] for i in x]
            if len(names) > 3:
                names = names[:3]
            return names

        return []

    def clean_data(self, x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''


    def get_recommendations(self, title):
        games = pd.read_csv("../data/content_games.csv", index_col='id')
        indices = pd.read_pickle("../data/indices")
        print(indices)
        cosine_sim = pd.read_csv("../data/cosine_sim.csv").values
        idx = indices[title]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        game_indices = [i[0] for i in sim_scores]

        return games['name'].iloc[game_indices]
