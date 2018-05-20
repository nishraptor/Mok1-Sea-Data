import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import urllib.request, json
from datetime import datetime, date, time
from ipywidgets import widgets  
from IPython import get_ipython
from matplotlib import pylab
from pylab import *
from IPython.display import clear_output


def plotTimeSeriesData(data,col_name_to_plot,graphKeyVals):
    #Sets the size of the figure in the notebook

    for i in range(len(data)):
        plt.plot(data[i]['date_time'],data[i][col_name_to_plot], label = str(graphKeyVals[i]))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

        #fontsize of the tick labels
        plt.rc('xtick', labelsize=15) 
        plt.rc('ytick', labelsize = 15)

        #Size of ticks
        plt.tick_params(direction='out', length=10, width=2,)

        #X and Y labels
        plt.xlabel('Time',fontsize=18)
        plt.ylabel(col_name_to_plot,fontsize=18)


    plt.legend(loc = "best",prop={'size': 20})
    plt.show()
    
        
def simplify_column_names(df):
    new_header = []
    for i in (list(df.columns.values)):
        if len(i) == 1:
            new_header.append(i[0])
        elif len(i) == 2:
            new_header.append('%s (%s)'%(i[0],i[1]))
    df.columns = new_header
    return df

#Creates a datetime object based on the dates and times and appends to the existing dataframe

#function to streamline the operation
def createDateTime(df):
    df_temp = df[['#YY (#yr)', 'MM (mo)','DD (dy)','hh (hr)','mm (mn)']].copy()
    df_temp.columns = ['year', 'month', 'day', 'hour', 'minute']
    df_temp = pd.to_datetime(df_temp)

    df_temp = pd.DataFrame({'date_time': df_temp})
    df = pd.concat([df,df_temp], axis = 1)
    return df


def create_data(cinergi_url):
    url_data = []

    with urllib.request.urlopen(cinergi_url) as url:
        data = json.loads(url.read().decode())
        data = data["_source"]["links_s"]
        if isinstance(data,str):    
            url_data.append(pd.read_csv(data, delim_whitespace=True, header=[0,1], na_values=['99.0','999.0','99.00','999','9999.0' ]))
        else:
            for i in data:
                url_data.append(pd.read_csv(i, delim_whitespace=True, header=[0,1], na_values=['99.0','999.0','99.00','999','9999.0' ]))

            # Preview Data from Cinergi URL
    return url_data

#Generates table of number of variables in each column name
def create_dropdowns(data):
    widgetData = []
    for i in data:
        display(("%s 's data (number of variables in each column)"%(i["#YY (#yr)"][0])),pd.DataFrame(i.count()).transpose().style)
        widgetData.append(pd.DataFrame(i.count()).transpose())

    dropdown_options = widgetData[0].columns.values
    dropdown_options = dropdown_options.tolist()

    #Generate Dropdown Options (Get all column names where sum of useable values is not 0)
    for i in widgetData:
        dropdown_options = list(set(dropdown_options)&set((i.T[i.any()].T).columns.values))
    dropdown_options = [x for x in dropdown_options if x not in ["hh (hr)", "mm (mn)", "#YY (#yr)","DD (dy)","date_time","MM (mo)"]]
    return dropdown_options