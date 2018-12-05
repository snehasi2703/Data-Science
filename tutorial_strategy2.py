# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:42:40 2018

@author: singh
"""
#strategy 2
import os
import pandas as pd
file_dir = os.path.join('C:\\','Users', 'singh','Documents\data Science with Python\Assignment1')
file_name = os.path.join(file_dir, 'SSC.csv') 
#Seven Stars Cloud Group, Inc. (SSC)
#NasdaqCM - NasdaqCM Real Time Price. Currency in USD
df = pd.read_csv(file_name)
df.rename(columns={'Adj Close': 'Price'}, inplace = True)

df['std'] = df['Price'].rolling(14).std()
k = 2 # a factor of 2
df['st_ma'] = df['Price'].rolling(14).mean()
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
final_profit_or_loss = 0

#loop through to calculate each win and loss
for eachDay in range(14,1258):
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
            #this would be the final profit or loss
            #if loss value would be negative else positive
            final_profit_or_loss = selling_price - buying_price 
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

#calculate total transaction count, average profit per win, average profit per loss        
total_transaction = no_of_wins+ no_of_losses
average_profit_per_win = total_profit/no_of_wins
average_loss_per_lose = total_loss /no_of_losses

#write back into csv file
import csv
output_file_name = os.path.join(file_dir, 'output_strategy2.txt')
with open(output_file_name, mode='w') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(['Strategy', 'S_win', 'L_win','trans','P/L','Winning','P/L', 'Loosing', 'P/L'])
    output_writer.writerow(['Strategy_1', '14', '50',total_transaction,final_profit_or_loss,no_of_wins,average_profit_per_win,no_of_losses,average_loss_per_lose])
    
