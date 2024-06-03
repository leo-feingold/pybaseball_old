from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

dateInitial = '2024-05-26'
dateEnd = '2024-05-27'

def scrapeData(start, end):
    data = statcast(start_dt = start, end_dt = end)
    return data

def cleanData(df): 
    df = df[['pitch_type', 'release_speed', 
        'release_pos_x', 'release_pos_z', 'spin_dir',
        'pfx_x', 'pfx_z', 'plate_x', 'plate_z', 'vx0',
        'vy0', 'vz0', 'ax', 'ay', 'az', 'release_spin_rate',
        'release_extension', 'spin_axis' 'delta_run_exp']] 
    df.dropna()
    return df

def splitData(df):
    X = df.drop('delta_run_exp', axis=1)
    y = df['delta_run_exp']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def trainModel(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred

def visualizeData(X_train, y_test, y_pred):
    r2 = r2_score(y_test, y_pred)
    numSamples = X_train.shape[0]
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual Delta Run Expectancy")
    plt.ylabel("Predicted Delta Run Expectancy")
    plt.title(f"Stuff+ Model: r^2 = {r^2}, ({numSamples} Samples)")
    plt.show()

def main():
    data = scrapeData(start=dateInitial, end=dateEnd)
    data = cleanData(data)
    X_train, X_test, y_train, y_test = splitData(data)
    y_pred = trainModel(X_train, X_test, y_train, y_test)
    visualizeData(X_train, y_test, y_pred)

if __name__ == "__main__":
    main()