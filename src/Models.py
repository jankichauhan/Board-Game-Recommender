import pandas as pd
import numpy as np
from src.PopularityRecommender import PopularityRecommender
import src.Correlation as corr
from src.Collabrative import Collabrative
import os.path
from os import path

def get_popular(type):
    popular = PopularityRecommender(type)
    print(popular.recommend_items().loc[:,'name'])

def get_correlated(game_id):
    if os.path.isfile('../data/data.csv'):
        print(corr.recommend_items(game_id))
    else:
        corr.correlation()
        print(corr.recommend_items(game_id))

# get_correlated('174430')

def get_collabrative():
    coll_model = Collabrative()
    coll_model.transform()

get_collabrative()