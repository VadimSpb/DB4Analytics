# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:00:39 2019

@author: v.mazeiko
"""
#%%
import pandas as pd
import re
#%%
import os
os.chdir('C:/Users/v.mazeiko/Desktop/project/DB4Analytics')
#%%
df = pd.read_csv('orders.csv', sep=";")
#%% Делаем нормальную выдачу чисел, без Е.
pd.set_option('display.float_format', '{:.0f}'.format)
#%%
#df = df.tail(100).append(df.head(100)).reset_index()
#%%
df['o_date'] = df['o_date'].astype('datetime64[D]')

#%%
df['price'] = df['price'].apply(lambda x : float(x.replace(',','.')))

#%%
import datetime as dt
NOW = dt.datetime(2018,01,01)
#%%
rfmTable = df.groupby('user_id').agg({'o_date': lambda x: (NOW - x.max()).days, # Recency
                                        'id_o': lambda x: len(x),      # Frequency
                                        'price': lambda x: x.sum()}) # Monetary Value

rfmTable['o_date'] = rfmTable['o_date'].astype(int)
#%%
rfmTable.rename(columns={'o_date': 'recency', 
                         'id_o': 'frequency', 
                         'price': 'monetary_value'}, inplace=True)
rfmTable.index.names = ['user_id']


#%%
rfmTable.loc[(rfmTable['recency'] < 30),'r'] = 3
rfmTable.loc[(rfmTable['recency'] > 60),'r'] = 1
rfmTable.loc[(rfmTable['r'].isna()),'r'] = 2
#%%
rfmTable.loc[(rfmTable['frequency'] > 4),'f'] = 3
rfmTable.loc[(rfmTable['frequency'] <= 1),'f'] = 1
rfmTable.loc[(rfmTable['f'].isna()),'f'] = 2
#%%
rfmTable.loc[(rfmTable['monetary_value'] >= 15000),'s'] = 3
rfmTable.loc[(rfmTable['monetary_value'] < 5000),'s'] = 1
rfmTable.loc[(rfmTable['s'].isna()),'s'] = 2
#%%
rfmTable.loc[(rfmTable['r'] == 1),'status'] = 'lost'
#%%
rfmTable.loc[(rfmTable['r'] > 1) &
             (rfmTable['f'] == 3) &
             (rfmTable['s'] == 3),'status'] = 'VIP'
#%%
rfmTable.loc[(rfmTable['r'] > 1) &
             (rfmTable['f'] != 3) &
             (rfmTable['s'] != 3),'status'] = 'regular'
#%%
count = [len(rfmTable.loc[(rfmTable['status'] == 'VIP')]),
         len(rfmTable.loc[(rfmTable['status'] == 'lost')]),
         len(rfmTable.loc[(rfmTable['status'] == 'regular')])]
#%%
result = rfmTable.groupby(['status']).sum()['monetary_value']
result = pd.DataFrame(data=result)
result['count'] = count
#%%

#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#%%
#Сначала создаются столбцы r,f,m:
#R1 days > 60, R2  30 < days <= 60, R3 days <= 30; 
#F1 orders <= 1, F2 1 < orders <= 4, F3 > 4; 
#M1 price < 5000, 5000 <= M2 < 15000; M3 >= 15000.
#%%
#rfmTable.loc[(rfmTable['recency'] < 30),'r_class'] = 'A'
#rfmTable.loc[(rfmTable['recency'] > 60),'r_class'] = 'C'
#rfmTable.loc[(rfmTable['r_class'].isna()),'r_class'] = 'B'

#rfmTable.loc[(rfmTable['recency'] < 30),'r_class'] = 'A'
#rfmTable.loc[(rfmTable['recency'] > 60),'r_class'] = 'C'
#rfmTable.loc[(rfmTable['r_class'].isna()),'r_class'] = 'B'
#%%
from sklearn.cluster import KMeans
#%%
model = KMeans(n_clusters=3)
model.fit(rfmTable[['frequency','frequency']])
clasters_f = model.predict(rfmTable[['frequency','frequency']])
#%%
model = KMeans(n_clusters=3)
model.fit(rfmTable[['recency','recency']])
clasters_r = model.predict(rfmTable[['recency','recency']])
#%%
model = KMeans(n_clusters=3)
model.fit(rfmTable[['monetary_value','monetary_value']])
clasters_p = model.predict(rfmTable[['monetary_value','monetary_value']])
#%%
rfmTable['f_class'] = clasters_f
rfmTable['r_class'] = clasters_r
rfmTable['p_class'] = clasters_p
#%%
a ={}
for i in range(3):
    f_min = rfmTable.loc[(rfmTable['f_class'] == i),'frequency'].min()
    f_max = rfmTable.loc[(rfmTable['f_class'] == i),'frequency'].max()

    r_min = rfmTable.loc[(rfmTable['r_class'] == i),'recency'].min()
    r_max = rfmTable.loc[(rfmTable['r_class'] == i),'recency'].max()
                      
    p_min = rfmTable.loc[(rfmTable['p_class'] == i),'monetary_value'].min()
    p_max = rfmTable.loc[(rfmTable['p_class'] == i),'monetary_value'].max()
    
    a[i] = [f'{int(f_min)} - {int(f_max)}', f'{int(r_min)} - {int(r_max)}', 
            f'{int(p_min)} - {int(p_max)}']

criteries['criterion'] = ['recency', 'frequency', 'monetary_value']

#%%
criteries = pd.DataFrame(data=a)
criteries.index = ['recency', 'frequency', 'monetary_value']
#%%
rfmTable.loc[(rfmTable['r_class'] >= 1),'status'] = 'lost'
#%%



