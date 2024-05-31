from pybaseball import playerid_lookup
from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dateInitial = '2024-05-24'
dateEnd = '2024-05-27'

def scrapeAndSaveData(start, end):
    data = statcast(start_dt = start, end_dt = end)
    data.to_csv(f"{start}_to_{end}_statcast_data.csv")
    return data

def selectColumns(df):
    columns = [
    'pitch_type', 'game_date', 'release_speed', 'release_pos_x', 'release_pos_y', 
    'release_pos_z', 'pitcher', 'stand', 'p_throws', 'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'vx0', 'vy0', 'vz0', 'ax', 'ay', 
    'az', 'release_spin_rate', 'release_extension', 'spin_axis'
    ]
    df = df[columns]
    return df

def main():
    data = scrapeAndSaveData(dateInitial, dateEnd)
    data = selectColumns(data)
    print(data.columns)


if __name__ == "__main__":
    main()