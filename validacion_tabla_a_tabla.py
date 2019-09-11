#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 17:35:01 2018
Código usado para hacer la validación de las estaciones automáticas
@author: edwin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:09:40 2018

@author: edwin
"""
#Se seleccionó los valores horarios para poderlos comparar con los datos del wrf
### Se va a crear una base de datos con precipitación, humedad relativa, brillo solar, temperatura, velocidad del viento y dirección del viento


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import style
from pvlib.location import Location
import datetime

def lista_nombres(base):
        base_r = pd.DataFrame(list(base))
        return(base_r)
        
def orden(base):
    return(base.sort_values(by='date', ascending=True))

vari = ['cod', 'date', 'precip-10min', 'hum_2m', 'Rad-gl', 'tmp_2m', 'tmp_2m_min', 'tmp_2m_max', 'Vel-vie-10min', 'Dir-vie-10min']

#Carga de los datos

os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/hydras3_2005')
lista_estaciones_2 = pd.DataFrame(list(os.listdir()))
#i = '21206990.csv'
estaciones = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/catalogo_est_4326.csv')

##Tabla para la inclusión de los datos
#humedad
humedad_tabla = (pd.DataFrame([{'cod':0,
               'isnull':0,
               'total_isnull':0,
               'range':0,
               'diff':0, 
               'total_sinnan':0,
               'No datos':0,
               'P. rango':0,
               'P. diferencia':0,
               'total_total':0}]))# Total de los datos sin contar los NA de la humedad

#Precipitación
prec_tabla = (pd.DataFrame([{'cod':0,
               'isnull':0,
               'total_isnull':0,
               'range':0,
               'total_sinnan':0,
               'No datos':0,
               'P. rango':0,
               'total_total':0}]))# Total de los datos sin contar los NA de la humedad
 
    
#Velocidad del viento

        
vv_tabla = (pd.DataFrame([{'cod':0,
       'isnull':0,
       'total_isnull':0,
       'range':0,
       'diff':0,
       'roll_1':0,
       'P. Rango':0,
       'P. diferencia':0,
       'P. secuencia':0,
       'total_sinnan':0,
       'total_total':0}]))# Total de los datos sin contar los NA de la humedad

    
## Radiación
    
rad_tabla = (pd.DataFrame([{'cod':0,
       'isnull':0,
       'total_isnull':0,
       'range':0,
       'diff':0,
       'sky_1':0,
       'P. Rango':0,
       'P. diferencia':0,
       'P. cielo despejado':0,
       'total_sinnan':0,
       'total_total':0}]))

# Dirección del viento:

dir_tabla = (pd.DataFrame([{'cod':0,
   'isnull':0,
   'total_isnull':0,
   'range':0,
   'total_sinnan':0,
   'P. Rango':0,
   'total_total':0}]))
    
#Tmp tabla

tmp_tabla = (pd.DataFrame([{'cod':0,
   'isnull':0,
   'total_isnull':0,
   'range':0,
   'spikes':0,
   'diff':0,
   'roll':0,
   'rango_valores':0,
   'P. Rango':0,
   'P. spikes':0,
   'P. diferencia':0,
   'P. roll':0,
   'P. rango_val':0,
   'total_sinnan':0,
   'total_total':0}]))

os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/datos_variables')

lista_total = os.listdir()

lista_codigos = pd.DataFrame({'a':os.listdir()}).a.str[0:8].unique()

lista_var_1 = pd.DataFrame({'a':os.listdir()}).a.str[9:-4].unique()

def acomodar(base):
    base.date = pd.to_datetime(base.date, format ='%Y%m%d %H:%M:%S', errors='coerce')
    base = base.sort_values(by='date', ascending=True)
    
    

for i in lista_codigos:
    print(i)
#i = '21195160.csv'    
#i = '21206990.csv'  
#i = '21205791.csv'
    
    #base = pd.read_csv(i)
    #base.date = pd.to_datetime(base.date, format ='%Y%m%d %H:%M:%S', errors='coerce')
    #base = base.sort_values(by='date', ascending=True)
    #base2 = base.iloc[:,np.where(lista_nombres(base).isin(vari) == True)[0]]
    
    #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
    
    #Cambio de los nombres porque no se pueden manejar fácilmente
    
    if i+'_tmp_2m.csv' not in lista_total:
            continue
    
    
    #######################Validación de la humedad relativa
    
    if i+'_hum_2m.csv' in lista_total:
        
        base_hum = pd.read_csv(i+'_hum_2m.csv')
        
        acomodar(base_hum)
        
        #Plot del antes
        #plt.plot_date(base_hum.date, base_hum.hum_2m)
        
        # Si el valor es 1 quiere decir que es un dato erroneo
        
        #Quitar los no valores
        
        base_hum['null_1'] = np.where(base_hum.hum_2m.isnull(), 1, 0)
        
        #Límites según Shafer en el artículo de Estevez2011
        
        base_hum['range'] = np.where((base_hum.hum_2m > 0.8) & (base_hum.hum_2m < 100), 0, 1)
        
        # La diferencia de los valores no puede ser superior a 45°C
            # Se le quitan los valores que son NaN para evitar problemas 
        base_hum['diff_0'] = ((abs((base_hum[-base_hum.hum_2m.isnull()].hum_2m) - (base_hum[-base_hum.hum_2m.isnull()].hum_2m.shift(1))) < 45))
        base_hum['diff_1'] = np.where(base_hum.diff_0 == True, 0, 1)
        
        n_datos = len(base_hum)
        
#        if (n_datos - len(base_hum[base_hum.null_1 == 0])) < 0:
#            n_datos = len(base_hum)
        
        ##Tabla para la estadística de la validación
        humedad_tabla = humedad_tabla.append(pd.DataFrame([{'cod':i[0:8], # Código
                       'isnull':(n_datos -len(base_hum[base_hum.null_1 == 0])),
                       'total_isnull':n_datos,
                       'range':base_hum[-base_hum.hum_2m.isnull()].range.sum(),
                       'diff':base_hum[-base_hum.hum_2m.isnull()].diff_1.sum(), 
                       'total_sinnan':len(base_hum[-base_hum.hum_2m.isnull()]),
                       'No datos':((n_datos -len(base_hum[base_hum.null_1 == 0])) * 100)/n_datos,
                       'P. rango':(base_hum[-base_hum.hum_2m.isnull()].range.sum() * 100) / len(base_hum[-base_hum.hum_2m.isnull()]),
                       'P. diferencia':(base_hum[-base_hum.hum_2m.isnull()].diff_1.sum() * 100) / len(base_hum[-base_hum.hum_2m.isnull()]),
                       'total_total':len(base_hum)}]))# Total de los datos sin contar los NA de la humedad
        
        #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
        
        # Test de persistencia para determinar si los valores no están pegados pero no se puede usar en la humedad relativa ya que la humedad alcanza valores de 100% y se puede mantener allí por largas horas en la noche
        
        #base_hum['_roll_1'] = np.where(((base_hum.hum_2m.rolling(window = 5, center = True).std())  > 0.01 ), 0, 1)
        
        ## Resultado final
        
        base_hum['val_hum'] = np.where((base_hum['null_1'] == 0) & (base_hum['range'] == 0) & (base_hum['diff_1'] == 0), 0, 1)
        
        base_hum_2 = base_hum[['cod', 'date', 'hum_2m', 'val_hum']]
        
        base_hum_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_hum_2m.csv')
        base_hum.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_hum_2m.csv')
        
        # =============================================================================
        # plt.plot_date(base_hum.date, base_hum.hum_2m)
        # plt.plot_date(base_hum[base_hum['null_1'] == 0].date, base_hum[base_hum['null_1'] == 0].hum_2m)
        # plt.plot_date(base_hum[base_hum['range'] == 0].date, base_hum[base_hum['range'] == 0].hum_2m)
        # plt.plot_date(base_hum[base_hum['diff_1'] == 0].date, base_hum[base_hum['diff_1'] == 0].hum_2m)
        # plt.plot_date(base_hum[base_hum['_roll_1'] == 0].date, base_hum[base_hum['_roll_1'] == 0].hum_2m)
        # 
        # inicio_1 = pd.to_datetime('2014/02/14 00:00:00', format ='%Y%m%d %H:%M:%S', errors='coerce')
        # fin_1 = pd.to_datetime('2014/02/15 00:00:00', format ='%Y%m%d %H:%M:%S', errors='coerce')
        # 
        # plt.plot_date(base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)].date , base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)].hum_2m)
        # plt.plot_date(base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)][base_hum['null_1'] == 0][base_hum['range'] == 0][base_hum['diff_1'] == 0].date , base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)][base_hum['null_1'] == 0][base_hum['range'] == 0][base_hum['diff_1'] == 0].hum_2m)
        # #plt.plot_date(base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)][base_hum['null_1'] == 0][base_hum['range'] == 0][base_hum['diff_1'] == 0][base_hum['_roll_1'] == 0].date , base_hum[(base_hum.date > inicio_1) & (base_hum.date < fin_1)][base_hum['null_1'] == 0][base_hum['range'] == 0][base_hum['diff_1'] == 0][base_hum['_roll_1'] == 0].hum_2m)
        # plt.xticks(rotation = 90)
        # 
        # plt.plot_date(base2[base2.val_hum == 0].date, base2[base2.val_hum == 0].hum_2m)
        # =============================================================================
    ##Acá voy
    
    ################ Validación de la precipitación
    
    if i+'_precip-10min.csv' in lista_total: 
        
        base_prec = pd.read_csv(i+'_precip-10min.csv')
        
        acomodar(base_prec)
        
        #base2.columns.values[np.where(base2.columns.values == 'precip-10min')[0][0]] = 'precip_1'
        
        #base_prec = base2.reset_index()[['date', 'precip_1']]
        
        ## Buscar los no valores
        base_prec.columns.values[3] = 'precip_1'
        base_prec.columns = base_prec.columns.str.strip()
        base_prec['null_1'] = np.where(base_prec.precip_1.isnull(), 1, 0)
        
        ##Quitar los valores extremos
        
        base_prec['range'] = np.where((base_prec.precip_1 >= 0) & (base_prec.precip_1 < 120), 0, 1)
        
        base_prec['val_prec'] = np.where((base_prec['null_1'] == 0) & (base_prec['range'] == 0), 0, 1)
    
        ##Tabla para la precipitación
        
         ##Tabla para la estadística de la validación
         
        
        #if(n_datos - len(base_prec[base_prec.null_1 == 0])) < 0:
        n_datos = len(base_prec)
         
        prec_tabla = prec_tabla.append(pd.DataFrame([{'cod':i[0:8], #Código
                       'isnull':( n_datos -len(base_prec[base_prec.null_1 == 0])),
                       'total_isnull':n_datos,
                       'range':base_prec[-base_prec.precip_1.isnull()].range.sum(),
                       'total_sinnan':len(base_prec[-base_prec.precip_1.isnull()]),
                       'No datos':(( n_datos -len(base_prec[base_prec.null_1 == 0])) * 100) / n_datos,
                       'P. rango':(base_prec[-base_prec.precip_1.isnull()].range.sum() * 100) / len(base_prec[-base_prec.precip_1.isnull()]),
                       'total_total':len(base_prec)}]))# Total de los datos sin contar los NA de la humedad
    
        base_prec_2 = base_prec[['cod', 'date', 'precip_1', 'val_prec']]
        
        base_prec_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_precip_1.csv')
        base_prec.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_precip_1.csv')
    
    # =============================================================================
    # 
    # plt.plot_date(base_prec.date, base_prec.precip_1)
    # plt.plot_date(base_prec[base_prec.range == 0].date, base_prec[base_prec.range == 0].precip_1)
    # plt.plot_date(base2[base2.val_prec == 0].date, base2[base2.val_prec == 0].precip_1)
    # 
    # inicio_1 = pd.to_datetime('2014/05/01 00:00:00', format ='%Y%m%d %H:%M:%S', errors='coerce')
    # fin_1 = pd.to_datetime('2014/05/30 00:00:00', format ='%Y%m%d %H:%M:%S', errors='coerce')
    # 
    # plt.plot_date(base2.date, base2.precip_1)
    # plt.plot_date(base2[(base2.date > inicio_1) & (base2.date < fin_1)][base2.val_prec == 0].date, base2[(base2.date > inicio_1) & (base2.date < fin_1)][base2.val_prec == 0].precip_1)
    # 
    # plt.xticks(rotation = 90)
    # =============================================================================
    
    
    
    
    ##########################Validación de la velocidad del viento
        
    if i+'_Vel-vie-10min.csv' in lista_total:
        
        base_vv = pd.read_csv(i+'_Vel-vie-10min.csv')
        acomodar(base_vv)
    
        #base2.columns.values[np.where(base2.columns.values == 'Vel-vie-10min')[0][0]] = 'vel_vi10'
        
        #base_vv = base2.reset_index()[['date', 'vel_vi10']]
        
        #Plot del antes
        #plt.plot_date(base_vv.date, base_vv.vel_vi10)
        
        # Si el valor es 1 quiere decir que es un dato erroneo
        
        #Quitar los no valores
        base_vv.columns.values[3] = 'vel_vi10'
        base_vv.columns = base_vv.columns.str.strip()
        
        base_vv['null_1'] = np.where(base_vv.vel_vi10.isnull(), 1, 0)
        
        #Límites según Shafer en el artículo de Estevez2011
        
        base_vv['range'] = np.where((base_vv.vel_vi10 >= 0) & (base_vv.vel_vi10 < 60.3), 0, 1)
        
        # La diferencia de los valores no puede ser superior a 45°C
        
        base_vv['diff_0'] = ((abs((base_vv[-base_vv.vel_vi10.isnull()].vel_vi10) - (base_vv[-base_vv.vel_vi10.isnull()].vel_vi10.shift(1))) < 10))
        base_vv['diff_1'] = np.where(base_vv.diff_0 == True, 0, 1)
        
        # Test de persistencia para determinar si los valores no están pegados pero no se puede usar en la humedad relativa ya que la humedad alcanza valores de 100% y se puede mantener allí por largas horas en la noche
        
        base_vv['_roll_1'] = np.where(((base_vv.vel_vi10.rolling(window = 5, center = True).std())  > 0.01 ), 0, 1)
        
        ##Tabla resúmen para los estadísticos
        
        #if (n_datos - len(base_vv[base_vv.null_1 == 0])) < 0:
        n_datos = len(base_vv)
            
        
        vv_tabla = vv_tabla.append(pd.DataFrame([{'cod':i[0:8], #Código
                                                  
                                                                
               'isnull':(n_datos - len(base_vv[base_vv.null_1 == 0])),
               'total_isnull':n_datos,
               'range':base_vv[-base_vv.vel_vi10.isnull()].range.sum(),
               'diff':base_vv[-base_vv.vel_vi10.isnull()].diff_1.sum(),
               'roll_1':base_vv[-base_vv.vel_vi10.isnull()]._roll_1.sum(),
               'No. datos':((n_datos - len(base_vv[base_vv.null_1 == 0])) *100)/n_datos,
               'P. Rango':((base_vv[-base_vv.vel_vi10.isnull()].range.sum()) *100)/len(base_vv[-base_vv.vel_vi10.isnull()]),
               'P. diferencia':( (base_vv[-base_vv.vel_vi10.isnull()].diff_1.sum())*100)/len(base_vv[-base_vv.vel_vi10.isnull()]),
               'P. secuencia':((base_vv[-base_vv.vel_vi10.isnull()]._roll_1.sum()) *100)/len(base_vv[-base_vv.vel_vi10.isnull()]),
               'total_sinnan':len(base_vv[-base_vv.vel_vi10.isnull()]),
               'total_total':len(base_vv)}]))# Total de los datos sin contar los NA de la humedad

        #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
        
        base_vv['val_vv'] = np.where(((base_vv.diff_1 == 0) & (base_vv.range == 0) & 
             (base_vv.null_1 == 0)), 0, 1)
        
        base_vv_2 = base_vv[['cod', 'date', 'vel_vi10', 'val_vv']]
        
        base_vv_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_vel_vi10.csv')
        base_vv.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_vel_vi10.csv')
        
        
        # =============================================================================
        # plt.plot_date(base_vv.date, base_vv.vel_vi10)
        # plt.plot_date(base_vv[(base_vv.null_1 == 0)].date,
        #               base_vv[(base_vv.null_1 == 0)].vel_vi10)
        # 
        # plt.plot_date(base_vv[(base_vv.range == 0) & (base_vv.null_1 == 0)].date,
        #               base_vv[(base_vv.range == 0) & (base_vv.null_1 == 0)].vel_vi10)
        # 
        # plt.plot_date(base_vv[(base_vv.diff_1 == 0) & (base_vv.range == 0) & (base_vv.null_1 == 0)].date,
        #               base_vv[(base_vv.diff_1 == 0) & (base_vv.range == 0) & (base_vv.null_1 == 0)].vel_vi10)
        # 
        # #plt.plot_date(base_vv[(base_vv._roll_1 == 0) & (base_vv.diff_1 == 0) & (base_vv.range == 0) & (base_vv.null_1 == 0)].date,
        # #              base_vv[(base_vv._roll_1 == 0) & (base_vv.diff_1 == 0) & (base_vv.range == 0) & (base_vv.null_1 == 0)].vel_vi10)
        # 
        # =============================================================================
        
        ## Resultado final
        
        
        
        
    
    
    
    ######################################Validación de la radiación
    
    if i+'_Rad-gl.csv' in lista_total:
        
        base_rad = pd.read_csv(i+'_Rad-gl.csv')
        acomodar(base_rad)
        
        #base2.columns.values[np.where(base2.columns.values == 'Rad-gl')[0][0]] = 'rad_1'
        #base_rad = base2.reset_index()[['date', 'rad_1']]
        #Quitar los valores con NaN
        
        base_rad.columns.values[3] = 'rad_1'
        base_rad.columns = base_rad.columns.str.strip()        
        
        base_rad['null_1'] = np.where(base_rad.rad_1.isnull(), 1, 0)
        
        #Quitar los valores que estén fuera de rango
        
        base_rad['range'] = np.where((base_rad.rad_1 >= -1) & (base_rad.rad_1 < 1500), 0, 1)
        
        #La diferencia de los datos no puede exceder y si es un Na tomarlo como un dato
        
        base_rad['diff_0'] = (abs((base_rad[-base_rad.rad_1.isnull()].rad_1) - (base_rad[-base_rad.rad_1.isnull()].rad_1.shift(1))) < 555.)
        base_rad['diff_1'] = np.where(base_rad.diff_0 == True, 0, 1)
        
        #Validación de los datos que no se salgan de los valores máximos
        
        tus = Location(float(estaciones[estaciones.cod == int(i[0:8])].LATITUD), float(estaciones[estaciones.cod == int(i[0:8])].LONGITUD), 'America/Bogota')
        base_rad['sky_0'] = tus.get_clearsky(pd.DatetimeIndex(base_rad.date, tz='America/Bogota'))['ghi'].reset_index(drop=True)  # ineichen with climatology table by default
        
        base_rad['sky_1'] = np.where(((base_rad.sky_0 +10) > base_rad.rad_1), 0, 1)
        
        
        
        ##Tabla de resumen para extracción de las estadísticas
        
        #if (n_datos - len(base_rad[base_rad.null_1 == 0])) < 0:
        n_datos = len(base_rad)
        
        rad_tabla = rad_tabla.append(pd.DataFrame([{'cod':i[0:8], #Código
               'isnull':(n_datos - len(base_rad[base_rad.null_1 == 0])),
               'total_isnull':n_datos,
               'range':base_rad[-base_rad.rad_1.isnull()].range.sum(),
               'diff':base_rad[-base_rad.rad_1.isnull()].diff_1.sum(),
               'sky_1':base_rad[-base_rad.rad_1.isnull()].sky_1.sum(),
               'No. datos':((n_datos - len(base_rad[base_rad.null_1 == 0])) *100)/n_datos,
               'P. Rango':( (base_rad[-base_rad.rad_1.isnull()].range.sum())*100)/len(base_rad[-base_rad.rad_1.isnull()]),
               'P. diferencia':((base_rad[-base_rad.rad_1.isnull()].diff_1.sum()) *100)/len(base_rad[-base_rad.rad_1.isnull()]),
               'P. cielo despejado':((base_rad[-base_rad.rad_1.isnull()].sky_1.sum()) *100)/len(base_rad[-base_rad.rad_1.isnull()]),
               'total_sinnan':len(base_rad[-base_rad.rad_1.isnull()]),
               'total_total':len(base_rad)}]))
        #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
        # =============================================================================
        # plt.plot_date(base_rad.date, base_rad.rad_1)
        # plt.plot_date(base_rad[base_rad.null_1 == 0].date, base_rad[base_rad.null_1 == 0].rad_1)
        # 
        # plt.plot_date(base_rad[(base_rad.range == 0) & (base_rad.null_1 == 0)].date,
        #                        base_rad[(base_rad.range == 0) & (base_rad.null_1 == 0)].rad_1)
        # 
        # plt.plot_date(base_rad[(base_rad.diff_1 == 0) & (base_rad.range == 0) & (base_rad.null_1 == 0)].date,
        #                        base_rad[(base_rad.diff_1 == 0) & (base_rad.range == 0) & (base_rad.null_1 == 0)].rad_1)
        # 
        # 
        # plt.plot_date(base_rad[(base_rad.sky_1 == 0) & (base_rad.diff_1 == 0) & (base_rad.range == 0) & (base_rad.null_1 == 0)].date,
        #                        base_rad[(base_rad.sky_1 == 0) & (base_rad.diff_1 == 0) & (base_rad.diff_1 == 0) & (base_rad.range == 0) & (base_rad.null_1 == 0)].rad_1)
        # 
        # =============================================================================
        
        base_rad['val_rad'] = np.where(((base_rad.sky_1 == 0) & (base_rad.diff_1 == 0) & 
             (base_rad.range == 0) & (base_rad.null_1 == 0)), 0, 1)
        
        base_rad['sky_3'] = base_rad['sky_0'] + 10
        
        base_rad_2 = base_rad[['cod', 'date', 'rad_1', 'val_rad', 'sky_3']]
        
        base_rad_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_val_rad.csv')
        base_rad.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_val_rad.csv')
        
        ##acá voy
        
        #### Gráfica de la profe
        
        
        inicio = pd.to_datetime('20070203', format ='%Y%m%d', errors='coerce')
        fin = pd.to_datetime('20070205', format ='%Y%m%d', errors='coerce')
        base_rad_g = base_rad_2[(base_rad_2.date > inicio) & (base_rad_2.date < fin)]
        
        
        plt.figure(figsize=((8,6)))
        plt.plot_date(base_rad_g[base_rad_g.val_rad == 0].date, base_rad_g[base_rad_g.val_rad == 0].rad_1, color='dimgray' )
        plt.plot_date(base_rad_g[base_rad_g.val_rad == 1].date, base_rad_g[base_rad_g.val_rad == 1].rad_1, color = 'dimgray', marker='^')
        plt.plot_date((base_rad_g.date), base_rad_g.sky_3, '-', color = 'k')
        plt.legend(['Validos','No-Validos','Límite'])
        plt.xticks(rotation=90)
        plt.savefig('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/graficas_radiacion/'+i+'.pdf' ,dpi = 100)
        plt.close()
        
        
        


##################Validación de la dirección del viento
        
    if i+'_Dir-vie-10min.csv' in lista_total:
        if i+'_Vel-vie-10min.csv' in lista_total:
            
            base_dir  = pd.read_csv(i+'_Dir-vie-10min.csv')                    
            
            acomodar(base_dir)
            
            
            #base2.columns.values[np.where(base2.columns.values == 'Dir-vie-10min')[0][0]] = 'dir_viento'
            #base_dir = base2.reset_index()[['date', 'dir_viento', 'vel_vi10' ]]  
            
            base_dir.columns.values[3] = 'dir_viento'
            base_dir.columns = base_dir.columns.str.strip()            
            
            
            base_vv = pd.read_csv(i+'_Vel-vie-10min.csv')
            acomodar(base_vv)

            
            #Quitar los no valores
            base_vv.columns.values[3] = 'vel_vi10'
            base_vv.columns = base_vv.columns.str.strip()
            
            base_dir = pd.merge(base_dir, base_vv, how = 'outer', on =['cod', 'date'])
            
            #No valores
            
            base_dir['null_1'] = np.where(((base_dir.dir_viento.isnull()) | base_dir.vel_vi10.isnull()), 1, 0)
            
            # Rangos
            
            base_dir['range'] = np.where((base_dir.dir_viento >= 0) & (base_dir.dir_viento <= 360), 0, 1)
# =============================================================================
#             
#             plt.plot_date(base_dir.date, base_dir.dir_viento)
#             plt.plot_date(base_dir[base_dir.range == 0].date, base_dir[base_dir.range == 0].dir_viento)
#                 
# =============================================================================
            
            ## Tabla de resumen para las estadísticas
            
            #if (n_datos - len(base_dir[base_dir.null_1 == 0])) < 0:
            n_datos = len(base_dir)
            
            dir_tabla = dir_tabla.append(pd.DataFrame([{'cod':i[0:8], #Código
               'isnull':(n_datos - len(base_dir[base_dir.null_1 == 0])),
               'total_isnull':n_datos,
               'range':base_dir[-base_dir.dir_viento.isnull()].range.sum(),
               'total_sinnan':len(base_dir[-base_dir.dir_viento.isnull()]),
               'No. datos':((n_datos - len(base_dir[base_dir.null_1 == 0])) *100)/n_datos,
               'P. Rango':((base_dir[-base_dir.dir_viento.isnull()].range.sum()) *100)/len(base_dir[-base_dir.dir_viento.isnull()]),
               'total_total':len(base_dir)}]))
            #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
            
            base_dir['val_dir'] = np.where(((base_dir.range == 0) & (base_dir.null_1 == 0)), 0, 1)
            
            base_dir_2 = base_dir[['cod', 'date', 'dir_viento', 'val_dir']]
            
            base_dir_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_val_dir.csv')
            base_dir.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_val_dir.csv')
        
    #######################################"###Validación de la temperatura
    
    if i+'_tmp_2m.csv' in lista_total:
        base2 = pd.read_csv(i+'_tmp_2m.csv')
        
        
        
        if not i+'_tmp_2m.csv' in lista_total:
            base2['tmp_2m'] = np.NaN
            
            
        if not i+'_tmp_2m_min.csv' in lista_total:
            base2['tmp_2m_min'] = np.NaN
        else: base2 = pd.merge(base2, pd.read_csv(i+'_tmp_2m_min.csv'), on=['date', 'cod'], how='outer')
            
            
        if not i+'_tmp_2m_max.csv' in lista_total:
            base2['tmp_2m_max'] = np.NaN
        else: base2 = pd.merge(base2, pd.read_csv(i+'_tmp_2m_max.csv'), on=['date', 'cod'], how='outer')
        
        #if (len(base2.tmp_2m) > 5) & (len(base2.tmp_2m_min) > 5) & (len(base2.tmp_2m_max) > 5):
            
        if (base2.tmp_2m.sum() == 0) & (base2.tmp_2m_min.sum() == 0) & (base2.tmp_2m_max.sum() == 0):
            continue
        
        #Creación de una sola columna de datos de temperatura
        a = base2[-base2.tmp_2m.isnull()][['date','tmp_2m']]
        a.columns = ['date','tmp_2m']
        b = base2[base2.tmp_2m.isnull()& -base2.tmp_2m_min.isnull()][['date','tmp_2m_min']]
        b.columns = ['date', 'tmp_2m']
        c = base2[base2.tmp_2m.isnull()& base2.tmp_2m_min.isnull() & -base2.tmp_2m_max.isnull()][['date','tmp_2m_max']]
        c.columns = ['date','tmp_2m']
        
        dd = pd.merge(on = 'date', left = a, right=b, how = 'outer') # Se pegan las bases para buscar los datos que no están en la base 1 pero están en la base 2
        dd.columns = ['date','tmp_2m_x','tmp_2m']
        
        ee = pd.concat([a, dd[dd.tmp_2m_x.isnull()][['date','tmp_2m']]])
        
        ff = pd.merge(on = 'date', left = ee, right=c, how = 'outer') # Se pegan las bases para buscar los datos que no están en la base 1 pero están en la base 2
        ff.columns = ['date','tmp_2m_x','tmp_2m']
        
        gg = pd.concat([ee, ff[ff.tmp_2m_x.isnull()][['date','tmp_2m']]])
        
        acomodar(gg)
        
        base_tmp = gg.sort_values(by='date', ascending=True)
        
        
        ##Quitar los valores que son na
        
        base_tmp['null_1'] = np.where(base_tmp.tmp_2m.isnull(), 1, 0)
        
        #Quitar los valores que se salen del rango
        
        base_tmp['range'] = np.where((base_tmp.tmp_2m >= -20) & (base_tmp.tmp_2m < 40), 0, 1)
        
        #Pruebas
        
        # Desviación estándar y Promedio
        base_tmp['mean_1'] = base_tmp.tmp_2m.rolling(window=9, center=True, min_periods=1).mean()
        base_tmp['std_2'] = base_tmp.tmp_2m.rolling(window=9, center=True, min_periods=1).std()
        
        #Spikes
        base_tmp['spikes_1'] = np.where((((base_tmp.mean_1 - (base_tmp.std_2 * 1)) > 
              base_tmp.tmp_2m) | (base_tmp.tmp_2m > (base_tmp.mean_1 + 
                    (base_tmp.std_2 * 1)))), 1,0)
        #Las diferencias no pueden ser superires a 4°C
        
        base_tmp['dif_0'] = ((abs((base_tmp[-base_tmp.tmp_2m.isnull()].tmp_2m) - (base_tmp[-base_tmp.tmp_2m.isnull()].tmp_2m.shift(1))) < 4))
        base_tmp['dif_1'] = np.where(base_tmp.dif_0 == True, 0, 1)
        
        
        # Probar que los sensores no estén pegados
        
        base_tmp['roll_1'] = np.where(((base_tmp.tmp_2m.rolling(window = 5, center = True).std())  > 0.01 ), 0, 1)
        
        base_tmp['rango_valores'] = np.where((((base_tmp.tmp_2m > 0.4)|(base_tmp.tmp_2m < 0.0))), 0, 1)
        
        ##Resultados finales
        
        base_tmp['val_tmp'] = np.where(((base_tmp.dif_1 == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.rango_valores == 0)), 0, 1)
        
        #if (n_datos - len(base_tmp[base_tmp.null_1 == 0])) < 0:
        n_datos = len(base_tmp)
        
        
        
        tmp_tabla = tmp_tabla.append(pd.DataFrame([{'cod':i[0:8], #Código
           'isnull':(n_datos - len(base_tmp[base_tmp.null_1 == 0])),
           'total_isnull':n_datos,
           'range':base_tmp[-base_tmp.tmp_2m.isnull()].range.sum(),
           'spikes':base_tmp[-base_tmp.tmp_2m.isnull()].spikes_1.sum(),
           'diff':base_tmp[-base_tmp.tmp_2m.isnull()].dif_1.sum(),
           'roll':base_tmp[-base_tmp.tmp_2m.isnull()].roll_1.sum(),
           'rango_valores':base_tmp[-base_tmp.tmp_2m.isnull()].rango_valores.sum(),
           'No. datos':((n_datos - len(base_tmp[base_tmp.null_1 == 0])) *100)/n_datos,
           'P. Rango':((base_tmp[-base_tmp.tmp_2m.isnull()].range.sum()) *100)/len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'P. spikes':((base_tmp[-base_tmp.tmp_2m.isnull()].spikes_1.sum()) *100)/len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'P. diferencia':((base_tmp[-base_tmp.tmp_2m.isnull()].dif_1.sum()) *100)/len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'P. roll':((base_tmp[-base_tmp.tmp_2m.isnull()].roll_1.sum()) *100)/len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'P. rango_val':((base_tmp[-base_tmp.tmp_2m.isnull()].rango_valores.sum()) *100)/len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'total_sinnan':len(base_tmp[-base_tmp.tmp_2m.isnull()]),
           'total_total':n_datos}]))
    
        #n_datos = ((base2.date.max() - base2.date.min())// datetime.timedelta(hours = 1))
        # =============================================================================
        # 
        # plt.plot_date(base_tmp.date, base_tmp.tmp_2m)
        # plt.plot_date(base_tmp[base_tmp.null_1 == 0].date, base_tmp[base_tmp.null_1 == 0].tmp_2m)
        # plt.plot_date(base_tmp[base_tmp.null_1 == 0][base_tmp.range == 0].date,
        #               base_tmp[base_tmp.null_1 == 0][base_tmp.range == 0].tmp_2m)
        # 
        # plt.plot_date(base_tmp[(base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].date, base_tmp[(base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].tmp_2m)
        # 
        # plt.plot_date(base_tmp[(base_tmp.dif_1 == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].date,
        #                        base_tmp[(base_tmp.dif_1 == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].tmp_2m)
        # 
        # plt.plot_date(base_tmp[(base_tmp.roll_1 == 0) & (base_tmp.dif_1 == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].date,
        #                        base_tmp[(base_tmp.roll_1 == 0) & (base_tmp.dif_1 == 0) & (base_tmp.spikes_1 == 0) & (base_tmp.null_1 == 0) & (base_tmp.range == 0) & (base_tmp.spikes_1 == 0)].tmp_2m)
        # 
        # =============================================================================
        
        base_tmp_2 = base_tmp[['date','tmp_2m','val_tmp']]
        
        #base2 = pd.merge(on = 'date', left= base2, right= base_tmp[['date','tmp_2m','val_tmp']]) # une la nueva temperatura con la base que se viene trabajando
        
        #base2.tmp_2m_x = base2.tmp_2m_y # Se cambia la variable de temperatura
        
        #base2 = base2.drop(['tmp_2m_y'], axis=1) # Se elimina la columna de exceso 
        
        #base2.columns.values[np.where(base2.columns == 'tmp_2m_x')[0][0]] = 'tmp_2m' 
        
        base_tmp_2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/' +'v_'+i+'_tmp_2m.csv')
        base_tmp.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col1/' +'v_'+i+'_tmp_2m.csv')

        
    #base2.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_validados_20180620/' +i[0:8]+ '.csv')
    
    ##Salidas de las bases de temperatura y otras

###Tablas resúmen de la validación   
#humedad_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'humedad_v'+ '.csv')
humedad_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'humedad_v'+ '.csv')
#prec_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'precip_v' +'.csv')
prec_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'precip_v' +'.csv')
#vv_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'vv_v' +'.csv')
vv_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'vv_v' +'.csv')
#rad_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'rad_v' +'.csv')
rad_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'rad_v' +'.csv')
#dir_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'dir_tabla_v' +'.csv')
dir_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'dir_tabla_v' +'.csv')
#tmp_tabla.to_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'tmp_tabla_v' +'.csv')
tmp_tabla = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/estadisticas_validacion/' +'tmp_tabla_v' +'.csv')

len(dir_tabla)
lista_nombres(dir_tabla)
dir_tabla[dir_tabla.iloc[:,2] ==dir_tabla.iloc[:,2].max()]
dir_tabla.sort_values(by='No. datos', ascending=False)
dir_tabla.sort_values(by='P. Rango', ascending=False)
dir_tabla.sort_values(by='P. cielo despejado', ascending=False)


un_busca_cod(cod=21206980)  
un_busca_cod(cod=21205012)  

def busca_cod(base_1, col_cod='cod'):
    #Función creada para buscar los nombres de las estaciones automáticas o convencionales a partír del código
    ## tmp_tabla = busca_cod(tmp_tabla, 'cod')
    
    lista_estaciones = pd.read_csv('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/est_usadas_lista.csv')
    lista_estaciones.columns.values[0] = 'cod_1'
    lista_estaciones.columns = lista_estaciones.columns.str.strip()
    lista_estaciones.columns.values[1] = 'Nombre'
    
    name_0 = pd.merge(left=base_1, right=lista_estaciones, 
                    left_on=col_cod, right_on='cod_1', how='left')
    
    return(name_0)
    #busca_cod(tmp_tabla, 'cod')
        


        

tmp_tabla = tmp_tabla.iloc[:,1:]
tmp_tabla = busca_cod(tmp_tabla, 'cod')
print(tmp_tabla[['Nombre', 'No. datos', 'P. Rango', 'P. diferencia', 'P. roll', 'P. spikes', 'P. rango_val','total_total']].iloc[1:,].round(2).to_latex(index = False, longtable=True))
15,0,1,2,3,4,11
humedad_tabla = humedad_tabla.iloc[:,1:]
humedad_tabla = busca_cod(humedad_tabla, 'cod')
print(humedad_tabla.iloc[1:,[11,0,1,2,7]].round(2).to_latex(index = False))

prec_tabla = prec_tabla.iloc[:,2:]
prec_tabla = busca_cod(prec_tabla)
print(prec_tabla.iloc[1:,[9,0,1,5]].round(2).to_latex(index = False))

rad_tabla = rad_tabla.iloc[:,2:]
rad_tabla = busca_cod(rad_tabla)
print(rad_tabla.iloc[1:,[13,0,1,2,3,9]].round(2).to_latex(index = False))

vv_tabla = vv_tabla.iloc[:,2:]
vv_tabla = busca_cod(vv_tabla)
print(vv_tabla.iloc[1:,[13,0,1,2,3,9]].round(2).to_latex(index = False))



dir_tabla = dir_tabla.iloc[:,2:]
dir_tabla = busca_cod(dir_tabla)
print(dir_tabla.iloc[1:,[9,0,1,5]].round(2).to_latex(index = False))



os.chdir('/media/edwin/6F71AD994355D30E/Edwin/Maestría Meteorologia/Tesis/datos_ideam/validados_col_col/')

lista_total = os.listdir()

lista_codigos = pd.DataFrame({'a':os.listdir()}).a.str[2:10].unique()
lista_var = pd.DataFrame({'a':os.listdir()}).a.str[11:-4].unique()

def union_variables:
    for i in lista_codigos:
        
        for j in lista_var:
            print(i, j)
            
            if not 'v_'+i+'_'+j+'.csv' in lista_total:
                continue
            base = pd.read_csv('v_'+i+'_'+j+'.csv')
            
            base.
            


