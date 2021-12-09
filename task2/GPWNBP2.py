#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import urllib.request
from bs4 import BeautifulSoup as bs

# In[50]:


def calculateVolumeByCurrency(filepath):
    try:                   
        excel_data_df = pd.read_excel(filepath)
        excel_data_df['Obrót'] = excel_data_df['Obrót']*1000    
        excel_data_df['Najlepszy_papier'] = excel_data_df['Kurs max'] / excel_data_df['Kurs min']
        positiveWolumen = excel_data_df[excel_data_df.Wolumen>0]
        bestRate=positiveWolumen.loc[positiveWolumen.Najlepszy_papier == positiveWolumen.Najlepszy_papier.max()].iloc[:,[0,3,4,5,6,10]].reset_index(drop=True)
        currencyPastedByUser = input('Podaj trzyznakowy skrót waluty: ').upper()
        if len(currencyPastedByUser)!=3:
            raise Exception(f"Skót waluty ma być trzy znakowy. Podany skrót: {currencyPastedByUser}")
        exchangeRates = getExchangeRates(currencyPastedByUser)
        bestRate['Obrót'] = (bestRate['Obrót']*exchangeRates).round(2)        
        # bestRate['Kurs średni']= exchangeRates
        return bestRate
    except FileNotFoundError:
        raise Exception(f"Plik nie istnieje. Podany plik: {filepath}")


# In[51]:


def getExchangeRates(currencyPastedByUser):
    tableA = getTableFromUrl('https://www.nbp.pl/home.aspx?f=/kursy/kursya.html')
    tableB = getTableFromUrl('https://www.nbp.pl/home.aspx?f=/kursy/kursyb.html')
    exchangeRates = tableA.append(tableB, ignore_index = True)    
    exchangeRate= exchangeRates[exchangeRates['Kod waluty'].str.contains(currencyPastedByUser)].reset_index(drop=True)
    if exchangeRate.empty:
        raise Exception(f"Nie udało się znaleźć kursu dla waluty: {currencyPastedByUser}")
    tmp = int (exchangeRate['Kod waluty'].values[0].split()[0])
    if tmp != 1:
        return exchangeRate['Kurs średni'].values[0]/tmp
    return exchangeRate['Kurs średni'].values[0]


# In[52]:


def getTableFromUrl(url):
    with urllib.request.urlopen(url) as stronahtml:
        html = stronahtml.read()
    htmlWebSite = bs(html, 'html.parser')
    full_table = htmlWebSite.select('table.pad5')
    table = pd.read_html(str(full_table),flavor='html5lib', thousands='.' , decimal =',')[0]
    return table


result = calculateVolumeByCurrency('GPW.xlsx')
print(result)
