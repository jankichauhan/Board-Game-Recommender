import requests
from bs4 import BeautifulSoup
import pandas as pd

rank = []
name = []
bggId = []

bgg_rank_page = 'https://boardgamegeek.com/browse/boardgame/page/'

for i in range(1, 701):
    current_page = bgg_rank_page + str(i)

    page = requests.get(current_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='collection')
    games = results.find_all(id='row_')

    for game in games:
            gameRank = game.find('td').text.strip()
            gameName = game.find(class_='collection_objectname').find('a').text.strip()
            gameId = game.find(class_='collection_objectname').find('a')['href'].split('/')[2]
            rank.append(gameRank)
            name.append(gameName)
            bggId.append(gameId)

print(rank[0])
print(name[0])
print(bggId[0])

f = pd.DataFrame({'Rank':rank, 'Name': name,  'Id': bggId})
f.to_csv('../data/bgglist.csv', mode='a', header=False, index=False, encoding='utf-8')
