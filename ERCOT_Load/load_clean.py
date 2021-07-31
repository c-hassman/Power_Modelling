#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 09:09:51 2021

# Script to Clean Hourly ERCOT Load Data


@author: Colburn Hassman
"""

import pandas as pd
import os
os.chdir("/home/colburn/Documents/Power_Modelling/ERCOT_Load")


def clean_columns(col):
    '''
    Creates Uniform Column names for the ERCOT Load Data

    Parameters
    ----------
    col : list of column names from ERCOT Load Data

    Returns
    -------
    Column list with uniform names

    '''
    for i in range(len(col)):
        if(col[i] == "FWEST"):
            col[i] = "FAR_WEST"
        elif(col[i] == "Hour Ending"):
            col[i] = "Hour_End"
        elif(col[i] == "HourEnding"):
            col[i] = "Hour_End"
        elif(col[i] == "NCENT"):
            col[i] = "NORTH_CENTRAL"
        elif(col[i] =="NORTH_C"):
            col[i] = "NORTH_CENTRAL"
        elif(col[i] == "SCENT"):
            col[i] = "SOUTH_CENTRAL"
        elif(col[i] =="SOUTH_C"):
            col[i] = "SOUTH_CENTRAL"
        elif(col[i] == "SOUTHERN"):
            col[i] = "SOUTH"
        else:
            pass
    return(col)


def catch_24(data):
    '''
    The goal of this function is to fix these ridiculous ERCOT time issues. 
    The typical thing in Energy is quoted in "Hour Ending" but of course in 
    Datetime objects, hour 24:00 doesn't exist.. thats hour 00:00. Also, 
    Some hours are recorded at the 59th minute the hour before...
    
    Took some time to figure out how to do it but luckily there are some good 
    Datetime tool

    Parameters
    ----------
    data : Dataset with a column containing Datetime names "Hour_End"

    Returns
    -------
    Same Dataset but with good clean time stamps
    
    http://www.ercot.com/services/comm/mkt_notices/archives/1701
    
    
    '''
    #print(data.head())
    # This captures the issue with hour 24:00. 
    data['Hour_End'] = data['Hour_End'].str.replace("24:00", "23:59")
    # Copy only values. will reassign late
    time = data['Hour_End'].values
    # convert to datetime. No problems with inferring from string timestamp
    time = pd.to_datetime(time)
    # Set the timezone. nonextistent choice based off ercot link above
    time = time.tz_localize("America/Chicago", ambiguous = "NaT",
                            nonexistent = "shift_forward")
    # Round time to nearest hour: dealing with 59th minute issues
    time = time.round("H")
    # Reassign Hour End 
    data['Hour_End'] = time
    # COME BACK TO, CURRENTLY DROPS VALUES WITH DST
    data.dropna(subset = ['Hour_End'], inplace = True)
    # set time as index for DF
    data = data.set_index('Hour_End')
    return(data)
    
     
 
     
def pull_combine(data, path):
    """
    Pulls in data from csv, cleans, and combines

    Parameters
    ----------
    data : original dataset 
    
    path : path to csv file
    
    Returns
    -------
    data : dataset with new data in it
    """
    # Pull in data
    new_data = pd.read_csv(path)
    # Clean and overwrite Columns
    new_data_col = list(new_data.columns.values)
    new_data.columns = clean_columns(new_data_col)
    # Send to TS helper function
    new_data = catch_24(new_data)
    # Ensure Columns are all numeric:
    cols = new_data.columns
    # Remove All Commas, which was leading to an issue with pd.to_numeric
    new_data = new_data.replace(",",'', regex = True)
    new_data[cols] = new_data[cols].apply(pd.to_numeric, errors = "coerce")
    # Combine Data
    data = data.append(new_data)
    
    return data

def main():
    data = pd.DataFrame()
    for i in range(2,22,1):
        year = "{:02d}".format(i)
        path = "20{}.csv".format(year)
        print("Pulling and Combining {}".format(path))
        data = pull_combine(data, path)
    print("Writing to Pickle")
    data.to_pickle("ERCOT_Load.pkl")

if __name__ == "__main__":
    main()

#df = pd.DataFrame()
#df = pull_combine(df, "2017.csv")
#print(df.loc[df.index.isnull().any()] == 'True')
#rows = df.index.isnull()
#df_na = df[rows]
#print(df_na)

#print(df.columns)
#print(df.dtypes)
   

    