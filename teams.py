import os
import numpy as np
import sys
import scipy
import csv
import time
np.set_printoptions(threshold=sys.maxsize)
num_iter = 1000

start = time.time()

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

# print(av_home_goals)
# print(av_away_goals)
# print(attack_home)
# print(attack_away)
# print(defense_home)
# print(defense_away)
# 0 to 19

# Set up the schedule - form not considered, does not make a difference
schedule = np.asarray([[0,1]])
for i in range(20):
  for j in range(20):
#    print(i,j)
    if ((i == (j-1)) and (i == 0)):
      temp = np.asarray([[i,j]]) 
    elif (i != j) :
      schedule = np.append(schedule,[[i,j]], axis = 0)     
np.random.shuffle(schedule)

def league_sim():
  # Set up data structure for the table
  table = np.zeros((20,9)) # ordered as per teams to index
  # Played, Wins, Draws, Losses, Goals For, Goals Against, Goal Diff, Points, index
  for i in range(20):
    (table[i])[8] = i

  #print(schedule)

  for match in schedule:
    hometeam_stats = table[match[0]]
    awayteam_stats = table[match[1]]

    # both play a game
    hometeam_stats[0] = hometeam_stats[0] + 1
    awayteam_stats[0] = awayteam_stats[0] + 1 

    # Get the goals both teams scored
    goals_home = np.random.poisson((av_home_goals*attack_home[match[0]]*defense_away[match[1]])) # TODO - how are goals generated 
    goals_away = np.random.poisson((av_away_goals*attack_away[match[1]]*defense_home[match[0]])) # TODO - how are goals generated

    if(goals_home > goals_away):
      hometeam_stats[1] += 1 # home won
      awayteam_stats[3] += 1 # away lost

      hometeam_stats[4] += goals_home # GF home
      hometeam_stats[5] += goals_away # GA home

      awayteam_stats[4] += goals_away # GF away
      awayteam_stats[5] += goals_home # GA away

      hometeam_stats[6] += (goals_home - goals_away) # GD home
      awayteam_stats[6] -= (goals_home - goals_away) # GD away
      
      hometeam_stats[7] += 3 # Winner gets points
    elif(goals_home == goals_away):
      hometeam_stats[2] += 1 # home drew
      awayteam_stats[2] += 1 # away drew

      hometeam_stats[4] += goals_home # GF home
      hometeam_stats[5] += goals_away # GA home

      awayteam_stats[4] += goals_away # GF away
      awayteam_stats[5] += goals_home # GA away
      
      hometeam_stats[7] += 1 # both get points
      awayteam_stats[7] += 1
    else : #(goals_home < goals_away)
      hometeam_stats[3] += 1 # home lost
      awayteam_stats[1] += 1 # away won

      hometeam_stats[4] += goals_home # GF home
      hometeam_stats[5] += goals_away # GA home

      awayteam_stats[4] += goals_away # GF away
      awayteam_stats[5] += goals_home # GA away

      hometeam_stats[6] += (goals_home - goals_away) # GD home
      awayteam_stats[6] -= (goals_home - goals_away) # GD away
      
      awayteam_stats[7] += 3 # Winner gets points

    table[match[0]] = hometeam_stats
    table[match[1]] = awayteam_stats

  #print(table)

  # use mergesort as it is a stable sort
  # the intial sorting remains if later sorting is not able to resolve
  # last by Points, then GD, GF, GA
  table = table[table[:,3].argsort(kind = 'mergesort')[::-1]] # sort by losses, reverse
  table = table[table[:,1].argsort(kind = 'mergesort')] # sort by wins
  table = table[table[:,4].argsort(kind = 'mergesort')] # sort by GF
  table = table[table[:,6].argsort(kind = 'mergesort')] # sort by GD
  table = table[table[:,7].argsort(kind = 'mergesort')[::-1]] # sort by points
  # print(table) # if all above same, alphabetical 
  return table

num_wins = np.zeros(20)
av_points = np.zeros(20)

for i in range(num_iter):
  table = league_sim()
  num_wins[int(table[0][8])] += 1
  for j in range(20):
    av_points[j] += table[j][7]

av_points = av_points/num_iter

print(num_wins)
print(av_points)

with open("op1.txt","a") as file:
  file.write("new sim starts, num iter is %d\n"% num_iter)
  file.write("num wins is\n")
  for i in range(20):
    file.write("%s  -  %d \n"% (teams_to_index[i],num_wins[i]))
  file.write(" \n")
  file.write("Average points total is\n")
  for i in range(20):
    file.write("%dth place - %6.2f \n"% ((i+1),av_points[i]))
  file.write(" \n")




end = time.time()
print(end-start)