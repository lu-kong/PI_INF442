#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from util import *
from scipy import stats  #compute z-score
import numpy as np

# ---------------------------------------------Power Data Cleaning-------------------------------------------------------------------------

### detecte outliers with a set threshold, usually 3 by default. 
def detect_outlier(data, threshold = 3):
    z = stats.zscore(data, nan_policy = 'omit')
    return np.where(np.abs(z)>threshold)  

### delete the outliers of a DataFrame after detection
def delete_outlier(data, threshold = 3):
    arr = detect_outlier(data, threshold = threshold)
    data.drop(data.index[arr], inplace = True)
    return data

### Interpolate the missing values and output a cleaned power data set
def power_clean(year = 2007):
    df = load_data(dt = 'p', name = year)
    for c in df.columns[2:]:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df[c] = delete_outlier(df[c])
    df.interpolate(method = 'linear', limit_direction='forward', inplace = True)
    df.interpolate(method = 'linear', limit_direction='backward', inplace = True)
    return df  



# -------------------------------------------Weather Data Cleaning-----------------------------------------------

### Since we need only the weather data concerning the households in Sceaux, we extracte the weather data of the Meteo station Orly with its code 7149
def abstract_data(code = 7149):
    df = pd.DataFrame(columns = ['date','time', 'numer_sta', 'pmer', 'tend', 'dd', 'ff', 't', 'td',
       'u', 'vv', 'n', 'nbas', 'hbas', 'pres', 'niv_bar', 'geop', 'tend24', 'tn12', 'tn24', 'tx12', 'tx24',
       'tminsol', 'tw', 'raf10', 'rafper', 'per', 'ht_neige',
       'ssfrai', 'perssfrai', 'rr1', 'rr3', 'rr6', 'rr12', 'rr24', 'nnuage1', 'hnuage1',
       'nnuage2', 'hnuage2', 'nnuage3', 'hnuage3',
       'nnuage4', 'hnuage4'])
    for i in range(4):
        for j in range(12):
            name = str(200701 + i*100 + j)
            df_tmp = load_data(dt = 'w', name = name)
            df_tmp.replace(['mq'],np.NaN, inplace=True)
            del_col = ['cod_tend', 'ww', 'w1', 'w2', 'cl', 'cm', 'ch', 'sw','etat_sol', 'phenspe1', 'phenspe2', 'phenspe3', 'phenspe4',
                       'ctype1', 'ctype2','ctype3', 'ctype4']
            df_tmp.drop(columns = del_col, inplace = True)
            df_tmp = df_tmp.loc[df_tmp['numer_sta']== code]
            df_tmp = df_tmp.iloc[:,:-1]
            fulltime = df_tmp['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d%H%M%S'))
            df_tmp.drop(columns = ['date'], inplace = True)
            df_tmp['date'] = fulltime.dt.date
            df_tmp['time'] = fulltime.dt.time
            df = pd.concat([df, df_tmp])
    df.reset_index(drop = True, inplace = True)
    return df

def weather_clean():
    df = abstract_data()
#     df.replace(['mq'],np.NaN, inplace=True)
    for col in df.columns[2:]:
        if(df[col].isna().sum()>5000):
            df.drop(columns = col, inplace = True)
        else:
            df[col] = delete_outlier(pd.to_numeric(df[col]))
    df.interpolate(method = 'linear', limit_direction='forward', inplace = True)
    df.interpolate(method = 'linear', limit_direction='backward', inplace = True)
    return df
    
            