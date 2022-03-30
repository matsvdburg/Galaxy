# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:08:56 2022

@author: matsv
"""
import requests
import pandas as pd

# API[]: Data over het zonnestelsel
url = 'https://api.le-systeme-solaire.net/rest/bodies/'

# Stuur requests naar URL
r = requests.get(url)
data = r.json() 

# Opties voor tonen van maximale columns
pd.option_context('display.max_columns', None)

# Maak Pandas DataFrame van API
df = pd.json_normalize(data["bodies"])

print(df)

# Exporteren van DataFrame naar excel werkblad
df.to_excel("Solar_System.xlsx")

