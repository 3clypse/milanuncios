#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import random
import time
import re
import requests

URL = {
    'login': 'http://www.milanuncios.com/cmd/',
    'advertisements_list': 'http://www.milanuncios.com/mis-anuncios/',
    'advertisement_values': 'http://www.milanuncios.com/renovar/',
    'renew': 'http://www.milanuncios.com/renovado/'
}

PAYLOAD = {
    'login': {
        'comando': 'login',
        'email': 'TU@EMAIL.COM',
        'contra': 'TUCONTRASENA',
        'rememberme': 's'
    },
    'advertisement_values': {
        'id_advertisement': None
    },
    'renew': {
        'comando': 'renovar',
        'a': None,
        't': None,
        'u': None,
        'id_advertisement': None
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
    response = requests.get(URL['login'], params=PAYLOAD['login'])
    return response.cookies


def get_advertisements_id(cookie):
    response = requests.get(URL['advertisements_list'], cookies=cookie)
    return re.findall(
        r"(?<=\?idanuncio=)(\d{9})(?=&)", response.text.encode('utf-8'))


def wait_until():
    rnd = random.randint(5, 60)
    time.sleep(rnd)


def get_advertisement_values(cookie, advertisement_id):
    PAYLOAD['advertisement_values']['id_advertisement'] = advertisement_id
    response = requests.get(
        URL['advertisement_values'],
        params=PAYLOAD['advertisement_values'],
        cookies=cookie)
    obfuscated_code = re.findall(r"(?<=unescape\(')(.+?)(?=')", response.text)
    obfuscated_code = obfuscated_code[1].decode('unicode-escape')
    short_hashes = re.findall("[a-z0-9]{32}", obfuscated_code)
    long_hash = re.findall("[a-z0-9]{96}", obfuscated_code)
    return (short_hashes[1].encode('utf-8'), short_hashes[0].encode('utf-8'),
            long_hash[0].encode('utf-8'))


def renew(cookie, advertisement_values, advertisement_id):
    PAYLOAD['renew']['a'] = advertisement_values[0]
    PAYLOAD['renew']['u'] = advertisement_values[1]
    PAYLOAD['renew']['t'] = advertisement_values[2]
    PAYLOAD['renew']['id_advertisement'] = advertisement_id
    response = requests.get(URL['renew'], PAYLOAD['renew'], cookies=cookie)
    return response.text


def main():
    cookie = login()
    if not cookie.values():
        print('[' + time_stamped() + '] No se pudo iniciar sesión. Comprueba'
              ' las credenciales.')
    else:
        id_advertisements = get_advertisements_id(cookie)
        number_advertisements = len(id_advertisements)
        if number_advertisements == 0:
            print('[' + time_stamped() + '] No tienes anuncios.')
        else:
            print('[' + time_stamped() + '] %d anuncios obtenidos:'
                  % number_advertisements)
            for id_advertisement in id_advertisements:
                if id_advertisements.index(id_advertisement) == 0:
                    values = get_advertisement_values(cookie, id_advertisement)
                    response = renew(cookie, values, id_advertisement)
                    print('[' + time_stamped() + '] Anuncio con referencia %s'
                          % id_advertisement + ' - ' +
                          RENEW_RESPONSE.get(response, 'error'))
                else:
                    wait_until()
                    values = get_advertisement_values(cookie, id_advertisement)
                    response = renew(cookie, values, id_advertisement)
                    print('[' + time_stamped() + '] Anuncio con referencia %s'
                          % id_advertisement + ' - ' +
                          RENEW_RESPONSE.get(response, 'error'))

if __name__ == "__main__":
    main()
