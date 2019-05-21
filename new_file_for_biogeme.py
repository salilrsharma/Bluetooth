# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:33:15 2019

@author: salilsharma
"""

import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from localfunctions import*
from clusterAlgorithm import*
import math
from scipy.io import loadmat

#Function to compute path choice based on realized travel times and a ranking system
def path_choice(row):
# =============================================================================
    if min(row.a3, row.a4, row.a6, row.a7) == row.a3:
        return 3
    elif min(row.a3, row.a4, row.a6, row.a7) == row.a4:
        return 4
    elif min(row.a3, row.a4, row.a6, row.a7) == row.a6:
         return 6
#     #elif min(row.a1, row.a2, row.a3, row.a4, row.a5, row.a6, row.a7) == row.a4:
#     #    return 4
#     #elif min(row.a1, row.a2, row.a3, row.a4, row.a5, row.a6, row.a7) == row.a5:
#     #    return 5
#     elif min(row.a3, row.a4, row.a6, row.a7) == row.a6:
#         return 6
#     else:
#         return 7
# =============================================================================
    else:
        return 7
    
    
    
#import truck data
Masterpath='pathname'
truck_data=pd.read_pickle(Masterpath + 'xxx.pkl')
#plt.plot(truck_data['TOD'], truck_data['TT'], '.')

#create a dictionary with date as the keys to generate integer date
whichDate={'10-02':0,'10-03':1,'10-04':2,'10-06':4,'10-09':5,'10-10':6,'10-11':7,'10-12':8,\
           '10-13':9,'10-16':10,'10-17':11,'10-18':12,'10-19':13,'10-20':14,'10-23':15,\
           '10-24':16,'10-25':17,'10-26':18,'10-27':19, '10-30':20,'10-31':21,'11-01':22,\
           '11-02':23,'11-03':24,'11-06':25,'11-07':26,'11-08':27,'11-09':28,'11-10':29,\
           '11-13':30,'11-14':31,'11-15':32,'11-16':33,'11-17':34,'11-20':35,'11-21':36,\
           '11-22':37,'11-23':38,'11-24':39}

truck_data['intDate']= truck_data['DATE'].map(whichDate)
#Next step is to assign a 15 min of interval which maps to TOA
df=truck_data.assign(time_interval = lambda x: np.floor((x['TOA']-15)/15))

df2=df[df['time_interval'] <=83]
df3 = df2.query('6 <= TOA <= 1250')
#df2.assign(rel = lambda x: reliability.iloc[x['intDate'],x['time_interval']-1])
df3['rt'] = np.floor(df3['TOA'])

#Number of rows
number_of_rows = df3.shape[0]


#path size information

ps = [(1/66.1) * (30.5/3 + 13.1/2 + 9.2/2 + 13.3/3), \
      (1/71.2) * (10.7/3 + 19.6/2 + 27.6/3 + 13.3/3), \
      (1/61.6) * (30.5/3 + 13.1/2 + 12/2 + 6/4), \
      (1/107.5) * (84.2/1 + 17.3/2 + 6/4), \
      (1/87.7) * (10.7/3 + 36.1/1 + 27.6/3 + 13.3/3), \
      (1/85.1) * (10.7/3 + 19.6/2 + 27.6/3 + 9.2/2 + 12/2 + 6/4), \
      (1/74.2) * (30.5/3 + 20.4/1 + 17.3/2 + 6/4)]

#Now work with traffic data
#step1: read excel file
name_list=[];
path_list = [1,2,3,4,5,6,7]
j=0
for i in path_list:
    j = j+1
    #call excel file from RCdata folder
    filename='D:/salilsharma/SurfDrive/My Documents/TU Delft/RCdata/1-7/Path'+\
    str(i)+'/1-7_'+str(i)+'.xlsx'
    
    #read specific excel sheets fro realized time, density, lc, reliability, length
    realized_time = pd.read_excel(filename, sheet_name = 0)
    path_density = pd.read_excel(filename, sheet_name = 1)
    lane_closures = pd.read_excel(filename, sheet_name = 2)
    reliability = pd.read_excel(filename, sheet_name = 3)
    length = pd.read_excel(filename, sheet_name = 5, header=None)
    
    # =============================================================================
    # # print length of a path
    # length[0]
    # 
    # #print a row of a dataframe
    # realized_time.iloc[2].plot()
    # 
    # path_density.iloc[1].plot()
    # 
    # realized_time.describe()
    # 
    # =============================================================================
    rel = [reliability.get_value(row, col) for row, col in zip(df3['intDate'],df3['time_interval']-1 )]
    den = [path_density.get_value(row, col) for row, col in zip(df3['intDate'],df3['time_interval']-1 )]
    r_tt = [realized_time.get_value(row, col) for row, col in zip(df3['intDate'],df3['rt']-1 )]
    
    #Create some variable names
    var1='r'+str(j)
    var2='d'+str(j)
    var3='u'+str(j)
    var4='td'+str(j)
    var5='a'+str(j)
    var6='ps'+str(j)
    name_list.extend([var1, var2, var3, var4, var5, var6])
    df3[var1] = r_tt
    df3[var2] = den
    df3[var3] = rel
    temp_l = length[0].values
    length_vector = [temp_l[0]/1000] * number_of_rows
    df3[var4] = length_vector
    df3[var5] = abs(df3['TT'] - r_tt)
    ps_vector = [ps[j-1]] * number_of_rows
    df3[var6] = ps_vector
    
#filter noise or stops for truck data
df3['minTT'] = (df3[['r3','r4','r6','r7']].min(axis=1))*0.90
df3['maxTT'] = (df3[['r3','r4','r6','r7']].max(axis=1))*1.10

df4 = df3.query("minTT <= TT <=maxTT")

plt.plot(df4['TOA'], df4['TT'],'.')

df4.loc[:, 'PATH_CHOICE'] = df4.apply(path_choice, axis=1)

#Print all the columns to be selected
print(name_list)
df5 = df4[['ID','r1', 'd1', 'u1', 'td1', 'a1', 'ps1', 'r2', 'd2', 'u2', 'td2', 'a2', 'ps2', 'r3', 'd3', 'u3', 'td3', 'a3', 'ps3', 'r4', 'd4', 'u4', 'td4', 'a4', 'ps4', 'r5', 'd5', 'u5', 'td5', 'a5', 'ps5', 'r6', 'd6', 'u6', 'td6', 'a6', 'ps6', 'r7', 'd7', 'u7', 'td7', 'a7', 'ps7', 'PATH_CHOICE']]
       
#drop rows with missign values
df5 = df5.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)   
df5.to_excel("4_2.xlsx")
