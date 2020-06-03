import pandas as pd
import pickle
import numpy as np
from fastai.collab import *
from pprint import pprint
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.neighbors import NearestNeighbors

class Collabrative:
    MODEL_NAME = 'Collabrative'

    def __init__(self):
        print("in init")
        self.user_ratings = pd.read_csv('../data/bgg_user_ratings.csv', index_col=0)

    def transform(self):
        print(" in transform")
        games_by_users = self.user_ratings.groupby('name')['rating'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        games_by_users['rank'] = games_by_users.reset_index().index + 1
        print(len(games_by_users))

        data_user_rating = CollabDataBunch.from_df(self.user_ratings, user_name='user', item_name='name', rating_name='rating', bs=100000,
                                       seed=42)
        data_user_rating.show_batch()

        learner = collab_learner(data_user_rating, n_factors=50, y_range=(2., 10))
        learner.fit_one_cycle(3, 1e-2, wd=0.15)
        print(learner.model)

        top_games = games_by_users[games_by_users['count'] > 5000].sort_values('mean', ascending=False).index
        print(len(top_games))
        mean_ratings = self.user_ratings.groupby('name')['rating'].mean().round(2)
        game_bias = learner.bias(top_games, is_item=True)
        game_bias.shapemean_ratings = self.user_ratings.groupby('name')['rating'].mean()
        game_ratings = [(b, i, mean_ratings.loc[i]) for i, b in zip(top_games, game_bias)]
        item0 = lambda o: o[0]

        print(sorted(game_ratings, key=item0)[:10])

        print(sorted(game_ratings, key=lambda o: o[0], reverse=True)[:15])
