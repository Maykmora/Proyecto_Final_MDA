import os
from datetime import datetime


def obtener_informacion(ruta):
    informacion = {"nombre": os.path.basename(ruta), "existe": os.path.exists(ruta)}

    if not informacion["existe"]:
        return informacion

    datos = os.stat(ruta)
    informacion["tamano"] = datos.st_size
    informacion["modificado"] = datetime.fromtimestamp(datos.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
    informacion["lectura"] = os.access(ruta, os.R_OK)
    informacion["escritura"] = os.access(ruta, os.W_OK)

    return informacion


def obtener_informacion_archivos(rutas):
    lista = []
    for ruta in rutas:
        lista.append(obtener_informacion(ruta))
    return lista