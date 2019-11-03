# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:00:39 2019

@author: v.mazeiko
"""
#%%
import pandas as pd
import re
#%%
print(f'homework. Task 1')
print(f'Залить в свою БД данные по продажам (часть таблицы Orders в csv)')
df = pd.read_csv('orders.csv', sep=";")

#%%
#df = df.tail(100).append(df.head(100)).reset_index()
#%%
df['o_date'] = df['o_date'].astype('datetime64[D]')

#%%
for i in range(len(df)):
    df['price'][i] = float(df['price'][i].replace(',', '.'))

#df['o_date'] = pd.to_datetime(df['o_date'], format="%d/%m/%Y")
#for i in range(len(df)):
#    df['price'][i] = re.sub(',','.', df['price'][i])
#    df['price'][i] = float(df['price'][i])
#    print(f"{i} = {df['price'][i]}, type is {type(df['price'][i])}.")
#%%
pd.set_option('display.float_format', '{:.3f}'.format)
#%%
print(f'homework. Task 2')
print(f'Проанализировать, какой период данных выгружен')

fst_date = df['o_date'].min().strftime("%m.%d.%Y")
lst_date = df['o_date'].max().strftime("%m.%d.%Y")
print(f'period of DB is from  {fst_date} to {lst_date}.')
#period of DB is from  01.01.2016 to 31.12.2017.
#%%
print(f'homework. Task 3')
print(f'Посчитать кол-во строк, кол-во заказов и кол-во уникальных\n\
пользователей, которые совершали заказы.')

df['id_o'].unique()
df['user_id'].unique()
df['o_date'].unique()
print(f'DB has {len(df)} rows.') 
#DB has 2002804 rows.
print(f'DB has {len(df["id_o"].unique())} unique orders.')
#DB has 2002804 unique orders.
print(f'DB has {len(df["user_id"].unique())} unique user id.')
#DB has 1015119 unique user id.
#%%
print(f'homework. Task 4')
print(f'По годам посчитать средний чек, среднее кол-во заказов на\n\
пользователя, сделать вывод , как изменялись это показатели год\
от года.')
stats = {}
years = df['o_date'].dt.year.unique()
for year in years:
    tmpdf = df.loc[(df['o_date'].dt.year == year)]
    mean_price = tmpdf['price'].mean()
    mean_order_per_user = tmpdf.groupby('user_id').count()[['id_o']].mean()[0]
    year_stat = {
            'средний чек' : mean_price,
            'среднее число заказов на один аккаунт' :  mean_order_per_user
                }
    
    stats.setdefault(year,{})
    stats[year].update(year_stat)
    
    print(year)
    print(stats[year])
  
    

#%%
print(f'homework. Task 5')
print(f'Найти кол-во пользователей, кот покупали в одном году и перестали\n\
покупать в следующем.')

df16 = df.loc[(df['o_date'].dt.year == years[0])]
df17 = df.loc[(df['o_date'].dt.year == years[1])]
print(f'Retaler has lost {len(df16[~df16.isin(df17)].dropna())} costumers')

#len(df.loc[(df['o_date'].dt.year == years[0])]\
#           [~df.loc[(df['o_date'].dt.year == years[0])]\
#                    .isin(df.loc[(df['o_date'].dt.year == years[1])])]\
#                    .dropna())
    
#%%
print(f'homework. Task 6')
print(f'Найти ID самого активного по кол-ву покупок пользователя.')
most_active_costumer = df.groupby('user_id').count()[['id_o']]\
                            .sort_values(by='id_o').tail(1)
most_active_costumer = most_active_costumer.index[0]
print(f'The most active costumer is {most_active_costumer}.') 