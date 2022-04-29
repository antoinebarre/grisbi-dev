"""Module Grisbi de gestion des actions et de leurs analyses"""

#module à utiliser
import pandas as pd
import numpy as np
import os
import pandas_datareader.data as web
import yfinance as yf
import datetime as dt

# CONSTANTES
# - Dates :
referencePeriod     = "5Y"
referenceInterval   = "1d"

default_startDate   =  dt.datetime(2019, 1, 1)
default_endDate     =  dt.date.today()

# - Repertoire
defaultDataFolder       = os.path.join(os.getcwd(),"data")
defaultListFolder       = os.path.join(os.getcwd(),"list")


###################################################################################
# FUNCTIONS D4IMPORT EXPORT
def get_data_from_Yahoo(ticker:str,
                    dataFolder:str = defaultDataFolder,
                    period:str=referencePeriod,interval:str = referenceInterval):
    """enregistre les données depuis Yahoo Finance a partir d'un ticker

    Args:
        ticker (str): ticker de l'action a enregistrer
        dataFolder (str, optional): chemin (absolu ou relative) des fichiers csv de données. Defaults to defaultDataFolder.
        period (str, optional): durée de l'enregistrement. Defaults to referencePeriod.
        interval (str, optional): fréquence de l'enregistrement. Defaults to referenceInterval.

    Raises:
        Exception: _description_
    """
    try:
        stock   = yf.Ticker(ticker)
        data    = stock.history(period=period, interval=interval)

        #suppression des mauvaises colonnes
        data.drop(["Dividends","Stock Splits"], axis=1, inplace=True)

        if data.empty:
            raise Exception
            # TODO: analyser le principe d'exception
    except:
            print(f"WARNING - le ticker {ticker} est inconnu pour Yahoo Finance")
            return 
    else:
        
        # create an absolute path
        dataFolder = os.path.abspath(dataFolder)

        #creation du dossier de sauvegarde
        os.makedirs(dataFolder,  exist_ok = True)

        #creer le fichier contenant les infos
        dataFile = os.path.join(dataFolder,ticker+".csv")
        data.to_csv(dataFile)

        return

def read_listStocks(listFolder:str = defaultListFolder):
    #collecter la liste des tickers
    listfiles = [f for f in os.listdir(listFolder) 
                if os.path.isfile(os.path.join(listFolder, f)) and 
                os.path.splitext(f)[-1] ==".csv"]
    
    #charger la liste des tickers
    listStocks = pd.DataFrame()

    for listfile in listfiles:
        #fichier a lire
        file2read = os.path.join(listFolder,listfile)
        listStocks = pd.concat([listStocks,pd.read_csv(file2read)],ignore_index=True)

    return listStocks


def update_stockData(listFolder:str = defaultListFolder,
                    dataFolder:str = defaultDataFolder,
                    period:str=referencePeriod,interval:str = referenceInterval,
                    maxTicker:int = -1  ):

    #collecter la liste des tickers
    listStocks = read_listStocks(listFolder= listFolder)
    
    listStocks = listStocks.iloc[0:maxTicker,:]

    for ticker in listStocks["symbol"]:
        print(f">>> mise a jour du ticker {ticker}")
        get_data_from_Yahoo(ticker=ticker,dataFolder=dataFolder,
                            period=period,interval=interval)
    
    return


def load_data_from_csv(ticker:str,
                    dataFolder:str = defaultDataFolder):
    #create an absolute path
    dataFile = os.path.abspath(os.path.join(dataFolder,ticker + ".csv"))

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


###################################################################################
# FONCTION DE CARACTERISTIQUES

def get_stockName(ticker:str,
                    listFolder:str = defaultListFolder)->str:
    """renvoie le nom de l'action en fonction de son ticker

    Args:
        ticker (str): ticker de l'action
        listFolder (str, optional): chemin du repertoire de liste (absolu ou relatif). Defaults to defaultListFolder.

    Returns:
        str: nom de l'action
    """
    
    # cas 1 : le ticker est présent dans les listes de tickers

    try:
        listStocks = read_listStocks(listFolder= listFolder)  
        name = listStocks.loc[listStocks['symbol']==ticker,"longName"].item()

        return name
    except:
        print(f"WARNING - ticker absent des listes :{ticker}")

        stock = yf.Ticker(ticker)
   
        try :
            return stock.info['longName']
        except:
            print(f"WARNING - ticker absent de Yahoo Finance :{ticker}")
            return ''

class stock:
    "objet stock permet de collecter et manipuler les données associées à un ticker de Yahoo FInance"

    # Property
    data        = None
    name        = None
    currency    = None
    ticker      = None
    period      = referencePeriod
    interval    = referenceInterval    
    data        = None
    __isValid   = False
    __isData    = False

###################################################################################
    # CONSTRUCTOR
    def __init__(self,ticker:str,listFolder:str = defaultListFolder):
        self.ticker     = ticker

        # collecter les données
        self.data       = load_data_from_csv(ticker)

        if self.data.empty:
            print(f"WARNING - ticker invalide :{ticker}")
            return
        else:
            self.__isValid=True

            #chercher le nom
            try:
                listStocks = read_listStocks(listFolder= listFolder)  
                self.name = listStocks.loc[listStocks['symbol']==ticker,"longName"].item()
            except:
                print(f"WARNING - ticker absent des listes :{ticker}")
                return
        return
            
        
        

###################################################################################
    # METHODE SURCHARGEES    

    def __str__(self)-> str:
        """Surcharge de la methode print

        Returns:
            str: message a afficher
        """

        str4stock = "STOCK INFORMATION :\n"\
                    f" - Ticker   : {self.ticker}\n"\
                    f" - Nom      : {self.name}\n"\
                    f" - Currency : {self.currency}\n"\
                    f" - Valid    : {self.__isValid}\n"\
                    f" - Period   : {self.period}\n"\
                    f" - Frequency: {self.interval}\n"
        return str4stock

###################################################################################
    # METHODES
    






