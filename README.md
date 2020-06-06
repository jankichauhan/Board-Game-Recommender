# Board Game Recommender
<br>Janki Chauhan
<br>
[Linkedin](https://www.linkedin.com/in/jankichauhan/) | [Github](https://github.com/jankichauhan) | [Board Game Geek](https://boardgamegeek.com/user/jankichauhan)

## Contents

* [Motivation](#motivation)
* [Data Exploration](#data-exploration)
  * [Data Pipeline](#pipeline-source)
  * [Analysis](#analysis)
* [Recommenders](#recommender)
  * [Popular recommender](#popular)
  * [Content base filtering](#content)
  * [Collaborative filtering](#collabrative)
* [Conclusion](#conclusion)
* [Future Analysis](#future-analysis)

## Motivation
I got introduced to board games in Dec 2010, no one had plans for the holidays and we all had enough of movie watching. We played Ticket to Ride and then Settler of Catan a few days later; it was so much fun, I loved it. Since then it has been board games over movies(for me!) When you have been playing board games for 10 years, you start developing your favorites. I am biased towards Euro games(specially worker placement games), any game by Jamey Stegmaier or Uwe Rosenberg I am willing to give a try. On the other hand card games are not in my top 10. Dominion is one of the best gateway games but it didn't appeal to me. For finding the next game to play, I rely on amazing people at [Dice Tower](www.dicetower.com)(this a youtube channel for board games reviews, play throughs ... etc). 

Can we train a machine to learn patterns among users and the games they like? We can use this trained machine to recommend the next game the user should play. 

## Data Exploration

### Data Pipeline

![](images/Data%20Pipeline.png)
 
Data Source: [BGG API](https://boardgamegeek.com/wiki/page/BGG_XML_API)

### Analysis

Each board game has the following fields: ~70K games
  > -`board game id` 
  > -`name` 
  > -`year published` 
  > -`min player` 
  > -`max player`
  > -`playing time`
  > -`rating`
  > -`designers`
  > -`categories`
  > -`game mechanic`
  > -`publishers`
  > -`user rating count`
  > -`age`
  > -`bgg rank`
  > -`category rank`

Each user rating has the following fields: ~2M ratings  
  > -`user id` 
  > -`bgg user handle` 
  > -`board game id` 
  > -`board game name` 
  > -`rating`
  > -`review`


#### Number of board games published in last 20 years
 
 ![](images/ratings.png)
 
 #### Ratings distribution over number of reviews
 
 ![](images/ratings_histogram.png)
 
 #### Most common words used in highly rated games and poorly rated games
 
 <img src="images/postive_reviews.png" width="400"> <img src="images/negative_reviews.png" width="400">
 
 
 ## Recommenders
 
 ### Popularity recommender
 
 Popularity criteria = rank(overall/per category) + total number of users that rated the game
 Popularity recommender will recommend the games based popularity criteria
 User can choose to pick one of the following categories and the recommender will return popular games based of that category:
 > - Abstract Game
 > - Children's Game
 > - Family Game
 > - Party Game
 > - Strategy Game
 > - Thematic Game
 > - War Game
 
 ### Content based recommender
 
 Determine similar games based on the rank, category, playtime, max and min player and age. Recommend similar games based on the user's input.
 
 ![](images/content.png)
 
 > - Method(s):
 >> - Correlation matrix using pearson similarity
 
 
 
 ### Collaborative recommender
 
 Determine similar users based on their profiles and recommend games that other users liked. 
 
 ![](images/collab.png)
 
 > - Method(s):
 >> - ALS: RMSE - 2.3
 >> - Fast AI + KNN: RMSE - 1.2
 
 ![](images/knn.png)
Seeing the games in a two deminsional plot. 

 ## Conclusion
 
 ## Future Analysis

