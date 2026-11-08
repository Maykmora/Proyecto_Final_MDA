import os

CARPETA_SRC = os.path.dirname(os.path.abspath(__file__))
CARPETA_PROYECTO = os.path.dirname(CARPETA_SRC)
CARPETA_DATOS = os.path.join(CARPETA_PROYECTO, "data")
CARPETA_REPORTES = os.path.join(CARPETA_PROYECTO, "reports")


def crear_carpetas():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    os.makedirs(CARPETA_REPORTES, exist_ok=True)