#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import datetime
import os
import random
import time
import re
from dotenv import load_dotenv, find_dotenv
import requests

load_dotenv(find_dotenv())

DEBUG_MODE = True if os.environ.get('DEBUG') == 'True' else False

URL = {
    'login': 'https://www.milanuncios.com/cmd/',
    'advertisements_list': 'http://www.milanuncios.com/mis-anuncios/',
    'advertisement_values': 'http://www.milanuncios.com/renovar/',
    'renew': 'http://www.milanuncios.com/renovado/'
}


PAYLOAD = {
    'login': {
        'comando': 'login',
        'email': os.environ.get('EMAIL'),
        'contra': os.environ.get('PASSWORD'),
        'rememberme': 's'
    },
    'advertisement_values': {
        'id': None
    },
    'renew': {
        'comando': 'renovar',
        'a': None,
        't': None,
        'u': None,
        'id': None
    }
}

RENEW_RESPONSE = {
    'renovado': 'Anuncio renovado.',
    'pronto': 'Aún es pronto, debes esperar 24h entre cada renovación.',
    'error': 'Error renovando el anuncio.'
}


def time_stamped(fname="", fmt='%d/%m/%Y | %H:%M:%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def login():
    response = requests.post(URL['login'], data=PAYLOAD['login'])
    return response.cookies


def get_advertisements_id(cookie):
    response = requests.get(URL['advertisements_list'], cookies=cookie)
    return re.findall(r"(?<=\?idanuncio=)(\d{9})(?=&)",
                      response.text.encode('utf-8'))


def wait_until():
    rnd = random.randint(3, 10)
    print('[' + time_stamped() + '] Esperando ' + str(rnd) +
          ' segundos para renovar.')
    time.sleep(rnd)


def get_advertisement_values(cookie, advertisement_id):
    PAYLOAD['advertisement_values']['id'] = advertisement_id
    response = requests.get(
        URL['advertisement_values'],
        params=PAYLOAD['advertisement_values'],
        cookies=cookie)
    obfuscated_code = re.findall(r"(?<=unescape\(')(.+?)(?=')", response.text)
    try:
        obfuscated_code = obfuscated_code[1].decode('unicode-escape')
    except IndexError:
        print('Error al acceder al índice. Cerrando el programa...')
        exit()
    short_hashes = re.findall("[a-z0-9]{32}", obfuscated_code)
    long_hash = re.findall("[a-z0-9]{96}", obfuscated_code)
    return (short_hashes[1].encode('utf-8'), short_hashes[0].encode('utf-8'),
            long_hash[0].encode('utf-8'))


def renew(cookie, advertisement_values, advertisement_id):
    PAYLOAD['renew']['a'] = advertisement_values[0]
    PAYLOAD['renew']['u'] = advertisement_values[1]
    PAYLOAD['renew']['t'] = advertisement_values[2]
    PAYLOAD['renew']['id'] = advertisement_id
    response = requests.get(URL['renew'], PAYLOAD['renew'], cookies=cookie)
    return response.text


def main():
    cookie = login()
    if not cookie.values():
        print('[' + time_stamped() + '] No se pudo iniciar sesión. Comprueba'
              ' las credenciales.')
    else:
        advertisements_id = get_advertisements_id(cookie)
        number_advertisements = len(advertisements_id)
        if number_advertisements == 0:
            print('[' + time_stamped() + '] No tienes anuncios.')
        else:
            print('[' + time_stamped() + '] %d anuncios obtenidos:'
                  % number_advertisements)
            for advertisement_id in advertisements_id:
                if not DEBUG_MODE and number_advertisements > 1:
                    wait_until()
                values = get_advertisement_values(cookie, advertisement_id)
                if DEBUG_MODE:
                    print(values)
                response = renew(cookie, values, advertisement_id)
                print('[' + time_stamped() + '] Anuncio con referencia %s'
                      % advertisement_id + ' - ' +
                      RENEW_RESPONSE.get(response, 'error'))

if __name__ == "__main__":
    main()
