import os

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CONTACTOS = os.path.join(CARPETA, "contactos.dat")

CAMPOS = ["id", "nombre", "telefono", "correo", "ciudad"]

LARGOS = {
    "id": 5,
    "nombre": 30,
    "telefono": 15,
    "correo": 35,
    "ciudad": 14,
}

TAMANO_REGISTRO = 100

def ajustar_campo(texto, largo):
    datos = texto.encode("utf-8")
    return datos + b" " * (largo - len(datos))

def validar_largos(contacto):
    for campo in CAMPOS:
        datos = str(contacto[campo]).encode("utf-8")
        if len(datos) > LARGOS[campo]:
            return ("El campo " + campo + " no puede ocupar más de "
                    + str(LARGOS[campo]) + " bytes.")
    return ""

def construir_registro(contacto):
    registro = b""
    for campo in CAMPOS:
        registro = registro + ajustar_campo(str(contacto[campo]), LARGOS[campo])
    registro = registro + b"\n"
    return registro

def convertir_registro(datos):
    contacto = {}
    posicion = 0
    for campo in CAMPOS:
        trozo = datos[posicion:posicion + LARGOS[campo]]
        contacto[campo] = trozo.decode("utf-8").strip()
        posicion = posicion + LARGOS[campo]
    contacto["id"] = int(contacto["id"])
    return contacto

def contar_registros():
    if not os.path.exists(ARCHIVO_CONTACTOS):
        return 0
    tamano = os.path.getsize(ARCHIVO_CONTACTOS)
    if tamano % TAMANO_REGISTRO != 0:
        raise ValueError("El tamaño del archivo no es múltiplo de "
                         + str(TAMANO_REGISTRO) + " bytes.")
    return tamano // TAMANO_REGISTRO

def leer_registro(numero):
    with open(ARCHIVO_CONTACTOS, "rb") as archivo:
        archivo.seek(numero * TAMANO_REGISTRO)
        posicion_inicial = archivo.tell()
        datos = archivo.read(TAMANO_REGISTRO)
        posicion_final = archivo.tell()

    if len(datos) != TAMANO_REGISTRO:
        raise ValueError("El registro " + str(numero) + " está incompleto.")

    contacto = convertir_registro(datos)
    return contacto, posicion_inicial, posicion_final

def buscar_por_id(id_buscado):
    total = contar_registros()
    for numero in range(total):
        contacto, inicio, fin = leer_registro(numero)
        if contacto["id"] == id_buscado:
            return numero, contacto, inicio, fin
    return None

def agregar_contacto(contacto):
    if buscar_por_id(contacto["id"]) is not None:
        return None

    numero = contar_registros()
    registro = construir_registro(contacto)

    if not os.path.exists(ARCHIVO_CONTACTOS):
        with open(ARCHIVO_CONTACTOS, "wb") as archivo:
            pass

    with open(ARCHIVO_CONTACTOS, "r+b") as archivo:
        archivo.seek(numero * TAMANO_REGISTRO)
        inicio = archivo.tell()
        archivo.write(registro)
        fin = archivo.tell()

    return numero, inicio, fin

def modificar_contacto(contacto):
    resultado = buscar_por_id(contacto["id"])
    if resultado is None:
        return None

    numero = resultado[0]
    registro = construir_registro(contacto)

    with open(ARCHIVO_CONTACTOS, "r+b") as archivo:
        archivo.seek(numero * TAMANO_REGISTRO)
        inicio = archivo.tell()
        archivo.write(registro)
        fin = archivo.tell()

    return numero, inicio, fin

def listar_contactos():
    lista = []
    total = contar_registros()
    for numero in range(total):
        contacto, inicio, fin = leer_registro(numero)
        lista.append((numero, contacto, inicio))
    return lista