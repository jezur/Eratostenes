import numpy as np
import pandas as pd
import itertools


types = {
    'fecha'      : 'datetime64',
    'hora'       : 'str',
    'latitud'    : 'float', 
    'longitud'   : 'float',
    'l'          : 'float', # cm
    'r'          : 'float', # cm
    'sitio'      : 'str'}


def preprocesamiento(df):
    base_dt = pd.to_datetime('00:00:00')
    df = df.astype(types)
    dat = df.copy()
    dat.dropna(inplace=True)
    dat['l']       = dat['l']/100 # a metros
    dat['r']       = dat['r']/100 # a metros
    dat['angulo']  = np.arctan(dat['r'] / dat['l']) * 180 / np.pi
    return dat


def comparaciones_old(data):
    '''
    Criterio: Si tiene misma hora, y diferente latitud, entonces sirve para el
    cómputo del radio de la Tierra.'''
    tiempos = list(data['hora'].unique())
    
    comparaciones_ok = []
    comparaciones_id = []
    for time in tiempos:
        data_test = data[data['hora'] == time]
        data_test = [tuple(x) for x in data_test[['id','hora', 'latitud']].to_numpy()]
        for element in itertools.product(*[data_test, data_test]):
            if element[0][-1] != element[1][-1]:
                comparaciones_ok.append(element)
                comparaciones_id.append((element[0][0], element[1][0]))
                
    comparaciones_ok = set(map(lambda x: tuple(sorted(x)),comparaciones_ok))
    comparaciones_id = set(map(lambda x: tuple(sorted(x)),comparaciones_id))
                
    return comparaciones_ok, comparaciones_id


def comparaciones(data):
    '''
    Criterio: Si tiene misma hora, diferente latitud y diferente sitio, entonces
    sirve para el cómputo del radio de la Tierra.'''
    tiempos = list(data['hora'].unique())
    
    comparaciones_ok = []
    comparaciones_id = []
    for time in tiempos:
        data_test = data[data['hora'] == time]
        data_test = [tuple(x) for x in data_test[['id','sitio', 'hora', 'latitud']].to_numpy()]
        for element in itertools.product(*[data_test, data_test]):
            if element[0][1] != element[1][1]:
                if element[0][-1] != element[1][-1]:
                    comparaciones_ok.append(element)
                    comparaciones_id.append((element[0][0], element[1][0]))
                
    comparaciones_ok = list(set(map(lambda x: tuple(sorted(x)),comparaciones_ok)))
    comparaciones_id = list(set(map(lambda x: tuple(sorted(x)),comparaciones_id)))
                
    return comparaciones_ok, comparaciones_id


def eratostenes(data, comparaciones_ok):
    eratostenes = []
    for comps in comparaciones_ok:
        a, b, sitio_a, sitio_b = comps[0][0], comps[1][0], comps[0][1], comps[1][1]
        df     = data.filter(items = [a, b], axis=0).T
        latdif = np.abs(df[a].loc['latitud'] - df[b].loc['latitud'])
        angdif = np.abs(df[a].loc['angulo'] - df[b].loc['angulo'])
        timedif= np.abs(df[a].loc['fecha'] - df[b].loc['fecha'])
        dns    = 40030 * latdif / 360 
        circ   = dns * 360 / angdif
        radio  = circ / 2 / np.pi
        eratostenes.append([a, sitio_a, b, sitio_b, latdif, timedif, dns, angdif, circ, radio])
        
    eratoscols  = ['ID 1','sitio 1','ID 2','sitio 2','latdif','timedif','dns','angdif','circ','radio']
    return pd.DataFrame(data=eratostenes, columns=eratoscols)


def estadísticas(df):
    rad_avg = df['radio'].mean()
    cir_avg = df['circ'].mean()
    rad_std = df['radio'].std()
    cir_std = df['circ'].std()
    realcir = 40030.0
    realrad = realcir/2/np.pi
    sampsze = len(df)
    
    # ERRORES
    error_est = cir_std / np.sqrt(sampsze)
    error_exp = np.abs(realcir - cir_avg) * 100 / realcir
    print('Circunferencia Media : {:.2f} +- {:.2f} km'.format(cir_avg, cir_std))
    print('Radio Tierra Medio   :  {:.2f} +- {:.2f}  km'.format(rad_avg, rad_std))
    print('Número de cálculos   :  {}'.format(sampsze))
    print('Error estadístico    :  {:.2f}'.format(error_est))
    print('Error experimental   :  {:.2f} %'.format(error_exp))
    

def shadow_time_plot(df):
    '''
    For same date and location: time vs shadow length
    1. Tomar database principal, hacer tuplas de uniques de fecha y ubicacion
    2. Para cada tupla seleccionar las bases de datos que tengan esa data. Hacer subsets
    3. Plotear cada subset en un mesh 
    Luego ver si hay coincidencia con días que son nublados
    '''
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    fig.set_facecolor('white')
    
    
    
    
    
    
    
    
    
    
    
    
    
    