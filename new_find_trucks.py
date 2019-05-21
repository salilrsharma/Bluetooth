#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 11:19:12 2019

@author: salilsharma
"""

#Identify trucks; genrate data for Biogeme

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


Path='2-1_1'
Seg='seg1'
filter = 54.6
   
Masterpath='xxx'

whichDate=['10-02','10-03','10-04','10-06','10-09','10-10','10-11','10-12','10-13','10-16','10-17','10-18','10-19','10-20','10-23','10-24','10-25','10-26','10-27','10-30','10-31','11-01','11-02','11-03','11-06','11-07','11-08','11-09','11-10','11-13','11-14','11-15','11-16','11-17','11-20','11-21','11-22','11-23','11-24']

# Create an empty pandas dataframe
df1 = pd.DataFrame()

for datelist in range(0,len(whichDate)):
    #Access master list for paths
    
    master_list=pd.read_pickle(Masterpath + 'Recursive_logit/ODP/'+Path+'/' + Path+ "_masterList.pkl")
    a=set(master_list.ID.unique())
    
    #read trucks after running bluetooth.py
    slower_vehicles=pd.read_pickle(Masterpath + 'Recursive_logit/Short_stretch/'+Seg+'/' + whichDate[datelist]+ ".pkl")
    b=set(slower_vehicles.ID.unique())
    
    #Intersection of two sets and find common vehicle IDs
    c=a & b
    
    #Create a dataframe of common vehicle Ids from "slower_vehicles" dataframe and matches date
    df2 = master_list[master_list.ID.isin(c) & master_list['DATE'].str.match(whichDate[datelist])]
    
    Y=extract_trucks_highpass(df2, filter)
    
    plt.plot(Y['TOD'],Y['TT'],'.')
    
    Z1=remove_outliers_TOD(Y)
    plt.plot(Z1['TOD'],Z1['TT'],'.')
    
    df1=pd.concat([df1,Z1])
    #Z1.to_pickle(Masterpath+ 'Recursive_logit/Biogeme_data/'+Path+'/' +whichDate[datelist]+".pkl")
    print("--- %s seconds ---" % (time.time() - start_time))
    
    del Y, Z1, df2, master_list, slower_vehicles
    
Z2=remove_outliers_TOD(df1)
plt.plot(Z2['TOD'],Z2['TT'],'.')

Z2.to_pickle(Masterpath + 'Recursive_logit/Biogeme_data/' + Path+".pkl")