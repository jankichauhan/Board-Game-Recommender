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

## Data Exploration

### Data Pipeline

 ![](images/Data Pipeline.png)
 
Data Source: [BGG API](https://boardgamegeek.com/wiki/page/BGG_XML_API)

### Analysis

Each board game has the following fields:  
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

Each user rating has the following field.  
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
 
 ### Popular recommender
 
 ### Content based recommender
 
 ### Collaborative recommender
 
 ## Conclusion
 
 ## Future Analysis

