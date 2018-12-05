# -*- coding: utf-8 -*-
"""
Created on Tues Oct  2 03:26:00 2018

@author: singh
"""
import os
import math
import pandas as pd
file_dir = os.path.join('C:\\','Users', 'singh','Documents\data Science with Python\Assignment2')
file_name = os.path.join(file_dir, 'SSC.csv') 
#Seven Stars Cloud Group, Inc. (SSC)
#NasdaqCM - NasdaqCM Real Time Price. Currency in USD

df = pd.read_csv(file_name)
df.rename(columns={'Adj Close': 'Price'}, inplace = True)

df['pct_change'] = df['Price'].pct_change()
df['buyorSell'] = (df['pct_change'] < 0).astype(int)

average_profit_collection = {}
consecutive_zeroes_collection = {}

for w in {1,2,3,4,5}:
    no_of_consecutive_zeroes = 0
    n = 0
    total_profit = 0
    no_of_stock = 0
    transaction_count = 0
    average_profit_loss = 0
    for day in range (1,len(df) - 1):
        if(n > w) :
            n = 0    
        if no_of_stock == 0:
            if df['buyorSell'].loc[day] == 0 and n < w:
                n+=1
                continue;
            elif df['buyorSell'].loc[day] == 1 and n <= w:
                no_of_stock = 100 / df['Price'].loc[day]
                transaction_count+=1
            elif df['buyorSell'].loc[day] == 0 and n == w: 
                #even if it is zero, buy since window has ended
                transaction_count +=1
                no_of_stock = 100 / df['Price'].loc[day]
                no_of_consecutive_zeroes += 1
        else:
            money_in_hand = no_of_stock * df['Price'].loc[day]
            profit = (money_in_hand - 100)
            if(profit != 0 and math.isnan(profit) != True):
                total_profit += profit
            no_of_stock = 0
            transaction_count+=1   
        n+=1 #increase the window inner counter       
    if(transaction_count > 0):     
        average_profit_loss = total_profit / transaction_count     
        average_profit_collection.update({w:average_profit_loss})    
    consecutive_zeroes_collection.update({w:no_of_consecutive_zeroes}) 

import csv
output_file_name = os.path.join(file_dir, 'output_task4_Assignment2.csv')
with open(output_file_name, mode='w') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(['window_1', 'window_2', 'window_3','window_4','window_5'])
    output_writer.writerow([average_profit_collection[1], average_profit_collection[2], average_profit_collection[3], average_profit_collection[4],average_profit_collection[5]])
    output_writer.writerow(['window_1_consecutive_zeroes', 'window_2_consecutive_zeroes', 'window_3_consecutive_zeroes','window_4_consecutive_zeroes','window_5_consecutive_zeroes'])
    output_writer.writerow([consecutive_zeroes_collection[1], consecutive_zeroes_collection[2], consecutive_zeroes_collection[3], consecutive_zeroes_collection[4],consecutive_zeroes_collection[5]])    
    
                    
   
            
            