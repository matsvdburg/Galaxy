# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 11:08:56 2022

@author: matsv
"""
import pandas as pd
import math
import numpy as np

# Inlezen van excel data en omvormen naar DataFrame
df = pd.read_excel('Solar_System.xlsx')

# Verwijder (drop) onnodige colummen
df.drop([
    'mass',
    'vol',
    'aroundPlanet',
    'aroundPlanet.rel',
    'vol.volValue',
    'vol.volExponent',
    'row',
    'axialTilt',
    'mainAnomaly',
    'argPeriapsis',
    'longAscNode',
    'isPlanet',
    'semimajorAxis',
    'eccentricity',
    'inclination',
    'escape',
    'equaRadius',
    'polarRadius',
    'flattening',
    'dimension',
    'sideralOrbit',
    'alternativeName',
    'mass.massValue',
    'mass.massExponent',
    'aroundPlanet.planet',
    'density'
    
    ], axis=1, inplace=True)

# Creëer nieuwe kolom die omtrek berekent aan de hand van 'meanRadius' met math.pi functie
df['meanCircum'] = 2 * (df['meanRadius']) * math.pi

# Verander alle 0-waarden van 'avgTemp' naar "nan"
df['avgTemp'] = df['avgTemp'].replace(0,"nan")

# Maak nieuwe kolom 'discoveryYear' die de datum van 'discoveryDate' opschoont
df['discoveryYear'] = df['discoveryDate'].str.split('/').str[2]

# Verander lege waarden naar 0
df['discoveryYear'] = df['discoveryYear'].fillna(0)

# Verander het type 'discoveryYear' naar integer
df['discoveryYear'] = df['discoveryYear'].astype(int)

# Deel de waarden van 'discoveryPeriod' in in verschillende secties om zo perioden te creëeren
df["discoveryPeriod"] = pd.cut(x=df["discoveryYear"],
    bins=[-1,
          1600, 
          1649, 
          1699, 
          1749,
          1799,
          1849,
          1899,
          1949,
          1999, 
          np.inf],
    labels=["Unknown", 
            "1600 - 1649", 
            "1650 - 1699", 
            "1700 - 1749", 
            "1750 - 1799", 
            "1800 - 1849", 
            "1850 - 1899", 
            "1900 - 1949", 
            "1950 - 1999", 
            "2000 - 2022"
            ])

# Verander de 0-waarden in de kolom naar een leeg veld
df['discoveryYear'] = df['discoveryYear'].replace(0, "")

# Maak een nieuwe kolom met alleen de waarde 1 (gebruikt om de piechart te creëeren)
df['numbers'] = 1

# Exporteer Pandas DataFrame naar excel
df.to_excel("final_data.xlsx")
