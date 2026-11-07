import os
import json

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_INDICE = os.path.join(CARPETA, "indice.json")
ARCHIVO_TEMPORAL = os.path.join(CARPETA, "indice.tmp")


def guardar_indice(datos_indice):
    with open(ARCHIVO_TEMPORAL, "w", encoding="utf-8") as archivo:
        json.dump(datos_indice, archivo, indent=2)
    os.replace(ARCHIVO_TEMPORAL, ARCHIVO_INDICE)


def cargar_indice():
    with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
        datos_indice = json.load(archivo)

    if not isinstance(datos_indice, dict):
        raise ValueError("El índice no tiene el formato correcto.")

    for clave in datos_indice:
        valor = datos_indice[clave]
        if not clave.isdigit() or not isinstance(valor, int) or valor < 0:
            raise ValueError("El índice tiene datos incorrectos.")

    return datos_indice