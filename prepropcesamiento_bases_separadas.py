#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 17:15:26 2018

@author: edwin
"""


import pandas as pd
import numpy as np
import os
import pdb


#Directorio
os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/descarga_hydras2')

#Lista de archivos

lista_estaciones = pd.DataFrame(list(os.listdir()))

lista_estaciones.columns = ['a']   #nombres
lista_estaciones.columns.values[0] = 'a'

lista_estaciones['cod'], lista_estaciones['varr'] = lista_estaciones.a.str.split('_').str

lista_estaciones['variable'], lista_estaciones['csv']= lista_estaciones.varr.str.split('.').str

lista_estaciones_2 = lista_estaciones.iloc[:,[1,3]]

# =============================================================================
# 21206600 = Nueva generación Bogotá
# 21206990 = Tibaitatá
# 21206790 = Nemocón Hda Sta Ana 
# =============================================================================

#os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/hydras')#????
#base1 = pd.read_csv('21206990_2007_0075.csv', header=None)


#Cargar la base de datos de las variables
os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam')
vari_hydras = pd.read_csv('base_nombres.csv')

# Función para arreglar cada csv y ponerlo en forma para ser usado
def ajuste_base(base):
    base.columns = ['cod', 'dat1', 'dat2', 'value', 'cod_var']
    base['date'] = base.dat1.astype(str) + '-' + base.dat2.astype(str)
    base.date = pd.to_datetime(base.date, format ='%Y%m%d-%H:%M:%S', errors='coerce')
    nombre_1 = vari_hydras[vari_hydras.variable.isin(base.cod_var)].titulo # Busca cual es el nombre de la variable
    base.columns.values[3] = nombre_1.iloc[0]
    base2 = base.iloc[:,[0,5,3]]
    base2.iloc[:,2] = pd.to_numeric(base2.iloc[:,2], errors = 'coerce')
    return(base2)

lista_estaciones_3 = lista_estaciones_2.iloc[:,:].astype(str)

for i in list(lista_estaciones_3.cod.unique()):
#for i in list(pd.DataFrame(lista_estaciones_3.cod.unique()).iloc[61:78,0]):
    #print(i)
#     c1 = pd.DataFrame({ 'cod' : [99999999, 99999991],
#                            'date' : ([pd.to_datetime('1999-01-01 02:00:00'),
#                                       pd.to_datetime('1999-01-01 03:00:00')]),})
#     d1 = pd.DataFrame({ 'cod' : [99999999, 99999991],
#                            'date' : ([pd.to_datetime('1999-01-01 02:00:00'),
#                                       pd.to_datetime('1999-01-01 03:00:00')]),})
#     
#     a = np.NaN
#     c = pd.DataFrame({ 'cod' : [99999999, 99999991],
#                            'date' : ([pd.to_datetime('1999-01-01 02:00:00'), pd.to_datetime('1999-01-01 03:00:00')]),
#                 })
    
    for k in list(lista_estaciones_3.variable.unique()):
        acod = (i + '_' + k +'.csv')
        acod2 = lista_estaciones[lista_estaciones.a == acod]
        if len(lista_estaciones[lista_estaciones.a == acod]) > 0: # El condicional para la selección del archivo
            os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/descarga_hydras2')
            pdb.set_trace()
            base_a = pd.read_csv(acod)
            base_b = ajuste_base(base_a)
            os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/datos_variables')
            base_b.to_csv(i + '_' + base_b.columns[2] +'.csv')
            
