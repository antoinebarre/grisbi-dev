# utilits
import pandas as pd
import numpy as np
import os
import pandas_datareader.data as web
from grisbi import parameter, stocks
import datetime
from plotly.subplots import make_subplots
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

        


        df['MA5'] = df['Adj Close'].rolling(5).mean()
        df['MA20'] = df['Adj Close'].rolling(20).mean()

        # Create candlestick plot
        candles = go.Candlestick(x=df.index, 
                                    open=df['Open'], 
                                    high=df['High'],
                                    low=df['Low'], 
                                    close=df['Close'], 
                                    name=ticker)

        
        # Create volume bar chart
        vol = go.Bar(x=df.index, y=df['Volume'], name="Volume",
                    marker=dict(
                        color='blue',
                        line=dict(color='blue', width=3)
                        )
                    )

        # Create figure with secondary y-axis
        fig = make_subplots(rows=2, cols=1, row_heights = [0.7,0.3])

        # Add plots
        fig.add_trace(trace=candles, row=1, col=1)
        fig.add_trace(trace=vol, row=2, col=1)


        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                ),
                type="date"),
            title_text=stocks.get_stockName(ticker)    
        )
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)

        fig.update_yaxes(title_text=f"Value ({stocks.get_stockCurrency(ticker)})", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        fig.update_layout(showlegend=False)
        fig.show()
