# -*- coding: utf-8 -*-

"""
Created on Tue Jun 26 16:53:04 2018

@author: salilsharma
"""

def contains(small, big):
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i
            #return i, i+len(small)
    return False

def travel_time_data(aa,Points,query_string,pd,traveltime):
    bb=aa.sort_values(by=['dateTime'])
    bb1= bb[bb['locationId'].diff(-1).ne(0)].query(query_string)
    bb2= bb[bb['locationId'].diff().ne(0)].query(query_string)
    frames=[bb1,bb2]
    result = pd.concat(frames)
    sorted=result.sort_values(by=['dateTime'])
    A=sorted['locationId'].tolist()
    if len(Points)<=2:
        B=[Points[0],Points[0],Points[1],Points[1]]
    else:
        B=[Points[0],Points[0],Points[1],Points[1],Points[2],Points[2]]
    start_point=contains(B,A)

    if type(start_point) != bool:
        if len(Points)<=2:
            needed=sorted.iloc[start_point:start_point+4]
            TT=needed.iloc[2]['dateTime']-needed.iloc[1]['dateTime']
            traveltime.append([needed.iloc[2]['level_0'],TT, needed.iloc[1]['dateTime'], needed.iloc[2]['dateTime']])
        else:
            needed=sorted.iloc[start_point:start_point+6]
            TT=needed.iloc[4]['dateTime']-needed.iloc[1]['dateTime']
            traveltime.append([needed.iloc[4]['level_0'],TT, needed.iloc[1]['dateTime'], needed.iloc[4]['dateTime']])
    return traveltime


def travel_time_list(aa,Points,query_string,pd,traveltime):
    bb=aa.sort_values(by=['dateTime'])
    bb1= bb[bb['locationId'].diff(-1).ne(0)].query(query_string)
    bb2= bb[bb['locationId'].diff().ne(0)].query(query_string)
    frames=[bb1,bb2]
    result = pd.concat(frames)
    sorted=result.sort_values(by=['dateTime'])
    A=sorted['locationId'].tolist()
    if len(Points)<=2:
        B=[Points[0],Points[0],Points[1],Points[1]]
    else:
        B=[Points[0],Points[0],Points[1],Points[1],Points[2],Points[2]]
    start_point=contains(B,A)

    if type(start_point) != bool:
        if len(Points)<=2:
            needed=sorted.iloc[start_point:start_point+4]
            TT=needed.iloc[2]['dateTime']-needed.iloc[1]['dateTime']
            traveltime.append([needed.iloc[2]['level_0'],TT, needed.iloc[2]['dateTime']])
        else:
            needed=sorted.iloc[start_point:start_point+6]
            TT=needed.iloc[4]['dateTime']-needed.iloc[1]['dateTime']
            traveltime.append([needed.iloc[4]['level_0'],TT, needed.iloc[4]['dateTime']])
    return traveltime


def upload_data(filename,json):
    with open(filename,'r') as f:
        data = json.load(f)
    return data

def make_query(Points):
    if len(Points)<=2:
        query_string="locationId in " + "[" + str(Points[0]) + "," + str(Points[1]) + "]"
    else:
        query_string="locationId in " + "[" + str(Points[0]) + "," + str(Points[1]) + "," + str(Points[2]) + "]"
    return query_string

def make_search_list(Points):
    if len(Points)<=2:
        search_list={Points[0],Points[1]}
    else:
        search_list={Points[0],Points[1],Points[2]}
    return search_list

def generate_plot(travel_time, Points,plt, whichDate, uppercut):
    plt.figure()
    for j in range(0, len(travel_time)):
        if (travel_time[j][1].seconds)/60 <=uppercut:
            trtime=(travel_time[j][3].hour*60+travel_time[j][3].minute+travel_time[j][3].second/60)
            plt.plot(trtime, (travel_time[j][1].seconds)/60, marker='.', color='r', markersize=3)
    plt.show()
    plt.xlabel('Time of day (in minutes)')
    plt.ylabel('Travel time (in minutes)')
    if len(Points)>2:
        plt.title('BT observations on ' + whichDate + '-2017' + ' from ' + str(Points[0]) +' to ' + str(Points[2]) + ' via ' + str(Points[1]))
    else:
        plt.title('BT observations on ' + whichDate + '-2017' + ' from ' + str(Points[0]) +' to ' + str(Points[1]))

def outliers_iqr_dataframe(Z):
    Q1 = Z['TT'].quantile(0.25)
    Q3 = Z['TT'].quantile(0.75)
    IQR = Q3 - Q1
    filtered = Z.query('(@Q1 - 1.5 * @IQR) <= TT <= (@Q3 + 1.5 * @IQR)')
    return filtered
    
def remove_outliers_TOD(Z):
    import pandas as pd
    RP=Z[Z['TOD']<390]
    MP=Z[(Z.TOD>=390) & (Z.TOD<570)]
    AP=Z[(Z.TOD>=570) & (Z.TOD<960)]
    EP=Z[(Z.TOD>=960) & (Z.TOD<1140)]
    LP=Z[Z['TOD']>=1140]
    
    RP1=outliers_iqr_dataframe(RP)
    MP1=outliers_iqr_dataframe(MP)
    AP1=outliers_iqr_dataframe(AP)
    EP1=outliers_iqr_dataframe(EP)
    LP1=outliers_iqr_dataframe(LP)
    
    frames=[RP1,MP1,AP1,EP1,LP1]
    result = pd.concat(frames)
    return result


def extract_trucks_highlowpass(Z, Path, BT):
    import pandas as pd
    if Path==1:
        Z1=Z[(Z.TT>=(27.6*60/80)) & (Z.TT<=BT)]    
    else:
        Z1=Z[(Z.TT>=(23.2*60/80)) & (Z.TT<=BT)] 
    
    return Z1

def extract_trucks_highpass(Z, filter):
    import pandas as pd
    Z1=Z[Z['TT']>=(filter)]    
    return Z1

def buffer_time_route(Z):
    import numpy as np
    import pandas as pd
    RP=Z[Z['TOD']<390]
    MP=Z[(Z.TOD>=390) & (Z.TOD<570)]
    AP=Z[(Z.TOD>=570) & (Z.TOD<960)]
    EP=Z[(Z.TOD>=960) & (Z.TOD<1140)]
    LP=Z[Z['TOD']>=1140]

    RP1=outliers_iqr_dataframe(RP)
    MP1=outliers_iqr_dataframe(MP)
    AP1=outliers_iqr_dataframe(AP)
    EP1=outliers_iqr_dataframe(EP)
    LP1=outliers_iqr_dataframe(LP)
    
    RP2=pd.concat([RP1,LP1])
    B1=np.percentile(RP2['TT'],95)-np.mean(RP2['TT'])
    B2=np.percentile(MP1['TT'],95)-np.mean(MP1['TT'])
    B3=np.percentile(AP1['TT'],95)-np.mean(AP1['TT'])
    B4=np.percentile(EP1['TT'],95)-np.mean(EP1['TT'])
    #B5=np.percentile(LP1[:,1],95)-np.mean(LP1[:,1])
    
    BT=[]
    BT=[B2, np.mean(MP1['TT']), B3, np.mean(AP1['TT']), B4, np.mean(EP1['TT']),B1,np.mean(RP2['TT'])]
    #Z1=np.vstack([RP1,MP1,AP1,EP1,LP1])
    return BT