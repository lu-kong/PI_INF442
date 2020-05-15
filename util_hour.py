#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

def violin(data, str = 'g_active_power'):
    fig, ax = plt.subplots(figsize = (23,8))
    data['full_time'] = pd.to_datetime(data['full_time'])
    ax = sns.violinplot(x = data['full_time'].dt.hour, y = data[str], color = 'aqua',scale = 'width', data = data)
    ax.set_xlabel('hour')
    ax.set_ylabel(str)
    plt.show()

def test_seperate_year(str = 'g_active_power'):
    fig, ax = plt.subplots(figsize = (10,5))
    x = d_2007.index
    ax.plot(x, d_2007[str], 'bo--')
    ax.plot(x, d_2008[str], 'ro--')
    ax.plot(x, d_2009[str], 'go--')
    ax.plot(x, d_2010[str], 'yo--')
    ax.legend(['2007', '2008', '2009', '2010'])
    ax.set_xlabel('hour in a day')
    ax.set_ylabel(str)
    plt.title(str+'  hourly distribution in a day (during year 2007-2010)')
    plt.show()