#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import re
import requests
import time

url = {
    'login': 'http://www.milanuncios.com/cmd/',
    'advertisements_list': 'http://www.milanuncios.com/mis-anuncios/',
    'advertisement_values': 'http://www.milanuncios.com/renovar/',
    'renew': 'http://www.milanuncios.com/renovado/'
}

payload = {
    'login': {
        'comando': 'login',
        'email': 'YOUR@EMAIL.COM',
        'contra': 'TU CONTRASEÑA',
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

renew_responses = {
    'renovado': 'Anuncio renovado.',
    'pronto': 'Aún es pronto, debes esperar 24h entre cada renovación.',
    'error': 'Error renovando el anuncio.'
}


def timeStamped(fname="", fmt='%d/%m/%Y | %H:%M:%S'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def login():
    response = requests.get(url['login'], params=payload['login'])
    return response.cookies


def get_advertisements_id(cookie):
    response = requests.get(url['advertisements_list'], cookies=cookie)
    return re.findall(
        "(?<=\?idanuncio=)(\d{9})(?=&)", response.text.encode('utf-8'))


def waitUntil():
    rnd = random.randint(5, 60)
    time.sleep(rnd)


def get_advertisement_values(cookie, advertisement_id):
    payload['advertisement_values']['id'] = advertisement_id
    response = requests.get(
        url['advertisement_values'],
        params=payload['advertisement_values'],
        cookies=cookie)
    obfuscated_code = re.findall(
        "(?<=unescape\(')(.+?)(?=')", response.text)
    obfuscated_code = obfuscated_code[1].decode('unicode-escape')
    short_hashes = re.findall("[a-z0-9]{32}", obfuscated_code)
    long_hash = re.findall("[a-z0-9]{96}", obfuscated_code)
    return (short_hashes[1].encode('utf-8'), short_hashes[0].encode('utf-8'),
            long_hash[0].encode('utf-8'))


def renew(cookie, advertisement_values, advertisement_id):
    payload['renew']['a'] = advertisement_values[0]
    payload['renew']['u'] = advertisement_values[1]
    payload['renew']['t'] = advertisement_values[2]
    payload['renew']['id'] = advertisement_id
    response = requests.get(url['renew'], payload['renew'], cookies=cookie)
    return response.text


def main():
    cookie = login()
    if not cookie.values():
        print('[' + timeStamped() + '] No se pudo iniciar sesión. Comprueba'
              ' las credenciales.')
    else:
        ids = get_advertisements_id(cookie)
        number_advertisements = len(ids)
        if number_advertisements == 0:
            print('[' + timeStamped() + '] No tienes anuncios.')
        else:
            print('[' + timeStamped() + '] %d anuncios obtenidos:'
                  % number_advertisements)
            for id in ids:
                if ids.index(id) == 0:
                    values = get_advertisement_values(cookie, id)
                    response = renew(cookie, values, id)
                    print('[' + timeStamped() + '] Anuncio con referencia %s'
                          % id + ' - ' + renew_responses.get(response, 'error'))
                else:
                    waitUntil()
                    values = get_advertisement_values(cookie, id)
                    response = renew(cookie, values, id)
                    print('[' + timeStamped() + '] Anuncio con referencia %s'
                          % id + ' - ' + renew_responses.get(response, 'error'))

if __name__ == "__main__":
    main()
