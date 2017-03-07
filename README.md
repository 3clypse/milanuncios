# Autorenovación MIL ANUNCIOS.com

[![Build Status](https://travis-ci.org/3clypse/milanuncios.svg?branch=master)](https://travis-ci.org/3clypse/milanuncios)

Autorenovación de anuncios de [MIL ANUNCIOS.com](http://www.milanuncios.com/).

## NO. ¡No permitimos un uso comercial!

## Prequisitos

-   Python 2.7
-   [pip](https://pip.pypa.io/en/stable/)

## Instalación

```
sudo pip install -r requirements.txt
```

## Uso

-   Copia el archivo `.env.example` a `.env`
-   Añade tus credenciales en el fichero `.env`
-   Ejecuta el script:

```
python renew.py
```

Una forma de automatizar el proceso es añadir una tarea cron cada 24 horas.
