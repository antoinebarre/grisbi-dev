"""Module Grisbi de gestion des actions et de leurs analyses"""

#module à utiliser
import pandas as pd
import numpy as np
import os
import pandas_datareader.data as web
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl

# fond blanc pour les figures
mpl.rcParams['figure.facecolor'] = 'white'

# CONSTANTES
# - Dates :
referencePeriod     = "5Y"
referenceInterval   = "1d"

default_startDate   =  dt.datetime(2019, 1, 1)
default_endDate     =  dt.date.today()

# - Repertoire
defaultDataFolder       = os.path.join(os.getcwd(),"data")
defaultListFolder       = os.path.join(os.getcwd(),"list")


# - Elements graphique
defaultFigSize = (16,12)

# classe d'ordre
from enum import IntEnum

class ordre(IntEnum):
    VENTE = -1
    NEUTRE = 0
    ACHAT = 1

class status(IntEnum):
    FREE = 0   
    HOLD = 1



###################################################################################
# FUNCTIONS D'IMPORT EXPORT
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
        #stock   = yf.Ticker(ticker)
        data    = yf.download(ticker,period=period, interval=interval)

        #suppression des mauvaises colonnes
        #data.drop(["Dividends","Stock Splits"], axis=1, inplace=True)

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
    
    try:
        # cas 1 : le ticker est présent dans les listes de tickers
        listStocks = read_listStocks(listFolder= listFolder)  
        name = listStocks.loc[listStocks['symbol']==ticker,"longName"].item()

        return name
    except:
        print(f"WARNING - ticker absent des listes :{ticker}")
        # cas 2 : le ticker est dans Yahoo Finance
        
        stock = yf.Ticker(ticker)
   
        try :
            return stock.info['longName']
        except:
            print(f"WARNING - ticker absent de Yahoo Finance :{ticker}")
            return ''

#######################################################################################
# fonctions de tracage

def plot_stock(df,title:str="",currency:str=""):
    
    #create figure
    fig=plt.figure(figsize=defaultFigSize)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(f"Prix Cloture {currency}")
    

    df['Adj Close'].plot(label = "Close")
    plt.fill_between(df.index,df['High'],df['Low'],alpha=0.2,label='min max par jour')

    plt.grid(True)
    
    plt.legend()
    plt.show()

    return
    

def plot_candlestick(df,title:str="",ticker:str="",currency:str=""):

    import cufflinks as cf
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    init_notebook_mode(connected=True)
    # Use Plotly locally
    cf.go_offline()

    if not df.empty:
              

        df['MA5'] = df['Close'].rolling(5).mean()
        df['MA20'] = df['Close'].rolling(20).mean()

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
            title_text=title    
        )
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)

        fig.update_yaxes(title_text=f"Value ({currency})", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        fig.update_layout(showlegend=False)
        fig.show()


def plot_ichimoku(df1):

    df = df1.copy()

    # Conversion
    hi_val = df['High'].rolling(window=9).max()
    low_val = df['Low'].rolling(window=9).min()
    df['Conversion'] = (hi_val + low_val) / 2
    
    # Baseline
    hi_val2 = df['High'].rolling(window=26).max()
    low_val2 = df['Low'].rolling(window=26).min()
    df['Baseline'] = (hi_val2 + low_val2) / 2
    
    # Spans
    df['SpanA'] = ((df['Conversion'] + df['Baseline']) / 2).shift(26)
    hi_val3 = df['High'].rolling(window=52).max()
    low_val3 = df['Low'].rolling(window=52).min()
    df['SpanB'] = ((hi_val3 + low_val3) / 2).shift(26)
    df['Lagging'] = df['Close'].shift(-26)


    plt.figure(figsize=defaultFigSize)

    df['Adj Close'].plot(label = "Adj Close")

    plt.fill_between(df.index,df['SpanA'],df['SpanB'],
        where = df["SpanA"] >= df['SpanB'], color = 'lightgreen')
    plt.fill_between(df.index,df["SpanA"],df["SpanB"],
        where = df['SpanA'] < df["SpanB"], color = 'lightcoral')
    
    plt.grid(True)
    plt.show()

    #############################################################################
    # STRATEGIES DE LA TORTUE

def strategie_tortue(df_init, jour:int=28):

    df = df_init.copy()

    # calcul des valeurs de conditions
    df["min"] = df["Close"].shift(1).rolling(window = jour).min()
    df["max"] = df["Close"].shift(1).rolling(window = jour).max()

    # parametre de la strategie
    conditions = [df["max"]<df["Close"], # achat
                        df["min"]>df["Close"]] # vente
        
    choices = [ordre.ACHAT,ordre.VENTE]

    # application de la strategie
    df["recommandation"]= np.select(conditions, choices, default=ordre.NEUTRE)

    return df

#####################################################################################
# MODULE DE BACK TEST

def backtest(df_init):

    import math

    df = df_init.copy()
    currentStatus = status.FREE

    action =[]

    wallet = 100000
    #buy and hold
    nb0 = math.floor(wallet/df["Close"].iloc[0])
    reste = wallet - nb0*df["Close"].iloc[0]


    dt = None
    dt = pd.DataFrame(columns = ['Date','position', 'Prix'])

# complete df avec les recommandations
    df = strategie_tortue(df)

    currentWallet = wallet
    nbAction = 0


    for idx in df.index:
        df.loc[idx,"amount0"] = reste+nb0*df.loc[idx,"Close"]

        #Traitement signal en ACHAT
        if df.loc[idx,"recommandation"]==ordre.ACHAT and currentStatus==status.FREE:
            action.append(ordre.ACHAT)
            currentStatus = status.HOLD

            #prixVente.append(np.nan)
            nbAction = math.floor(currentWallet/df.loc[idx,"Close"])
            currentWallet = currentWallet - nbAction* df.loc[idx,"Close"]

            myrow = {'Date': idx,'position': "ACHAT",'Prix': df.loc[idx,"Close"]}

            dt = dt.append(myrow,ignore_index=True)

            #mise a jour du status
            currentStatus = status.HOLD

        #Traitement signal en VENTE    
        elif df.loc[idx,"recommandation"]==ordre.VENTE and currentStatus==status.HOLD:
            action.append(ordre.VENTE)
            currentStatus = status.FREE

            currentWallet = currentWallet + nbAction* df.loc[idx,"Close"]
            nbAction = 0
            

            myrow = {'Date': idx,'position': "VENTE",'Prix': df.loc[idx,"Close"]}
            dt = dt.append(myrow,ignore_index=True)


        else:
            action.append(ordre.NEUTRE)
    
        df.loc[idx,"fonds"]= nbAction*df.loc[idx,"Close"]+currentWallet
    
    df["position"] = action

    # creation d'une time series sur dy
    dt = dt.set_index('Date')
    dt = dt.set_index(pd.to_datetime(dt.index))


    # tracée de la stratégie
    fig, ax = plt.subplots(2,figsize=(12,8),sharex=True)

  
    ax[0].plot(df["Close"], label="Prix Cloture")
    
    ax[0].plot(dt[dt["position"]=="ACHAT"]["Prix"], 
                marker = '^', markersize = 10, color = 'green', label = 'ACHAT',linestyle = 'None')
    ax[0].plot(dt[dt["position"]=="VENTE"]["Prix"], 
                marker = 'v', markersize = 10, color = 'red', label = 'VENTE',linestyle = 'None')
       
    leg = ax[0].legend(loc='best', bbox_to_anchor=[0, 1],
                    ncol=1, shadow=True, title="Legend", fancybox=True)
    leg.get_title().set_color("black")
    ax[0].grid(True)

    ax[1].plot(df["fonds"]/wallet*100,label ="fonds")
    ax[1].plot(df["amount0"]/wallet*100,label ="buy and hold")
    ax[1].grid(True)
    plt.legend()
    
    plt.show()

    return dt