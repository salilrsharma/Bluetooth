# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:50:38 2019

@author: salilsharma
"""

# %%Data collection for a 3-point trajectory
# Pre-step before creating a masterlist

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

#Seg 1: 507 and 508
#Seg 2: 524 and 508

Points=[510,511,508]
Path='3-1_1'

#time_diff=120
#whichDate=['10-02','10-03','10-04','10-06','10-09','10-10','10-11','10-12','10-13','10-16','10-17','10-18','10-19','10-20','10-23','10-24','10-25','10-26','10-27']

time_diff = 60
whichDate=['10-30','10-31','11-01','11-02','11-03','11-06','11-07','11-08','11-09','11-10','11-13','11-14','11-15','11-16','11-17','11-20','11-21','11-22','11-23','11-24']


Masterpath='xxx'

for datelist in range(0,len(whichDate)):

    filename=Masterpath+ 'Data/' +  whichDate[datelist] + '.json'
    data=upload_data(filename,json)
        
    if 'error' in data:
        continue
    else:
        detection=data['detections'];
        
        # len(v) >=9 to ensure that macID has at least 3 registrations at all three bluetooth station.
        df=pd.concat({k: pd.DataFrame(v) for k, v in detection.items()if len(v) >= 9 })
        
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
                
        #generate_plot(travel_time, Points,plt, whichDate, 120)
        
        Z=generate_bluetooth_data(travel_time,200)
        
        df4=pd.DataFrame.from_records(Z)
        df4.columns=["ID", "TT", "TOA", "TOD"]
        df4["TT"] = df4['TT'].astype('float')
        df4["TOA"] = df4['TOA'].astype('float')
        df4["TOD"] = df4['TOD'].astype('float')
        
        #Adjust for UTC and CET/CEST difference
        df4["TOA"] = df4["TOA"] + time_diff
        df4["TOD"] = df4["TOD"] + time_diff
        df4["DATE"]=whichDate[datelist]
        df4["Seg"]=Path
        
        df4.to_pickle(Masterpath + 'Recursive_logit/ODP/'+Path+'/' + whichDate[datelist]+".pkl")
            
        print("--- %s seconds ---" % (time.time() - start_time))
                
        
            
        del Z, aa, data, detection, df, df2, df3, df4, i, query_string, travel_time