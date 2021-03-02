#!/usr/bin/env python 
import requests
import json
from credentials import *

def rotate(uid):
        rotated =''
        for i in range(0,8,2):
            rotated = uid[0+i:2+i]+rotated
        return rotated

def get_data(uid):
    rotated = False
    url_tarjeta_uc = 'https://api.uc.cl/tarjetauc/v1/user/{0}?buscar=mifare'.format(uid)
    uc_card = requests.get(url_tarjeta_uc, headers = tarjeta_uc_credential).json()
    print(uc_card)
    if uc_card['status']==300:
        rotated = True
        print("rotated")
        url_tarjeta_uc = 'https://api.uc.cl/tarjetauc/v1/user/{0}?buscar=mifare'.format(rotate(uid))
        new_uc_card = requests.get(url_tarjeta_uc, headers = tarjeta_uc_credential).json()
        data_tarjeta = new_uc_card['tarjetauc']['data']        
    else:
        
        data_tarjeta = uc_card['tarjetauc']['data']
        
    if isinstance(data_tarjeta, str):
        return data_tarjeta

    run = data_tarjeta['run']
    url_personas_uc = 'https://api.uc.cl/personauc/v1/user/{0}'.format(run)
    persona_uc  = requests.get(url_personas_uc, headers = persona_uc_credential).json()
    data = persona_uc['datos_personales']['data']
    source = data['tarjetauc']['data']
    if not data['tarjetauc']['data']['cod_mifare']:
        source = data_tarjeta
    return {'rfid':  source['cod_mifare'] if not rotated else rotate(source['cod_mifare']),
            'nombre': source['nombre_titular'],
            'correo': data['login']+'@uc.cl',
            'rut': data_tarjeta['run'][:-1]+'-'+ data_tarjeta['run'][-1],
            'sit_academica': data['rol'][0]['estado']}
    
