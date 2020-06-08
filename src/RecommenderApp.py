from collections import Counter
import src.Models as model
from flask import Flask, Response, render_template, request
import json
from wtforms import TextField, Form, SubmitField
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("../data/games.csv", index_col='id')
games = df['name'].values.tolist()


class SearchForm(Form):
    autocomp = TextField('Game name', id='game_autocomplete')

#auto complete feature for games
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    """

    :return:
    """
    return Response(json.dumps(games), mimetype='application/json')

#result page
@app.route('/result', methods=['GET', 'POST'])
def result():
    """

    :return:
    """
    form = SearchForm(request.form)
    if request.method == 'POST':
        recommended_game = model.get_popular(str(request.form['category']))
        return render_template('result.html', data=zip(recommended_game['name'].values.tolist(),
                                                       recommended_game['rating'].values.tolist()), form=form)

    return render_template("search.html", form=form)

#home page
@app.route('/', methods=['GET', 'POST'])
def recommend():
    """

    :return:
    """
    form = SearchForm(request.form)
    if request.method == 'POST':
        first_game = str(request.form['input1'])
        second_game = str(request.form['input2'])
        third_game = str(request.form['input3'])
        games = [first_game, second_game, third_game]
        recommended_game = model.get_collabrative(games)
        if not recommended_game.empty:
            return render_template('result.html', data=zip(recommended_game['name'].values.tolist(),
                                                           recommended_game['mean'].values.tolist()), form=form)
    return render_template("search.html", form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
