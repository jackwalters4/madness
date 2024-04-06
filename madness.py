import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

# Make bar chart based off Year and Madness Score
def make_bar_chart(year_scores): 
    plt.figure(figsize=(8, 6))
    plt.bar(np.array(year_scores.index), np.array(year_scores['SCORE']), color='green', edgecolor='black', width=0.6)

    plt.xlabel('Year')
    plt.ylabel('Madness Score')
    plt.title('Madness Score per year')

    plt.xticks(rotation=45)
    # plt.yticks(np.arange(100, 400, 20))
    plt.show()

# round of 64 = 0 round advanced, 32 round_eliminated = 1 round advanced, 
# 16 = 2 rounds advanced, 8 = 3 rounds advanced, 4 = 4 rounds advanced
# 2 = 5 rounds advanced, 1 = 6 rounds advanced

# Based on above: 64 / 2^(round_advanced) = round_eliminated
# ergo (crank some algebra)... round_advanced = log2(64/round_eliminated)
def team_score(row):
    round_advanced = int(math.log2(64/row['ROUND']) if row['ROUND'] != 68 else 0)
    return round_advanced * row['SEED']

# No upsets. Every lower seed beats every higher seed
def calculate_min_tourney_score():
    ## first round wipes out 16 - 9 seeds (32 teams elim) = 0 round_advanced
    first_round = 0
    ## second round wipes out 8 - 5 seeds (16 teams elim) = 1 round_advanced
    second_round = 1*(8*4 + 7*4 + 6*4 + 5*4)
    ## third round wipes out 4 and 3 seeds (8 teams elim) = 2 round_advanced
    third_round = 2*(4*4 + 3*4)
    ## fourth round wipes out 2 seeds (4 teams elim) = 3 round_advanced
    fourth_round = 3*(2*4)
    ## fifth round wipes out half of the 1 seeds (2 teams elim) = 4 round_advanced
    fifth_round = 4*(2*2)
    ## championship => a 1 seed wins, a 1 seed loses
    championship = 5*1 + 6*1

    return first_round + second_round + third_round + fourth_round + fifth_round + championship


def calculate_max_tourney_score():
    return 0


print(calculate_min_tourney_score())

# Read the CSV file into a DataFrame: 
# team, seed, round eliminated from 2008 onwards (~15 years)
df = pd.read_csv('madness_2008.csv')

# For each unique year,
# calculate a score by the sum of each team's score
# filter out teams eliminated in round 68 (play-in games)

df = df[df['YEAR'] < 2024] # has all zeros filled out for 2024 right now
df['SCORE'] = df.apply(team_score, axis=1)

# group by year and sum the team scores
year_scores = df.groupby('YEAR').sum('SCORE').sort_values('SCORE', ascending=False)
year_scores['SCORE'] = year_scores['SCORE'].apply(lambda x: x - calculate_min_tourney_score())

print(year_scores['SCORE'])

make_bar_chart(year_scores)


