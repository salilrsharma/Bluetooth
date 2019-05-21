# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:00:44 2019

@author: salilsharma
"""

import pandas as pd

df1=pd.read_excel("3_1.xlsx")
df2=pd.read_excel("3_2.xlsx")
df3=pd.read_excel("4_1.xlsx")
df4=pd.read_excel("4_2.xlsx")

frames = [df1, df2, df3, df4]

result = pd.concat(frames)

result.to_excel("7-1-diverse.xlsx")
