# Autorenovación MIL ANUNCIOS.com

[![Build Status](https://travis-ci.org/3clypse/milanuncios.svg?branch=master)](https://travis-ci.org/3clypse/milanuncios)

Autorenovación de anuncios de [MIL ANUNCIOS.com] (http://www.milanuncios.com/).

## NO. No commercial use allowed! 

## Prequisitos

 * Python 2.7 o python 3.5
 * [requests] (http://docs.python-requests.org/)

## Instalación

```
sudo pip install -r requirements.txt
```

## Uso

- Añade tus credenciales en las claves *email* y *contra* del diccionario *payload*.
- Ejecutar el script:

```
python renew.py
```

Una forma de automatizar el proceso es añadir una tarea cron cada 24 horas.

