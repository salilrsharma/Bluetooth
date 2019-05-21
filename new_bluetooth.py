# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 16:53:04 2018

@author: salilsharma
"""
# %%Data collection between two point
# Cluster trucks

import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from localfunctions import*
from clusterAlgorithm import*
import pickle


start_time = time.time()

time_diff=120
whichDate='10-02'

filename='xxx.json'
data=upload_data(filename,json)

detection=data['detections'];

# len(v) >=6 to ensure that macID has at least 3 registrations.
df=pd.concat({k: pd.DataFrame(v) for k, v in detection.items()if len(v) >= 6 })

df["locationId"] = df['locationId'].astype('int')

travel_time=[]

query_string=make_query(Points)
search_list=make_search_list(Points)
    
idx = (set(df[df['locationId'] == i].index.get_level_values(0)) for i in search_list)
a = set.intersection(*idx)

df2=df.to_records()

df3=pd.DataFrame.from_records(df2)

df3["dateTime"]=pd.to_datetime(df3['dateTime']) # vectorized - very fast

for i in a:   
    aa=df3[df3['level_0'].values==i]
    travel_time=travel_time_data(aa,Points,query_string,pd,travel_time)
        
#generate_plot(travel_time, Points,plt, whichDate, 30)

Z=generate_bluetooth_data(travel_time,20)

df4=pd.DataFrame.from_records(Z)
df4.columns=["ID", "TT", "TOA", "TOD"]
df4["TT"] = df4['TT'].astype('float')
df4["TOA"] = df4['TOA'].astype('float')
df4["TOD"] = df4['TOD'].astype('float')

#Adjust for UTC and CET/CEST difference
df4["TOA"] = df4["TOA"] + time_diff
df4["TOD"] = df4["TOD"] + time_diff
Z1=remove_outliers_TOD(df4)


# %%Classify trucks
Y=classify_trucks_v2(Z1,2)

# %%Extract trucks
Y["DATE"]=whichDate
Y["Seg"]=Path
truck=Y[(Y.cluster==0)]
# | (Y.cluster==3)| (Y.cluster==4)
#truck=Y[Y['cluster']==1]


plt.plot(Z1['TOD'],Z1['TT'],'.')
plt.plot(truck['TOD'],truck['TT'],'.', color='r', markersize=3)

# %%Save the variable
truck.to_pickle(Masterpath + 'Recursive_logit/ODP/'+Path+'/' + whichDate+".pkl")

print("--- %s seconds ---" % (time.time() - start_time))
