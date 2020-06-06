# Get Data:
GetData.py - will save xml per each game

Parser.py - will parse and save data into sql tables

# SQL tables meta data:
## Board game table: 
CREATE TABLE `board_game` (
  `id` int NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `year` varchar(45) DEFAULT NULL,
  `bgg_rank` varchar(45) DEFAULT NULL,
  `rating` varchar(45) DEFAULT NULL,
  `bayes_rating` varchar(45) DEFAULT NULL,
  `max_player` int DEFAULT NULL,
  `min_player` int DEFAULT NULL,
  `playing_time` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `users_rated` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
## Board game details table:
CREATE TABLE `board_game_detail` (
  `id` int NOT NULL,
  `bgg_rank` int DEFAULT NULL,
  `artist` varchar(300) DEFAULT NULL,
  `publisher` varchar(300) DEFAULT NULL,
  `desinger` varchar(300) DEFAULT NULL,
  `meachanics` varchar(300) DEFAULT NULL,
  `category` varchar(300) DEFAULT NULL,
  `abstract` int DEFAULT NULL,
  `childersgames` int DEFAULT NULL,
  `partygames` int DEFAULT NULL,
  `strategygames` int DEFAULT NULL,
  `thematic` int DEFAULT NULL,
  `videogames` int DEFAULT NULL,
  `wargames` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
## User ratings table:
CREATE TABLE `user_ratings` (
  `user_id` int DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `ratings` varchar(45) DEFAULT NULL,
  `review` blob,
  `game_id` int DEFAULT NULL,
  `gamename` varchar(200) DEFAULT NULL,
  `row_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`row_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# Run flask app:
python RecommenderApp.py

On your browser open localhost:8080

