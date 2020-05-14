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