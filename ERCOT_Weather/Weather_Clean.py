# -*- coding: utf-8 -*-
"""
WEATHER CLEAN 

The purpose of this script is to pull, clean, format, and save historic
Texas weather data


Created on Sat Jul 31 16:54:25 2021

@author: Colburn_Hassman
@contact: colburn.hassman@gmail.com
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

os.chdir("/home/colburn/Documents/Power_Modelling/ERCOT_Weather")

def pull_data():
    data = pd.DataFrame()
    for i in range(1,5):
        file = "weather_0{}.csv".format(i)
        print("Pulling {}".format(file))
        temp_df = pd.read_csv(file)
        data = data.append(temp_df)
    #data['DATE'] = pd.to_datetime(data['DATE'])
    return data
    


def seperate_data(data):
    # Dirty way of seperating 
    EL_PASO = data[data['NAME'] == 'EL PASO INTERNATIONAL AIRPORT, TX US'] 
    CORPUS_CHRISTI = data[data['NAME'] == 'CORPUS CHRISTI INTERNATIONAL AIRPORT, TX US']
    HOUSTON = data[data['NAME'] == 'HOUSTON INTERCONTINENTAL AIRPORT, TX US']
    #HOUSTON['TMAX'].plot()
    SAN_ANTONIO = data[data['NAME'] == 'SAN ANTONIO STINSON MUNICIPAL AIRPORT, TX, US']
    DALLAS = data[data['NAME'] == 'DALLAS FAA AIRPORT, TX US']
    TYLER = data[data['NAME'] == 'TYLER, TX US']
    LUBBOCK = data[data['NAME'] == 'LUBBOCK INTERNATIONAL AIRPORT, TX US']
    ABILENE = data[data['NAME'] == 'ABILENE REGIONAL AIRPORT, TX US']
    MIDLAND = data[data['NAME'] == 'MIDLAND INTERNATIONAL AIRPORT, TX US']
    SAN_ANGELO = data[data['NAME'] == 'SAN ANGELO MATHIS FIELD AIRPORT, TX US']
    BROWNSVILLE = data[data['NAME'] == 'BROWNSVILLE S PADRE ISLAND INTERNATIONAL AIRPORT, TX US']
    AUSTIN = data[data['NAME'] == 'AUSTIN BERGSTROM INTERNATIONAL AIRPORT, TX US']
    FORT_WORTH = data[data['NAME'] == 'FORT WORTH ALLIANCE AIRPORT, TX US']
    
    # Put dfs into a list
    cities = [EL_PASO, CORPUS_CHRISTI, HOUSTON, SAN_ANTONIO, 
              DALLAS, TYLER, LUBBOCK, ABILENE, MIDLAND, 
              SAN_ANGELO, BROWNSVILLE, AUSTIN, FORT_WORTH]
    return cities


def calculate(cities):
    for city in cities:
        city['AMP'] = (city['TMAX'] - city['TMIN'])/2
        city['TAVG_1'] = city['TAVG'].shift(-1)
        city['AMP_1'] = city['AMP'].shift(-1)
        
        
def hourly(row):
    hours = np.arange(0,24) # add step with another column
    date_time = []
    temp = []
    RISE = 8
    # Need to add the missing data
    if row['TAVG'] == np.nan:
        row.loc['TAVG'] = (row['TMAX'] + row['TMIN'])/2
    for hour in hours:
        # Make timestamp
        time = "{:02d}:00".format(hour)
        date_time.append(row['DATE'] + " " + time)
        # Make temperature
        if hour <= RISE:
            t = row['TAVG'] - row['AMP'] * (np.cos((np.pi*hour/(10+RISE))))
            temp.append(t)
        elif hour > RISE & hour <= 14:
            t = row['TAVG'] + row['AMP'] * (np.cos((np.pi*(hour-RISE)/14-RISE)))
            temp.append(t)
        else:
            t = row['TAVG_1'] - row['AMP_1'] * (np.cos((np.pi*hour/(10+RISE))))
            temp.append(t)

    return date_time, temp
        
def map_hourly(file_name, data):
    # File name should not have .pkl size
    # data is a Dataframe which will be converted to hourly and written to pkl
    Date = []
    Temperature = []
    for index, row in data.iterrows():       
        # Need to add the missing data
        date, temp = hourly(row) # returns lists of hourly timestamps and temperature estimates
        # Unpacks the lists and appends them individually
        for time in date:
            Date.append(time)
        for t in temp:
            Temperature.append(t)
        
    temp_df = pd.DataFrame()
    temp_df['Date'] = Date
    temp_df['Temp'] = Temperature
    temp_df['Temp'].plot()
   
    
    
    print("Writing {}".format(file_name))
    path = file_name + ".pkl"
    temp_df.to_pickle(path)
    
        
        
def main():
    data = pull_data()
    # Fix the NaNs in the TAVG
    data['TAVG'] = data.apply(
        lambda row: (row['TMAX']+row['TMIN'])/2 if np.isnan(row['TAVG']) else row['TAVG'],
        axis = 1)
    # Also has an issu where average was 0, especially on some of the older days. 
    # Assume no day in Texas has a 0 avg farenheit 
    data['TAVG'] = data.apply(
        lambda row: (row['TMAX']+row['TMIN'])/2 if row['TAVG']==0 else row['TAVG'],
        axis = 1)
    print("Seperating Cities")
    cities = seperate_data(data)

    calculate(cities)
    
    cities_names = ["EL_PASO", "CORPUS_CHRISTI", "HOUSTON", "SAN_ANTONIO", 
                    "DALLAS", "TYLER", "LUBBOCK", "ABILENE", "MIDLAND", 
                    "SAN_ANGELO", "BROWNSVILLE", "AUSTIN", "FORT_WORTH"]
    i = 0
    for city in cities:
        map_hourly(cities_names[i], city)
        i = i + 1

if __name__ == "__main__":
    main()
        
    
        

