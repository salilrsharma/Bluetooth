# -*- coding: utf-8 -*-

"""
Created on Tue Jun 26 16:53:04 2018

@author: salilsharma
"""

def classify_trucks(X,n_clusters):
    from sklearn.mixture import GaussianMixture as GMM
    G=X[:,2]
    #Y = np.reshape(G, [len(G), 1])
    Y=G.values.reshape(-1,1)
    gmm = GMM(n_components=n_clusters,max_iter=100).fit(Y)
    labels=gmm.predict(Y)
    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = X[:,0]
    cluster_map['TOD'] = X[:,1]
    cluster_map['traveltime'] = X[:,2]
    cluster_map['cluster'] = labels
    cluster_map['TOD']=cluster_map['TOD'].apply(pd.to_numeric)
    cluster_map['traveltime']=cluster_map['traveltime'].apply(pd.to_numeric)
    LABEL_COLOR_MAP = {0 : 'r',
                   1 : 'b',
                   }
    label_color = [LABEL_COLOR_MAP[l] for l in labels]
    print(gmm.means_)
    plt.scatter(cluster_map['TOD'], cluster_map['traveltime'], c=label_color, s=3);
    return cluster_map

def classify_trucks_v2(Z,n_clusters):
    from sklearn.mixture import GaussianMixture as GMM
    import numpy as np
    import matplotlib.pyplot as plt
    G=Z['TT']
    #Y = np.reshape(G, [len(G), 1])
    Y=G.values.reshape(-1,1)
    gmm = GMM(n_components=n_clusters,max_iter=100).fit(Y)
    labels=gmm.predict(Y)
    Z['cluster'] = labels
    print(gmm.means_)
    plt.scatter(Z['TOD'], Z['TT'], c=Z['cluster'], s=3);
    return Z


def generate_bluetooth_data(traveltime,uppercut):
    import numpy as np
    X1=[];
    X2=[];
    X3=[];
    index=[];
    for j in range(0, len(traveltime)):
        if (traveltime[j][1].seconds)/60 <=uppercut:
            index.append(traveltime[j][0])
            X2.append(traveltime[j][2].hour*60+traveltime[j][2].minute+traveltime[j][2].second/60)
            X3.append(traveltime[j][3].hour*60+traveltime[j][3].minute+traveltime[j][3].second/60)
            X1.append((traveltime[j][1].seconds)/60)
    X1=np.array(X1)
    index=np.array(index)
    X2=np.array(X2)
    X3=np.array(X3)
    return np.column_stack([index,X1,X2,X3])
    #return np.column_stack([X1,X2])


def generate_data(traveltime,uppercut):
    import numpy as np
    X1=[];
    X2=[];
    #index=[];
    for j in range(0, len(traveltime)):
        if (traveltime[j][1].seconds)/60 <=uppercut:
            #index.append(traveltime[j][0])
            X1.append(traveltime[j][2].hour*60+traveltime[j][2].minute+traveltime[j][2].second/60)
            X2.append((traveltime[j][1].seconds)/60)
    X1=np.array(X1)
    #index=np.array(index)
    X2=np.array(X2)
    #return np.column_stack([index,X1,X2])
    return np.column_stack([X1,X2])

def outliers_iqr(ys):
    import numpy as np
    quartile_1, quartile_3 = np.percentile(ys[:,1], [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return ys[np.logical_and(ys[:,1] <= upper_bound, ys[:,1] >= lower_bound)]

def outliers_removal(Z):
    import numpy as np
    RP=Z[Z[:,0]<390]
    MP=Z[np.logical_and(Z[:,0]>=390,Z[:,0]<570)]
    AP=Z[np.logical_and(Z[:,0]>=570,Z[:,0]<960)]
    EP=Z[np.logical_and(Z[:,0]>=960,Z[:,0]<1140)]
    LP=Z[Z[:,0]>=1140]

    RP1=outliers_iqr(RP)
    MP1=outliers_iqr(MP)
    AP1=outliers_iqr(AP)
    EP1=outliers_iqr(EP)
    LP1=outliers_iqr(LP)
      
    Z1=np.vstack([RP1,MP1,AP1,EP1,LP1])
    return Z1

def buffer_time(Z):
    import numpy as np
    RP=Z[Z[:,0]<390-20]
    MP=Z[np.logical_and(Z[:,0]>=390-20,Z[:,0]<570-20)]
    AP=Z[np.logical_and(Z[:,0]>=570-20,Z[:,0]<960-20)]
    EP=Z[np.logical_and(Z[:,0]>=960-20,Z[:,0]<1140-20)]
    LP=Z[Z[:,0]>=1140-20]

    RP1=outliers_iqr(RP)
    MP1=outliers_iqr(MP)
    AP1=outliers_iqr(AP)
    EP1=outliers_iqr(EP)
    LP1=outliers_iqr(LP)
    
    B1=np.percentile(RP1[:,1],95)-np.mean(RP1[:,1])
    B2=np.percentile(MP1[:,1],95)-np.mean(MP1[:,1])
    B3=np.percentile(AP1[:,1],95)-np.mean(AP1[:,1])
    B4=np.percentile(EP1[:,1],95)-np.mean(EP1[:,1])
    B5=np.percentile(LP1[:,1],95)-np.mean(LP1[:,1])
    
    C1=np.percentile(RP1[:,1],95)
    C2=np.percentile(MP1[:,1],95)
    C3=np.percentile(AP1[:,1],95)
    C4=np.percentile(EP1[:,1],95)
    C5=np.percentile(LP1[:,1],95)
    
    BT=[]
    BT=[B1,C1,B2,C2,B3,C3,B4,C4,B5,C5]
    #Z1=np.vstack([RP1,MP1,AP1,EP1,LP1])
    return BT




