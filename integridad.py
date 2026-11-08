import os
import hashlib
import zipfile
from datetime import datetime

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_HASH = os.path.join(CARPETA, "contactos.sha256")
ARCHIVO_HASH_TEMPORAL = os.path.join(CARPETA, "contactos.sha256.tmp")


def calcular_hash(ruta_archivo):
    sha256 = hashlib.sha256()
    with open(ruta_archivo, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)
            if not bloque:
                break
            sha256.update(bloque)
    return sha256.hexdigest()


def guardar_hash(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return ""

    hash_actual = calcular_hash(ruta_archivo)

    with open(ARCHIVO_HASH_TEMPORAL, "w", encoding="utf-8") as archivo:
        archivo.write(hash_actual)
    os.replace(ARCHIVO_HASH_TEMPORAL, ARCHIVO_HASH)

    return hash_actual


def leer_hash_guardado():
    if not os.path.exists(ARCHIVO_HASH):
        return None
    with open(ARCHIVO_HASH, "r", encoding="utf-8") as archivo:
        return archivo.read().strip()


def hash_valido(texto):
    if len(texto) != 64:
        return False
    for letra in texto:
        if letra not in "0123456789abcdef":
            return False
    return True


def verificar_integridad(ruta_archivo):
    hash_guardado = leer_hash_guardado()

    if not os.path.exists(ruta_archivo):
        if hash_guardado is None:
            return "sin_datos", "", ""
        return "archivo_faltante", hash_guardado, ""

    hash_actual = calcular_hash(ruta_archivo)

    if hash_guardado is None or not hash_valido(hash_guardado):
        guardar_hash(ruta_archivo)
        return "hash_creado", "", hash_actual

    if hash_actual == hash_guardado:
        return "correcto", hash_guardado, hash_actual

    return "modificado", hash_guardado, hash_actual


def crear_respaldo(rutas):
    existentes = []
    for ruta in rutas:
        if os.path.exists(ruta):
            existentes.append(ruta)

    if len(existentes) == 0:
        return None

    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_zip = os.path.join(CARPETA, "respaldo_" + marca + ".zip")

    detalle = []
    tamano_original = 0
    tamano_comprimido = 0

    with zipfile.ZipFile(ruta_zip, "w", zipfile.ZIP_DEFLATED) as respaldo:
        for ruta in existentes:
            respaldo.write(ruta, os.path.basename(ruta))

        for info in respaldo.infolist():
            detalle.append((info.filename, info.file_size, info.compress_size))
            tamano_original = tamano_original + info.file_size
            tamano_comprimido = tamano_comprimido + info.compress_size

    tamano_zip = os.path.getsize(ruta_zip)

    return ruta_zip, detalle, tamano_original, tamano_comprimido, tamano_zip