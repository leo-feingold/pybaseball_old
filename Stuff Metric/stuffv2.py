from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

dateInitial = '2023-06-25'
dateEnd = '2023-06-27'

def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    data = statcast(start_dt = start, end_dt = end)

    return data

def cleanData(df):
    df = df[["release_speed", "release_spin_rate", "pitcher", "player_name", "pitch_type", "home_team", "away_team", "inning_topbot"]]
    df.dropna(subset=["release_speed", "release_spin_rate", "pitch_type", "home_team", "away_team", "inning_topbot"], inplace=True) 
    df = df[(df["pitch_type"] == "FF")]
    df = df[((df['home_team'] == 'NYY') & (df["inning_topbot"] == "Top")) | ((df["away_team"] == 'NYY') & (df["inning_topbot"] == "Bot"))]

    return df

def visualizeData(df):
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.hist(df['release_speed'], bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Release Speed (mph)')
    plt.ylabel('Frequency')
    plt.title('Histogram of NYY 4-Seam Fastball Release Speed')

    plt.subplot(1, 2, 2)
    plt.hist(df['release_spin_rate'], bins=30, color='lightgreen', edgecolor='black')
    plt.xlabel('Release Spin Rate (rpm)')
    plt.ylabel('Frequency')
    plt.title('Histogram of NYY 4-Seam Fastball Release Spin Rate')

    plt.tight_layout()
    plt.show()

def main():
    data = scrapeData(start=dateInitial, end=dateEnd)
    #print(f"Columns: {data.columns}")

    cleaned_data = cleanData(data)
    #print(f"Sample Cleaned Data: {cleaned_data.head()}")

    print(f"Pitchers: {cleaned_data.player_name.unique()}")
    
    visualizeData(cleaned_data)

if __name__ == "__main__":
    main()