from pybaseball import playerid_lookup
from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dateInitial = '2024-05-26'
dateEnd = '2024-05-27'

def scrapeData(start, end):
    data = statcast(start_dt = start, end_dt = end)
    return data

def cleanData(df): 
    data = data[['pitch_type', 'release_speed', 
        'release_pos_x', 'release_pos_z', 'spin_dir',
        'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'vx0',
        'vy0', 'vz0', 'ax', 'ay', 'az', 'release_spin_rate',
        'release_extension', 'spin_axis' 'delta_run_exp']] 
    data.dropna()
    return data



def main():
    data = scrapeData(start=dateInitial, end=dateEnd)
    print(data.columns)

if __name__ == "__main__":
    main()