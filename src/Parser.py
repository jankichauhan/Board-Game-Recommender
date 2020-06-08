import xml.etree.ElementTree as ET
import os

import mysql.connector
import unicodedata

config = {
    'user': '',
    'password': '!',
    'host': '127.0.0.1',
    'database': '',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
mycursor = cnx.cursor()


# Parser to extract information from the board game xml files

class Parser:
    def __init__(self):
        print("in init")
        self.id = ''
        self.name = ''
        self.yearpublished = ''
        self.minplayers = 0
        self.maxplayers = 0
        self.playingtime = 0
        self.ratings = 0
        self.usersrated = 0
        self.bayesratings = 0
        self.designer = list([])
        self.publisher = list([])
        self.category = list([])
        self.mechanics = list([])
        self.artists = list([])
        self.age = ''
        self.rank = ''
        self.counter = 0;
        self.abstracts = 0;
        self.childrensgames = 0;
        self.familygames = 0;
        self.partygames = 0;
        self.strategygames = 0;
        self.thematic = 0;
        self.videogames = 0;
        self.wargames = 0;

    def getelements(self, filename):
        """

        :param filename:
        """
        tree = ET.parse("../xmls/" + filename)
        root = tree.getroot()

        for child in root:
            self.id = child.get('objectid')
            self.yearpublished = child.find('yearpublished').text if child.find('yearpublished') is not None else 0
            self.minplayers = child.find('minplayers').text if child.find('minplayers') is not None else 0
            self.maxplayers = child.find('maxplayers').text if child.find('maxplayers') is not None else 0
            self.playingtime = child.find('playingtime').text if child.find('playingtime') is not None else 0
            self.age = child.find('age').text if child.find('age') is not None else ''
            self.ratings = child.find('statistics').find('ratings').find('average').text if child.find(
                'statistics') is not None else 0
            self.bayesratings = child.find('statistics').find('ratings').find('bayesaverage').text if child.find(
                'statistics') is not None else 0
            self.usersrated = child.find('statistics').find('ratings').find('usersrated').text if child.find(
                'statistics') is not None else ''
            ranks = child.find('statistics').find('ratings').find('ranks') if child.find(
                'statistics') is not None else ''
            for rank in ranks:
                if rank.get('name') == 'boardgame':
                    self.rank = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'abstracts':
                    self.abstracts = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'childrensgames':
                    self.childrensgames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'familygames':
                    self.familygames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'partygames':
                    self.partygames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'strategygames':
                    self.strategygames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'thematic':
                    self.thematic = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'videogames':
                    self.videogames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                elif rank.get('name') == 'wargames':
                    self.wargames = rank.get('value') if rank.get('value') != 'Not Ranked' else 0
                else:
                    print("Game type not tracked: ", rank.get('name'))
            for grandChild in child:
                if grandChild.tag == 'boardgamedesigner':
                    self.designer.append(self.remove_accents(grandChild.text))
                if grandChild.tag == 'boardgamecategory':
                    self.category.append(grandChild.text)
                if grandChild.tag == 'boardgamepublisher':
                    self.publisher.append(self.remove_accents(grandChild.text))
                if grandChild.tag == 'boardgamemechanic':
                    self.mechanics.append(grandChild.text)
                if grandChild.tag == 'boardgameartist':
                    self.artists.append(self.remove_accents(grandChild.text))
                if grandChild.tag == 'name':
                    if grandChild.get('primary') == 'true':
                        self.name = self.remove_accents(grandChild.text)
        self.print_values()
        self.insert_into_table()

    def print_values(self):
        print("id = " + str(self.id))
        print(self.name)
        print(self.yearpublished)
        print(self.minplayers)
        print(self.maxplayers)
        print(self.playingtime)
        print(self.ratings)
        print(self.designer)
        print(self.publisher)
        print(self.category)
        print(self.mechanics)
        print(self.age)
        print(self.rank)
        print(self.counter)

    def remove_accents(self, input_str):
        """

        :param input_str:
        :return:
        """
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode()

    def insert_into_table(self):
        """

        """

        designer = ''
        publisher = ''
        mechanic = ''
        category = ''
        artist = ''

        if self.id != '' and self.name != '':
            if self.designer:
                designer = ':'.join(self.designer[:3])
                print(designer)
            if self.publisher:
                publisher = ':'.join(self.publisher[:3])
                print(publisher)
            if self.mechanics:
                mechanic = ':'.join(self.mechanics[:3])
            if self.category:
                category = ':'.join(self.category[:3])
                print(category)
            if self.artists:
                artist = ':'.join(self.artists[:3])
                print(artist)
            if self.rank == '' or self.rank == 'Not Ranked':
                self.rank = 0

            sql_insert = "INSERT INTO board_game (id,name,year,bgg_rank,rating,bayes_rating,max_player,min_player,playing_time,age,users_rated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.id, self.name, self.yearpublished, self.rank, self.ratings, self.bayesratings, self.maxplayers,
                   self.minplayers, self.playingtime, self.age, self.usersrated)
            print(sql_insert, val)
            mycursor.execute(sql_insert, val)
            cnx.commit()

            sql_insert = "INSERT INTO board_game_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                self.id, self.rank, artist, publisher, designer, mechanic, category, self.abstracts,
                self.childrensgames,
                self.partygames, self.strategygames, self.thematic, self.videogames, self.wargames)
            print(sql_insert, val)
            mycursor.execute(sql_insert, val)
            cnx.commit()

            print("1 record inserted, ID:", mycursor.lastrowid)
        else:
            print("Game is missing name")


if __name__ == '__main__':

    files = os.listdir('../xmls/')
    counter = 0

    # Clear all table content before inserting
    sql_delete = "delete from board_game where id > 0"
    mycursor.execute(sql_delete)
    sql_delete = "delete from board_game_detail where id > 0"
    mycursor.execute(sql_delete)
    cnx.commit()
    for file in files:
        print(file)
        counter += 1
        Parser().getelements(file)
    print(counter)
