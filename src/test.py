from dataclasses import dataclass
import pandas as pd 
import os
import matplotlib.pyplot as plt
from ta import add_all_ta_features
from ta.utils import dropna
import seaborn as sns


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
    plot.set_ylabel("Density")
    plt.show()

def comp_daily_return(stock_list):
    data = []
    for stock in stock_list:
        stock_data = pd.DataFrame()
        stock_data = stock[['Adj Close', 'Symbol']]
        stock_data.reset_index()
        data.append(stock_data)

def main():
    # read in stock csv files 
    AAPL = pd.read_csv("./Data/AAPL.csv")
    MSFT = pd.read_csv("./Data/MSFT.csv")
    INTC = pd.read_csv("./Data/INTC.csv")
    GOOG = pd.read_csv("./Data/GOOG.csv")
    AMZN = pd.read_csv("./Data/AMZN.csv")

    # price_change(AAPL)
    # tech_indicators(AAPL)
    # moving_averages(AAPL)
    daily_return(AAPL)


main()