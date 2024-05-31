from pybaseball import statcast_batter
import pandas as pd 
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup
import numpy as np
import seaborn as sns

firstName = 'Anthony'
lastName = 'Volpe'
start = '2023-01-01'
stop = '2023-12-31'

def getData(nameFirst, nameLast, startDate, endDate):
    player = playerid_lookup(nameLast, nameFirst)
    player_ID = player.loc["key_mlbam"]
    data = statcast_batter(startDate, endDate, player_ID)
    return data

def filterData(df):
    reg_season_condition = df["game_type"] == 'R'
    df = df.loc[reg_season_condition]
    df = df[["hc_x", "hc_y", "events", "game_date", "launch_speed", "launch_angle"]]
    df["hit_or_out"] = (df.events == 'single') | (df.events == 'double') | (df.events == 'triple') | (df.events == 'home_run')
    return df

def main():
    data = getData(firstName, lastName, start, stop)
    data = filterData(data)
    print(data.head())


if __name__ == "__main__":
    main()