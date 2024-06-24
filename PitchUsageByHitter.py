from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pybaseball import cache
cache.enable()

warnings.simplefilter(action='ignore')

date_initial = "2024-4-5"
date_final = "2024-6-23"

def scrape_data(start, end):
    df = statcast(start_dt=start, end_dt=end)
    return df

def clean_data(df):
    df = df[df["game_type"] == "R"]
    df = df[["pitch_type", "player_name", "p_throws", "stand", "estimated_woba_using_speedangle"]]

    pitch_names = {
        'FS': 'Splitter',
        'SI': 'Sinker',
        'FF': 'Four-Seam Fastball',
        'SL': 'Slider',
        'CU': 'Curveball',
        'FC': 'Cutter',
        'ST': 'Sweeping Curve',
        'CH': 'Changeup',
        'PO': 'Pitch Out',
        'KC': 'Knuckle Curve',
        'SV': 'Screwball',
        'EP': 'Eephus',
        'FA': 'Fastball',
        None: 'Unknown'
    }

    df["pitch_type"] = df["pitch_type"].map(pitch_names)

    return df

def visualize_data(df):
    player_first_name = "Marcus"
    player_last_name = "Stroman"
    player = f"{player_last_name}, {player_first_name}"

    throws = df["p_throws"].iloc[0] if not df.empty else df["p_throws"].iloc[7]
    df = df[df["player_name"] == player]
    df_lefty_batter = df[df["stand"] == "L"]
    df_righty_batter = df[df["stand"] == "R"]

    lefty_counts = df_lefty_batter["pitch_type"].value_counts(normalize=True) * 100
    righty_counts = df_righty_batter["pitch_type"].value_counts(normalize=True) * 100

    lefty_xwoba = df_lefty_batter.groupby("pitch_type")["estimated_woba_using_speedangle"].mean().fillna(0.000)
    righty_xwoba = df_righty_batter.groupby("pitch_type")["estimated_woba_using_speedangle"].mean().fillna(0.000)

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.bar(lefty_counts.index, lefty_counts.values, edgecolor='black')
    plt.title(f'Pitch Types vs Lefty Batters ({len(df_lefty_batter)} Pitches)')
    plt.xlabel('Pitch Type')
    plt.ylabel('Percentage (%)')
    for i, pitch in enumerate(lefty_counts.index):
        plt.text(i, lefty_counts[pitch], f'{lefty_xwoba[pitch]:.3f}', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    plt.bar(righty_counts.index, righty_counts.values, edgecolor='black')
    plt.title(f'Pitch Types vs Righty Batters ({len(df_righty_batter)} Pitches)')
    plt.xlabel('Pitch Type')
    plt.ylabel('Percentage (%)')
    for i, pitch in enumerate(righty_counts.index):
        plt.text(i, righty_counts[pitch], f'{righty_xwoba[pitch]:.3f}', ha='center', va='bottom', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    plt.xticks(rotation=45)

    plt.suptitle(f"{player_first_name} {player_last_name} ({throws}HP): LHH and RHH Pitch Mix with xwOBA Against\n(Date Range: {date_initial} through {date_final})")
    plt.tight_layout()
    plt.show()



def main():
    data = scrape_data(date_initial, date_final)
    #print(data.game_type)
    cleaned_data = clean_data(data)
    visualize_data(cleaned_data)

if __name__ == "__main__":
    main()