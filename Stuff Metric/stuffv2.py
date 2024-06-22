from pybaseball import statcast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pybaseball import cache
cache.enable()
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error


dateInitial = '2023-6-1'
dateEnd = '2024-06-1'

def scrapeData(start, end):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    data = statcast(start_dt = start, end_dt = end)
    data.to_csv("2023-6-1To2024-06-1.csv")
    return data

def loadData(csv):
    df = pd.read_csv(csv)
    return df

def sortData(df):
    # Create a count column
    df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

    # Replace 'hit_into_play' descriptions with corresponding 'events'
    df.loc[df['description'] == 'hit_into_play', 'description'] = df['events']

    # Combine similar events
    '''
    ['called_strike' 'foul' 'blocked_ball' 'field_out' 'ball' 'double'
    'swinging_strike' 'single' 'force_out' 'triple' 'home_run' 'foul_tip'
    'sac_bunt' 'swinging_strike_blocked' 'sac_fly' 'double_play'
    'grounded_into_double_play' 'foul_bunt' 'hit_by_pitch' 'field_error'
    'missed_bunt' 'fielders_choice' 'fielders_choice_out' 'catcher_interf'
    'pitchout' 'sac_fly_double_play' 'bunt_foul_tip' 'triple_play']
    '''


    df['description'] = df['description'].replace(['ball', 'blocked_ball'], 'ball')
    df['description'] = df['description'].replace(['swinging_strike', 'swinging_strike_blocked', 'foul_tip'], 'swinging_strike')
    df['description'] = df['description'].replace(['field_out', 'triple_play', 'force_out', 'fielders_choice_out', 'double_play', 'grounded_into_double_play'], 'field_out')

    # Filter relevant descriptions
    relevant_descriptions = ['called_strike', 'foul', 'field_out', 'ball', 'double', 'swinging_strike', 'single', 'triple', 'home_run', 'hit_by_pitch']
    df = df[df['description'].isin(relevant_descriptions)]

    # Group by description and count, then calculate the mean of delta_run_exp
    mean_delta_run_exp = df.groupby(['description', 'count'])['delta_run_exp'].mean().reset_index()
    mean_delta_run_exp.columns = ['description', 'count', 'mean_delta_run_exp']

    return df, mean_delta_run_exp

def mergeData(df, sorted_df):
    df_with_mean_exp = pd.merge(df, sorted_df, on=['description', 'count'], how='left')
    return df_with_mean_exp


def visualizeData(df):
    home_run_data = df[df['description'] == 'home_run']
    plt.figure(figsize=(10, 6))
    plt.bar(home_run_data['count'], home_run_data['mean_delta_run_exp'], color='blue')
    plt.xlabel('Count')
    plt.ylabel('Mean Delta Run Expectancy')
    plt.title('Mean Delta Run Expectancy for Home Runs by Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def cleanData(df): 
    df = df[['release_speed', 'release_pos_x', 'release_pos_z', 'pfx_x', 'pfx_z', 'release_spin_rate', 'release_extension', 'spin_axis', 'mean_delta_run_exp']] 
    # Convert all columns to numeric and drop rows with NaN values
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    print(f"Length: {len(df)}")
    return df

def splitData(df):
    X = df.drop('mean_delta_run_exp', axis=1)
    y = df['mean_delta_run_exp']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def trainModel(X_train, y_train):
    # Use Random Forest Regressor and perform Grid Search for hyperparameter tuning
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    rf = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_
    return best_model


def evaluateModel(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")

    return y_pred


def main():
    #data = scrapeData(start=dateInitial, end=dateEnd)
    csv = "/Users/leofeingold/Desktop/pybaseball/Stuff Metric/2023-6-1To2024-06-1.csv"
    df = loadData(csv)
    df, df_sorted = sortData(df)
    #visualizeData(df_sorted)
    good_df = mergeData(df, df_sorted)
    cleaned_df = cleanData(good_df)
    X_train, X_test, y_train, y_test = splitData(cleaned_df)
    model = trainModel(X_train, y_train)
    y_pred = evaluateModel(model, X_test, y_test)


if __name__ == "__main__":
    main()