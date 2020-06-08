import pandas as pd
import numpy as np
from src.PopularityRecommender import PopularityRecommender
from src.Content import Content
from src.Collabrative import Collabrative
import os.path
from os import path


# One access point to all models

def get_popular(type):
    """

    :param type:
    :return:
    """
    print("in get popular")

    popular = PopularityRecommender()
    result = popular.recommend_items(type)
    print(result)
    return result


def get_collabrative(games):
    """

    :param games:
    :return:
    """
    print("in get collabrative")
    coll_model = Collabrative()
    content = Content()
    result = pd.DataFrame()
    for game in games:
        print("Collab Recommendation for game ", game)
        df = coll_model.get_recommendations(game)
        if not df.empty:
            df = df[df.name != game]
            result = result.append(df)
    if result.empty:
        for game in games:
            print("Content Recommendation for game ", game)
            df = content.get_recommendations(game)
            result = result.append(df)

        return result.head(10)
    else:
        result = result.drop_duplicates().round({"mean": 2, "model_score": 2})
        return result.sort_values('model_score', ascending=False).head(10)
