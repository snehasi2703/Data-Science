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

def strategy_1(W_st, W_lt):   
    df = pd.read_csv(file_name)
    #add and calculate required columns
    df.rename(columns={'Adj Close': 'Price'}, inplace = True)
    df['st_ma'] = df['Price'].rolling(W_st).mean()
    df['lt_ma'] = df['Price'].rolling(W_lt).mean()
    df = df.tail(len(df) - 50)
    df['buy'] = df['st_ma'] > df['lt_ma']
    df['sell'] = df['st_ma'] < df['lt_ma']
    
    #declare required valiables
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
    for eachDay in range(50,1258):
        if df['buy'].loc[eachDay] == False and no_of_stock == 0:
            continue
        else:
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
    return (total_profit - total_loss)/(no_of_wins + no_of_losses)      

for W_st in range(14, 50, 7):
    for i in range(1, 15):
        W_lt = W_st+ i * 7
        Profit_loss = strategy_1(W_st, W_lt)
        if(Profit_loss < 0):
            plt.scatter(W_st, W_lt, c='R', s=(Profit_loss*(-1)))
        else:
            plt.scatter(W_st, W_lt, c='G', s=Profit_loss)    
   