import os
import numpy as np
import sys
import scipy
import csv

teams_to_index = ["Arsenal",
"Bournemouth",
"Brighton",
"Burnley",
"Chelsea",
"Crystal Palace",
"Everton",
"Huddersfield",
"Leicester",
"Liverpool",
"Man City",
"Man United",
"Newcastle",
"Southampton",
"Stoke",
"Swansea",
"Tottenham",
"Watford",
"West Brom",
"West Ham"]

# Global var for the params
attack_home = np.zeros(20)
attack_away = np.zeros(20)
defense_away = np.zeros(20)
defense_home = np.zeros(20)
av_home_goals = 0.0
av_away_goals = 0.0

def get_params():
  filename = "season-1718.csv"
  filename2 = "season-1819.csv"

  fields1 = []
  fields2 = []
  rows = []
  rows2 = []

  with open(filename, 'r') as csvfile: # 17-18 season
    # creating a csv reader object 
    csvreader = csv.reader(csvfile) 
       
    # extracting field names through first row 
    fields1 = csvreader.next() 

    # extracting each data row one by one 
    for row in csvreader: 
      rows.append(row) 

  with open(filename2,'r') as csvfile: # 18-19 season, uptill now
    csvreader = csv.reader(csvfile)

    fields2 = csvreader.next()
    
    for row in csvreader:
      rows2.append(row)

  fields = np.asarray(fields1)
  rows = np.asarray(rows)
  rows2 = np.asarray(rows2)

  fields = fields[1:6]
  rows = rows[:,1:6]
  rows2 = rows2[:,1:6]
  # HomeTeam, AwayTeam, HomeGoals, AwayGoals, Result

  tot_games = 0
  tot_home_goals = 0.0 # away conceded = home scored
  tot_away_goals = 0.0 # home condeded = away scored
  tot_games_home_perteam = np.zeros(20) # total number of games each team played home
  tot_games_away_perteam = np.zeros(20) # total number of games each team played away  
  tot_home_perteam = np.zeros(20) # total number of goals each scored at their home
  tot_away_perteam = np.zeros(20) # total number of away goals each team scored
  tot_conceded_home_perteam = np.zeros(20) # total number of goals team conceded at home
  tot_conceded_away_perteam = np.zeros(20) # total number of goals team conceded away
  global av_home_goals
  global av_away_goals

  for i in rows:
    tot_home_goals += int(i[2])
    tot_away_goals += int(i[3])
    tot_games += 1

    home_index = teams_to_index.index(i[0])
    away_index = teams_to_index.index(i[1])

    tot_games_home_perteam[home_index] += 1
    tot_games_away_perteam[away_index] += 1

    tot_home_perteam[home_index] += int(i[2])
    tot_away_perteam[away_index] += int(i[3])

    tot_conceded_home_perteam[home_index] += int(i[3])
    tot_conceded_away_perteam[away_index] += int(i[2])

  for i in rows2:
    tot_home_goals += int(i[2])
    tot_away_goals += int(i[3])
    tot_games += 1

    home_index = teams_to_index.index(i[0])
    away_index = teams_to_index.index(i[1])

    tot_games_home_perteam[home_index] += 1
    tot_games_away_perteam[away_index] += 1

    tot_home_perteam[home_index] += int(i[2])
    tot_away_perteam[away_index] += int(i[3])

    tot_conceded_home_perteam[home_index] += int(i[3])
    tot_conceded_away_perteam[away_index] += int(i[2])

  av_home_goals = float(tot_home_goals/tot_games) # sum of all home goals/number of games
  av_away_goals = float(tot_away_goals/tot_games) # sum of all away goals/number of games


  for i in range(20):
    attack_home[i] = (tot_home_perteam[i]/tot_games_home_perteam[i])/av_home_goals
    attack_away[i] = (tot_away_perteam[i]/tot_games_away_perteam[i])/av_away_goals

    defense_away[i] = (tot_conceded_away_perteam[i]/tot_games_away_perteam[i])/av_home_goals
    defense_home[i] = (tot_conceded_home_perteam[i]/tot_games_home_perteam[i])/av_away_goals

  return
get_params()
print(av_home_goals)
print(av_away_goals)
print(attack_home)
print(attack_away)
print(defense_home)
print(defense_away)