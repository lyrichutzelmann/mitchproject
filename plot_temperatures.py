# Author: Marina Reggiani-Guzzo
# Last modified: April 3, 2026

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import datetime

def create_dataframe(filename: str):
    df = pd.read_csv(filename, low_memory=False)
    df = df.drop(['#group', 'false', 'false.1', 'true', 'true.1', 'true.2', 'true.3'], axis=1) # remove undesired columns
    df.rename(columns={'false.2': 'timestamp'}, inplace=True) # rename column to a more meaningful name
    df.rename(columns={'false.3': 'measurement'}, inplace=True) # rename column to a more meaningful name
    df = df.drop([0,1,2], axis=0) # remove undesired rows
    df.reset_index(drop=True, inplace=True) # reset row index, so it starts at row=0
    df['measurement'] = df['measurement'].astype(float) # transform column 'measurement' from string to float
    return df

if __name__ == "__main__":

    # create dataframe for all temperature probes
    df_temp_top = create_dataframe('csv_files/labjack_temperature_top.csv')
    df_temp_topmid = create_dataframe('csv_files/labjack_temperature_topmiddle.csv')
    df_temp_bot = create_dataframe('csv_files/labjack_temperature_bottom.csv')
    df_temp_botmid = create_dataframe('csv_files/labjack_temperature_bottommiddle.csv')

    # Pick first n_rows of your dataframe. Comment lines 29-33 if you want to use the entire dataframe
    n_rows = 50 # number of lines you want to select
    df_temp_top = df_temp_top.loc[:n_rows]
    df_temp_topmid = df_temp_topmid.loc[:n_rows]
    df_temp_bot = df_temp_bot.loc[:n_rows]
    df_temp_botmid = df_temp_botmid.loc[:n_rows]

    # Print dataframe as a table on the terminal, so you can see how data is being saved
    print(df_temp_top.head())

    # Plot
    # Lines 50-54 are just making timestamp look nicer on the plot
    fig, ax = plt.subplots() # create canvas
    ax.plot(range(0,len(df_temp_top)), df_temp_top['measurement'], label="Top", color='orange') # plot top probe
    ax.plot(range(0,len(df_temp_topmid)), df_temp_topmid['measurement'], label="Top Middle", color='green') # plot top middle probe
    ax.plot(range(0,len(df_temp_bot)), df_temp_bot['measurement'], label="Bottom", color='cyan') # plot bottom middle probe
    ax.plot(range(0,len(df_temp_botmid)), df_temp_botmid['measurement'], label="Bottom Middle", color='purple') # plot bottom probe
    ax.legend() # add legend to canvas
    ax.set_title('Cryostat Temperature') # add title to the canvas/plot
    ax.set_ylabel('Temperature [K]') # label y axis
    ax.set_xlabel('Timestamp') # label x axis
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5)) # limit y axis to display 5 values (otherwise it gets too poluted)
    tick_positions = ax.get_xticks() # get the x position of the ticks
    tick_positions = tick_positions[1:-1] # remove first and last entries
    arr = df_temp_top.loc[tick_positions, "timestamp"].to_numpy() # retrieve timestamp from dataframe from the selected entries
    timestamp_readable = pd.to_datetime(arr).strftime("%b %-d, %Y\n%H:%M:%S") # re-shape timestamp to more readable format
    plt.xticks(tick_positions, timestamp_readable, rotation='vertical', ha="center") # replace ticks with timestamps
    plt.tight_layout() # ensure the plot&axis fits in canvas
    plt.show() # plot everything