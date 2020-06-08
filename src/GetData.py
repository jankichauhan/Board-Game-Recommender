import traceback
import time
import urllib3
import xmltodict
from random import seed

seed(1)
import pandas as pd


# Get board game geek's data for each game using game id.

class GetData:
    def get_data_by_id(id):
        """

        :return:
        """
        url = "https://www.boardgamegeek.com/xmlapi/boardgame/" + id + "?stats=1"
        http = urllib3.PoolManager()

        response = http.request('GET', url)
        try:
            data = xmltodict.parse(response.data)
            with open('../xmls/game' + id + '.xml', 'wb') as file:
                file.write(response.data)
        except:
            print("Failed to parse xml from response (%s)" % traceback.format_exc())
        return data


if __name__ == '__main__':

    colnames = ['Rank', 'Name', 'Id']
    data = pd.read_csv('../data/bgglist.csv', names=colnames)
    gameids = data.Id.tolist()
    for id in gameids[:1000]:
        print(id)
        GetData.get_data_by_id(str(id))
        time.sleep(0.3)
