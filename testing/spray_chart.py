from pybaseball import statcast_batter
import pandas as pd 
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup
import numpy as np
import seaborn as sns
from matplotlib.patches import Polygon


firstName = 'Anthony'
lastName = 'Volpe'
playerTeam = 'yankees'
playerTeamTag = 'NYY'
start = '2023-01-01'
stop = '2023-12-31'

def getData(nameFirst, nameLast, startDate, endDate):
    player = playerid_lookup(nameLast, nameFirst)
    player_ID = player.loc[0, "key_mlbam"]
    data = statcast_batter(startDate, endDate, player_ID)
    return data

def filterData(df):
    reg_season_condition = df["game_type"] == 'R'
    df = df.loc[reg_season_condition]
    df = df[["home_team", "hc_x", "hc_y", "events", "game_date", "launch_speed", "launch_angle"]]
    df["hit_or_out"] = (df.events == 'single') | (df.events == 'double') | (df.events == 'triple') | (df.events == 'home_run')
    df = df[df["hit_or_out"] == True]
    df = df[df["home_team"] == playerTeamTag]

    return df

def plot_stadium(df, team):
    fig, ax = plt.subplots()
    stadium = pd.read_csv('/Users/leofeingold/Desktop/pybaseball/mlbstadiums.csv')
    team_df = stadium[stadium['team'] == team.lower()]
    for i in stadium['segment'].unique():
        data = team_df[team_df['segment'] == i]
        ax.plot(data['x'],-1*data['y'], linestyle = '-', color = 'black')
    ax.axis('off')

    color_dict = {
        'single': 'brown',
        'double': 'green',
        'triple': 'blue',
        'home_run': 'black'

    }

    for event, color in color_dict.items():
        subset = df[df['events'] == event]
        ax.scatter(subset.hc_x, -1*subset.hc_y, color=color, label=event, alpha=0.7)

    ax.legend()
    ax.set_title(f"{firstName} {lastName} Spray Chart ({start} - {stop})")
    plt.show()

def main():
    data = getData(firstName, lastName, start, stop)
    data = filterData(data)
    plot_stadium(data, playerTeam)

if __name__ == "__main__":
    main()