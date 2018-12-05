# -*- coding: utf-8 -*-
"""
Created on Tues Oct  2 03:26:00 2018

@author: singh
"""
import matplotlib.pyplot as plt
import os
import pandas as pd

file_dir = os.path.join('C:\\','Users', 'singh','Documents\data Science with Python\Assignment1')
file_name = os.path.join(file_dir, 'SSC.csv') 
#Seven Stars Cloud Group, Inc. (SSC)
#NasdaqCM - NasdaqCM Real Time Price. Currency in USD

def strategy_2(w, k): 
    df = pd.read_csv(file_name)
    df.rename(columns={'Adj Close': 'Price'}, inplace = True)
    
    df['std'] = df['Price'].rolling(w).std()
    df['st_ma'] = df['Price'].rolling(w).mean()
    df['low_band'] = df['st_ma'] - k*df['std']
    df['upper_band'] = df['st_ma'] + k*df['std']
    df = df.tail(len(df) - 14)
    df['buy'] = df['Price'] > df['upper_band']
    df['sell'] = df['Price'] < df['low_band']
    
    #declare variables
    no_of_stock = 0
    count_of_buy = 0
    count_of_sell = 0
    no_of_wins = 0
    no_of_losses = 0
    buying_price = 100
    selling_price = 0
    total_profit = 0
    total_loss = 0
    
    #loop through to calculate each win and loss
    for eachDay in range(14,len(df) - 1):
        if df['buy'].loc[eachDay] == False and no_of_stock == 0:
            continue
        else: #if buy is true or we have some stock
            if df['buy'].loc[eachDay] == True and no_of_stock == 0:
                no_of_stock = buying_price/df['Price'].loc[eachDay] #buy with 100 bucks per transaction  
                count_of_buy +=  1       
            elif df['sell'].loc[eachDay] == True and no_of_stock != 0:
                selling_price = no_of_stock * df['Price'].loc[eachDay]
                no_of_stock = 0
                count_of_sell +=  1
                if selling_price > buying_price:
                    profit = selling_price - buying_price
                    total_profit += profit
                    no_of_wins += 1
                else:
                    loss = buying_price - selling_price
                    total_loss += loss
                    no_of_losses += 1                
            else:
                continue
    #print(total_profit)        
    if (no_of_wins + no_of_losses) > 0 :     
    #print((total_profit - total_loss)/(no_of_wins + no_of_losses))
        return (total_profit - total_loss)/(no_of_wins + no_of_losses)
    else:
        return 0

k_list = [0.5, 1, 1.25, 1.5, 1.75,
         2, 2.25, 2.5, 2.75,
         3, 3.25, 3.5, 3.75]

for w in range(14, 100, 7):
    for k in k_list:
        profit_loss = strategy_2(w, k)
        if(profit_loss != 0):
            if(profit_loss < 0):
                plt.scatter(w, k, c='R', s=(profit_loss*(-1)))
            else:
                plt.scatter(w, k, c='G', s=profit_loss)  