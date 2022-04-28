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
defaultFolder       = os.path.join(os.getcwd(),"data")




class stock:
    "objet stock permet de collecter et manipuler les données associées à un ticker de Yahoo FInance"

    # Property
    data        = None
    name        = None
    currency    = None
    ticker      = None
    period      = None
    interval    = None    
    data        = None
    __isValid   = False
    __isData    = False

###################################################################################
    # CONSTRUCTOR
    def __init__(self,ticker:str):
            self.ticker     = ticker
        

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
    def get_data_from_Yahoo(self,period:str=referencePeriod,interval:str = referenceInterval):
        """_summary_

        Args:
            period (str, optional): duree de recuperation. Defaults to referencePeriod.
            interval (str, optional): frequence de recuperation. Defaults to referenceInterval.
        """

        # collecter les infos sur le ticker
        try:
            stock   = yf.Ticker(self.ticker)
            data    = stock.history(period=period, interval=interval)

            #suppression des mauvaises colonnes
            data.drop(["Dividends","Stock Splits"], axis=1, inplace=True)

            if data.empty:
                raise Exception
        except:
            print(f"WARNING - le ticker {self.ticker} est inconnu pour Yahoo Finance")
            return
        else:
            # allouer les metadata de l'action
            self.data       = data
            self.__isValid  = True
            self.__isData   = True
            self.name       = stock.info['longName']
            self.currency   = stock.info['currency']
            self.period     = period
            self.interval   = interval
        return

    def save_data(self,dataFolder:str = defaultFolder ):
        """_summary_

        Args:
            dataFolder (str, optional): chemin absolu ou relatif. Defaults to defaultFolder.
        """

        # create an absolute path
        dataFolder = os.path.abspath(dataFolder)

        #creation du dossier de sauvegarde
        os.makedirs(dataFolder,  exist_ok = True)

        #creer le fichier contenant les infos
        dataFile = os.path.join(dataFolder,self.ticker+".csv")
        self.data.to_csv(dataFile)
        return

    def get_values_from_csv(self,dataFolder:str = defaultFolder):
        
        #create an absolute path
        dataFile = os.path.abspath(os.path.join(dataFolder,self.ticker + ".csv"))

        # Try to get the file and if it doesn't exist issue a warning
        try:
            df = pd.read_csv(dataFile)
            # change index to datetime
            df = df.set_index('Date')
            df = df.set_index(pd.to_datetime(df.index))
            
        except FileNotFoundError:
            print(f"WARNING - File <{dataFile}> doesn't exist")
            self.__isData   = False
            self.data       = None

            # TODO: verifier la periode et la frequence pour mettre a jour l'object
        else:
            self.__isData   = True
            self.data       = df






