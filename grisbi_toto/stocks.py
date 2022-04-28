# utilits
import pandas as pd
import numpy as np
import os
import pandas_datareader.data as web
from grisbi import parameter
import yfinance as yf



def save_value(ticker:str,
            dataFolder:str = parameter.defaultFolder ) -> pd.core.frame.DataFrame:
    """save the daily data of the stock nammed by the tickers and create a csv files

    Args:
        ticker (str): tickers of the stock
        dataFolder (str, optional): absolute path where the data are saved. Defaults to parameter.defaultFolder.

    Returns:
        pd.core.frame.DataFrame: dataFrame with the stock evolution
    """

    print(">> Download for the ticker: " + ticker)
 
    df = yf.download(tickers=ticker, period='max', interval='1d')

    # create an absolute path
    dataFolder = os.path.abspath(dataFolder)

    #creation du dossier de sauvegarde
    os.makedirs(dataFolder,  exist_ok = True)

    #creer le fichier contenant les infos
    dataFile = os.path.join(dataFolder,ticker+".csv")
    df.to_csv(dataFile)
    
    return df

def get_values_from_csv(ticker:str,dataFolder:str = parameter.defaultFolder ) -> pd.core.frame.DataFrame:
    """read a csv file generated by grisbi to transform to dataframe

    Args:
        ticker (str): stock ticker
        dataFolder (str, optional): path of the data file folder. Defaults to parameter.defaultFolder.

    Returns:
        pd.core.frame.DataFrame: read data frame. Empty if there is an error.
    """
    
    print(">> read csv for ticker: " + ticker)

    #create an absolute path
    dataFile = os.path.abspath(os.path.join(dataFolder,ticker+".csv"))

    # Try to get the file and if it doesn't exist issue a warning
    try:
        df = pd.read_csv(dataFile)
        # change index to datetime
        df = df.set_index('Date')
        df = df.set_index(pd.to_datetime(df.index))
        
    except FileNotFoundError:
        print(f"WARNING - File <{dataFile}> doesn't exist")
        return pd.DataFrame()
    else:
        return df

def get_stockName(ticker:str)->str:
    """get the name of stock associated to the ticker

    Args:
        ticker (str): ticker of the stock

    Returns:
        str: long name of the stock associated to the ticker
    """
    
    # Use yahoo finance API to collect the stock name
    stock = yf.Ticker(ticker)
   
    try :
        return stock.info['longName']
    except:
        return ''

def get_stockCurrency(ticker:str)->str:
    """get the stock currency

    Args:
        ticker (str): stock's tickers

    Returns:
        str: currency of the stock associated to the ticker
    """
        
    # Use yahoo finance API to collect the stock currency
    stock = yf.Ticker(ticker)

    try :
        return stock.info['currency']
    except:
        return ''




    
