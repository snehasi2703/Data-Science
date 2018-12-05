# -*- coding: utf-8 -*-
"""
Created on Tues Oct  2 03:26:00 2018

@author: singh
"""
import os
import pandas as pd
file_dir = os.path.join('C:\\','Users', 'singh','Documents\data Science with Python\Assignment2')
file_name = os.path.join(file_dir, 'SSC.csv') 
#Seven Stars Cloud Group, Inc. (SSC)
#NasdaqCM - NasdaqCM Real Time Price. Currency in USD

df = pd.read_csv(file_name)
df.rename(columns={'Adj Close': 'Price'}, inplace = True)

df['pct_change'] = df['Price'].pct_change()
df['buyorSell'] = df['pct_change'] < 0
no_of_stock = 0
money_in_hand = 100

#------------------------------------------------------------------------------------------
#c)compute total accumulation
for day in range(1,len(df)):
    if df['Date'].loc[day] >= '2013-10-02':
        if (df['buyorSell'].loc[day] and no_of_stock == 0):
            no_of_stock = money_in_hand / df['Price'].loc[day]
        elif (day+1) in df.index.values and df['buyorSell'].loc[day+1] and no_of_stock != 0    :
            money_in_hand = no_of_stock * df['Price'].loc[day]
            no_of_stock = 0

#final accummulated amount started with $100 on October 2, 2013 assuming that 
#you know the performance on the next day 
final_accumulated_amount_1 = money_in_hand

#-----------------------------------------------------------------------------------------
#d)put $100 on October 2, 2013, sell on Aug 30, 2018

no_of_stock = 100 / df['Price'].loc[df['Date'] == '2013-10-02'].iloc[0]
#selling on 30th august
money_in_hand = no_of_stock * df['Price'].loc[df['Date'] == '2018-08-30'].iloc[0]
final_accumulated_amount_2 = money_in_hand

#-----------------------------------------------------------------------------------------
#e)you missed the best 10 days
no_of_stock = 0
sortedDataFrame_withbestvalues = df.copy()
sortedDataFrame_withbestvalues = sortedDataFrame_withbestvalues.sort_values('pct_change').head(10)
list_of_top_10_indexes = list(sortedDataFrame_withbestvalues.index.values)

for day in range(1,len(df)):
    if df['Date'].loc[day] >= '2013-10-02' and day not in list_of_top_10_indexes:
        if (df['buyorSell'].loc[day] and no_of_stock == 0):
            no_of_stock = 100 / df['Price'].loc[day]
        #else sell today if the prices are falling the next day    
        elif (day+1) in df.index.values and df['buyorSell'].loc[day+1] and no_of_stock != 0 :
            money_in_hand = no_of_stock * df['Price'].loc[day]
            no_of_stock = 0
final_accumulated_amount_3 = money_in_hand
#-----------------------------------------------------------------------------------------
#f)you missed the worst 10 days
no_of_stock = 0
sortedDataFrame_withworstvalues = df.copy()
sortedDataFrame_withworstvalues = sortedDataFrame_withworstvalues.sort_values('pct_change').tail(10) #last 10 values
list_of_worst_10_indexes = list(sortedDataFrame_withworstvalues.index.values)
for day in range(1,len(df)):
    if df['Date'].loc[day] >= '2013-10-02' and day not in list_of_worst_10_indexes:
        if (df['buyorSell'].loc[day] and no_of_stock == 0):
            no_of_stock = 100 / df['Price'].loc[day]
        #else sell today if the prices are falling the next day
        elif (day+1) in df.index.values and df['buyorSell'].loc[day+1] and no_of_stock != 0:
            money_in_hand = no_of_stock * df['Price'].loc[day]
            no_of_stock = 0
final_accumulated_amount_4 = money_in_hand
#-------------------------------------------------------------------------------------------
#g)you missed best 5 and worst 5 days

no_of_stock = 0
list_of_5_best_5_worst = list(sortedDataFrame_withbestvalues.index.values[:5])
list_of_5_best_5_worst.extend(list(sortedDataFrame_withworstvalues.index.values[:5]))
for day in range(1,len(df)):
    if df['Date'].loc[day] >= '2013-10-02' and day not in list_of_5_best_5_worst:
        if (df['buyorSell'].loc[day] == True and no_of_stock == 0):
            no_of_stock = 100 / df['Price'].loc[day]
         #else sell today if the prices are falling the next day    
        elif (day+1) in df.index.values and df['buyorSell'].loc[day+1] and no_of_stock != 0    :
            money_in_hand = no_of_stock * df['Price'].loc[day]
            no_of_stock = 0
final_accumulated_amount_5 = money_in_hand    

import csv
output_file_name = os.path.join(file_dir, 'output_task3_Assignment2.csv')
with open(output_file_name, mode='w') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(['Strategy_buy_hold', 'Strategy_miss_best_ten', 'Strategy_miss_worst_ten','Strategy_5_best_5_worst'])
    output_writer.writerow([final_accumulated_amount_2, final_accumulated_amount_3, final_accumulated_amount_4, final_accumulated_amount_5])
    
                    
   