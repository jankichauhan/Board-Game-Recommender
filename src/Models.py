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

def get_collabrative(games):
    print("in get collabrative")
    coll_model = Collabrative()
    result = pd.DataFrame()
    for game in games:
        print("Recommendation for game ", game)
        df = coll_model.get_recommendations(game)
        print(df)
        if not df.empty:
            df = df[df.name != game]
            result = result.append(df)
    if result.empty:
        # implement content based recommendation
        # if content based returns empty, return popular
        return result
    else:
        result = result.drop_duplicates().round({"mean":2, "model_score":2})
        print(result)
        return result.sort_values('model_score', ascending=False).head(10)

get_collabrative(['Camel Up (Second Edition)', 'Carcassonne'])