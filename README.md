# F1 P10 Game

## Why?
Small fun project for logging tips when watching F1.  
Point is to guess who will finish at tenth position and who will DNF first.  
For each correct tip the points are awarded to the player and counted up.

## How?
Points are awarded from 25 points for 10th place going down to 18 points for  
9th and 11th place and going down all the way to 1 for 1st and 19th.  
For sprint points are lowered and starting at 8 points for 10th place.  
Correctly guessing first DNF will grand 20 points.

## What this is
This is a great way to have more fun while watching Formula 1,  
to guess who will finish not in a first place, but rather in a middle of a field.
It's a project I put together to log online rather than writing  
all predictions down with pen and a paper. 

## What is this not
This is a Python App that uses NiceGUI framework, which means it is  
not suitable for use for many users at the same time, the navigation in  
the app is visiable to all open instances.  
..Which is not a problem with few friends or in a family. 

## Data
Depends on data from my F1-Scrapper: 
```text
https://github.com/kamildemocko/F1Scrap.git
```
Either run manually and copy output to the program's input  
or set up scrapper to run on schedule and set correct paths in the config file.

## Installation and running
### Scrapper
```commandline
git clone https://github.com/kamildemocko/F1Scrap.git
cd F1Scrap
poetry install
poetry run playwright install chromium
poetry run f1_scrap/main.py
```

### Game

```commandline
git clone https://github.com/kamildemocko/F1P10Game.git
cd F1P10Game
poetry install
```

Set up config.ini paths to point to the scrapper json files and initial players
```text
[root]
title = Formula 1 P-10 Game
initial_players = Pete, Rachel
login_timeout_sec = 300

[paths]
drivers_path = /home/ubuntu/F1Scrap/f1_scrap/output/drivers.json
circuits_path = /home/ubuntu/F1Scrap/f1_scrap/output/circuits.json
players_path = data/players.json
results_path = /home/ubuntu/F1Scrap/f1_scrap/output/results.json
points_path = data/points_tables.json
```

Run with:
```commandline
cd f1p10game
poetry run main.py
```

set up your password in .env file in folder f1p10game, the login
```text
password=secret
```

## Screenshots

Pc

![image](https://github.com/kamildemocko/F1P10Game/assets/50048116/21f26d9b-91db-4431-aedf-d061c0cf2c17)

![image](https://github.com/kamildemocko/F1P10Game/assets/50048116/c69f8c81-7070-428c-b68f-92bc6223156b)

Phone

![image](https://github.com/kamildemocko/F1P10Game/assets/50048116/b1424b37-90d2-4de4-81ce-289f91a48fc3)
