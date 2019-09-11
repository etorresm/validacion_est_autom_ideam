#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 16:36:49 2018

@author: edwin
"""
import pandas as pd
import requests
import numpy as np
import os


os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/descargas')
#os.chdir('/home/agrometeo/edwin/descarga_hydras')

estaciones = pd.read_csv('estaciones_descarga.csv', header=None)
lista_esta = (list(estaciones[0]))

sid = input('sid IDEAM:')

variables = ['0068','0069','0070','0071','0027','0028','0240','0257','0255','0258','0103','0104','0105','0107','0111','0112','0239','0259','9000','0310','0075','0076','0077','0241','0242','0243','0030','0245','0246','0247','0240','0237','0239','0260']

#os.chdir('/home/agrometeo/edwin/descarga_hydras')

for i in lista_esta:
    for j in variables:
        dfs = np.NaN
        url = 'http://hydras3.ideam.gov.co/DATA.HTM?workspace=1&station=00'+str(i)+'&sensor='+str(j)+'&sid='+str(sid)+'+&start=2005&end=20180222&ymin=0&ymax=50&res=640x480&submit=Tabla'
        header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
        r = requests.get(url, headers=header)
        if len(r.text) > 100:
            dfs = pd.read_html(r.text)
            if len(dfs[0]) > 5:
                dfs_1 = dfs[0]
                dfs_1.columns = [dfs_1.iloc[0,:]]
                dfs_1['cod'] = i
                dfs_1['var'] = j
                dfs_1 = dfs_1[['cod', 'Fecha', 'Hora', 'Valor', 'var']]
                dfs_1 = dfs_1.iloc[1:,:]
                dfs_1.to_csv(str(i)+'_'+str(j)+'.csv', header=False, index=False)
                
        

    
    