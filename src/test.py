from dataclasses import dataclass
import pandas as pd 
import os
import matplotlib.pyplot as plt
from ta import add_all_ta_features
from ta.utils import dropna
import seaborn as sns

pd.options.mode.chained_assignment = None  # default='warn'


def get_basic_data(stock_df):
    # get basic stock infor by analyzing df using pandas
    print(f"{stock_df} stock information:")
    print(stock_df.describe())
    print(stock_df.info())


def price_change(stock_df):
    # plot stocks change in price over time based on the adjusted close
    stock_df['Adj Close'].plot(legend=True,figsize=(12,5))
    stock_df.set_index('Date',inplace=True)
    # plt.show()

    # plot the change in traded volume for a particular stock
    stock_df.plot(legend=True,figsize=(12,5))
    # plt.show()

def tech_indicators(stock_df):
    ta_data = add_all_ta_features(stock_df, open="Open", high="High", low="Low", close="Close", volume="Volume")
    print(ta_data.columns)

def moving_averages(stock_df):
    mov_avg_days = [10, 20, 50]
    for day in mov_avg_days:
        column_name = "MA for %s days" %(str(day))
        stock_df[column_name] = stock_df['Adj Close'].rolling(window=day,center=False).mean()
    print(stock_df.tail())
    stock_df[['Adj Close','MA for 10 days','MA for 20 days','MA for 50 days']].plot(subplots=False,figsize=(12,5))
    plt.show()

def daily_return(stock_df):
    stock_df['Daily Return'] = stock_df['Adj Close'].pct_change()
    # print(stock_df['Daily Return'])
    # change the y-axis to density
    plot = sns.displot(stock_df['Daily Return'].dropna(),bins=50,color='blue')
    plt.show()

def comp_daily_return_corr(stock_list, symbol_list):
    data = []
    for stock, symbol in zip(stock_list, symbol_list):
        stock_data = pd.DataFrame()
        stock_data = stock[['Adj Close', 'Date']]
        stock_data['Symbol'] = symbol
        stock_data.reset_index()
        data.append(stock_data)

    df = pd.concat(data)
    df = df.reset_index()
    df = df[['Date', 'Adj Close', 'Symbol']]
    df_pivot = df.pivot('Date', 'Symbol', 'Adj Close').reset_index().dropna(axis=0)
    # print(df_pivot.head())
    corr_df = df_pivot.corr(method='pearson')
    corr_df.head().reset_index()
    # print(corr_df.head(10))
 
    plt.figure(figsize=(13, 8))
    sns.heatmap(corr_df, annot=True, cmap="RdYlGn")
    # plt.show()
  
    return df_pivot, corr_df

def stock_returns_plt(df_pivot):
    df_pivot.plot(figsize=(10,4))
    plt.ylabel('Price')
    plt.show()
    return

def normalizing_stocks(df_pivot):
    print(df_pivot.head())
    print(df_pivot.dtypes)
    returnfstart = df_pivot[['AAPL', 'AMZN', 'GOOG', 'INTC', 'MSFT']].apply(lambda x: x / x[0])
    # print(returnfstart.head())
    # returnfstart.plot(figsize=(10,4)).axhline(1, lw=1, color='black')
    # plt.ylabel('Return From Start Price')
    # plt.show()
    return

def daily_ret_percent(df_pivot):
    percent_diff_df = df_pivot[['AAPL', 'AMZN', 'GOOG', 'INTC', 'MSFT']].pct_change()
    percent_diff_df.insert(0, 'Date', df_pivot['Date'])
    percent_diff_df.plot(figsize=(10,4))
    plt.axhline(0, color='black', lw=1)
    plt.ylabel('Daily Percentage Return')
    plt.show()
    # for most plots fix xaxis so it shows the date
    return
    
def investment_risk_val(corr_df):
    # Compute value of risk in investing in particular stock
    risk_df = corr_df.dropna()
    plt.figure(figsize=(8,5))
    plt.scatter(risk_df.mean(),risk_df.std(),s=25)
    plt.xlabel('Expected Return')
    plt.ylabel('Risk')


    # add annotations to the scatterplot
    for label,x,y in zip(risk_df.columns,risk_df.mean(),risk_df.std()):
        plt.annotate(
        label,
        xy=(x,y),xytext=(-120,20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        arrowprops = dict(arrowstyle='->',connectionstyle = 'arc3,rad=-0.5'))
    plt.show()
    return

def get_val_at_risk(stock_df):
    # Compute the daily return 
    stock_df['Daily Return'] = stock_df['Close'] - stock_df['Open']
    sns.displot(stock_df['Daily Return'].dropna(),bins=100,color='purple')
    plt.show()
    return



def main():
    # read in stock csv files 
    AAPL = pd.read_csv("./Data/AAPL.csv")
    MSFT = pd.read_csv("./Data/MSFT.csv")
    INTC = pd.read_csv("./Data/INTC.csv")
    GOOG = pd.read_csv("./Data/GOOG.csv")
    AMZN = pd.read_csv("./Data/AMZN.csv")

    # price_change(AAPL)
    # tech_indicators(AAPL)
    moving_averages(AAPL)
    # daily_return(AAPL)

    stocks = [AAPL, MSFT, INTC, GOOG, AMZN]
    symbols = ['AAPL', 'MSFT', 'INTC', 'GOOG', 'AMZN']
    # df_pivot, corr_df = comp_daily_return_corr(stocks, symbols)
    # stock_returns_plt(df_pivot)
    # normalizing_stocks(df_pivot)
    # daily_ret_percent(df_pivot)
    # investment_risk_val(corr_df)
    # get_val_at_risk(AAPL)


main()