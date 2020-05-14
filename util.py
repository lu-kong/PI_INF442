import platform
import pandas as pd


# DATABASE_PATH = 'E:/PI_INF442/p1-power-weather/'

if platform.node() == 'DESKTOP-QGJFK60': #PC of LULU
    DATABASE_PATH = 'C:/Users/lu/Desktop/PI/p1-power-weather/'
elif platform.node() == 'DESKTOP-KDOM9K4': #PC of JIAJIA
    DATABASE_PATH = 'E:/PI_INF442/p1-power-weather/'
    
def load_data(dt = 'w', name = '200701',mode = 'load'):
#     print(DATABASE_PATH)
    w_names = ['date','time','g_active_power','g_reactive_power','voltage','global_intensity','sub_1_kitchen','sub_2_laundry','sub_3_wh_ac']
    if(mode!='load' or dt not in ('w','p')):
        print('++++++++++++++++++++++++++++++++++++++\n            help mode\n++++++++++++++++++++++++++++++++++++++')
        print('dt means database type which can be choose from:\n','    '.join(('w','p')))
        print('\n For w, which means weather, name can be chose from 200701 to 201012\n For p, which means power, name can be chose from 2007 - 2010')
        print('Example of Usage:\n load_data()\n load_data(mode=\'load\',dt=\'p\',name = 2007)')
    else:
        if(dt=='w'): 
            PATH = DATABASE_PATH +  'weather/synop.' + str(name)+'.csv'
            return pd.read_csv(PATH,';', low_memory = False)
#        PATH = DATABASE_PATH + (dt == 'w')? 'weather/synop.': 'household_power_consumption/household_power_consumption_'
        else: 
            PATH = DATABASE_PATH + 'household_power_consumption/household_power_consumption_' + str(name)+'.csv'
            names = w_names
            return pd.read_csv(PATH,';',names=names, low_memory = False)
        
def time_rescale(df,timescale = '3H',how='any',mode = 'mean'):
    """
    parameters:
    -----------------------------------------
    df       : Dataframe (support only data of power_consumption for instance)
    timescae : Time scale to change to, chosen generally from 'XT','XH','XD'...X is a number to be chosen
    how      : usuel for dropping unfilled rows  how = 'any' by default
    mode     : mode to rescale, choosen from ('mean','max','sum')
    return:
    -----------------------------------------
    df cleaned and rescaled indexed by 'full_time'
    """
    assert mode in ('mean','sum','max') ,"mode is to be choosen from ('mean','max','sum')"
    
    print('Processe begin...\n')
    df_comb = df.copy()
    print('Begin configuring datetime line ...',end='')
    df_comb['full_time'] = df_comb['date']+' '+ df_comb['time']
    df_comb['full_time'] = pd.to_datetime(df_comb['full_time'])
    print('done')
    print('Begin dropping bug data ...',end='')
    df_dropped = df_comb.dropna(how = how)
    print(' done')
    df_dropped.iloc[:,2:-1] = df_dropped.iloc[:,2:-1].apply(pd.to_numeric)
    if(mode == 'sum'):
        res = df_dropped.iloc[:,2:].resample(timescale,on = 'full_time').sum()
    if(mode == 'mean'):
        res = df_dropped.iloc[:,2:].resample(timescale,on = 'full_time').mean()
    if(mode == 'max'):
        res = df_dropped.iloc[:,2:].resample(timescale,on = 'full_time').max()
    print('done\n')
    return res