import pandas as pd
import numpy as np
import mysql.connector
import unicodedata
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

def correlation():
    sql_query = "select id, bgg_rank, playing_time, max_player, min_player, age from board_game; "
    games_df = pd.read_sql_query(sql_query, cnx)
    games_df= games_df.set_index("id")
    games_df = games_df.astype(int)
    trans = games_df.T.corr(method='spearman')
    s = trans.unstack()
    dict = {}
    for id in games_df.index.values.tolist():
        dict[id] = list(s[id].sort_values(ascending=False).index)[1:]

    df = pd.DataFrame.from_dict(dict, orient="index")
    df.index.name = 'id'
    print(df)
    df.to_csv("../data/data.csv")

def recommend_items(id, topn=10):
    df = pd.read_csv("../data/data.csv", index_col='id')
    t = tuple(df.loc[int(id)].values[:topn])
    sql = "select name from board_game where id in {} ".format(t)
    games_df = pd.read_sql_query(sql, cnx)
    print(games_df)