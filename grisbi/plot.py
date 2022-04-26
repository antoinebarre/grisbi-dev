# utilits
import pandas as pd
import numpy as np
import os
import pandas_datareader.data as web
from grisbi import parameter, stocks
import datetime

import yfinance as yf


def plot_stock(ticker:str,dataFolder:str = parameter.defaultFolder,
        startDate:datetime.datetime =parameter.default_startDate,endDate:datetime.datetime=parameter.default_endDate):

    import cufflinks as cf
    import plotly.express as px
    import plotly.graph_objects as go

    #read stock information
    df = stocks.get_values_from_csv(ticker=ticker,dataFolder = dataFolder)
    df.tail()

    if not df.empty:
        # select the appropriate time range
    
        df=df.loc[startDate.strftime("%Y-%m-%d") : endDate.strftime("%Y-%m-%d"),:]

              
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close']))
        fig.update_yaxes(title="Stock Price")
        fig.show()
