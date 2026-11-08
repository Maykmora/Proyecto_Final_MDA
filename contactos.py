import os
import indice
import integridad

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

avisos = []

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

def reconstruir_indice(motivo):
    datos_indice = {}
    total = contar_registros()
    for numero in range(total):
        contacto, inicio, fin = leer_registro(numero)
        datos_indice[str(contacto["id"])] = numero

    indice.guardar_indice(datos_indice)
    avisos.append("El índice " + motivo + ".\nSe reconstruyó leyendo el archivo de contactos.")
    return datos_indice

def obtener_indice():
    total = contar_registros()
    try:
        datos_indice = indice.cargar_indice()
    except FileNotFoundError:
        if total == 0:
            return {}
        return reconstruir_indice("no existía")
    except ValueError:
        return reconstruir_indice("estaba dañado")

    if len(datos_indice) != total:
        return reconstruir_indice("no coincidía con la cantidad de contactos del archivo")

    return datos_indice

def leer_con_indice(numero, id_buscado):
    if numero >= contar_registros():
        return None
    contacto, inicio, fin = leer_registro(numero)
    if contacto["id"] != id_buscado:
        return None
    return contacto, inicio, fin

def buscar_por_id(id_buscado):
    datos_indice = obtener_indice()
    clave = str(id_buscado)

    if clave not in datos_indice:
        return None

    numero = datos_indice[clave]
    resultado = leer_con_indice(numero, id_buscado)

    if resultado is None:
        datos_indice = reconstruir_indice("tenía posiciones que no coinciden con el archivo")
        if clave not in datos_indice:
            return None
        numero = datos_indice[clave]
        resultado = leer_con_indice(numero, id_buscado)
        if resultado is None:
            return None

    contacto, inicio, fin = resultado
    return numero, contacto, inicio, fin

def agregar_contacto(contacto):
    datos_indice = obtener_indice()
    clave = str(contacto["id"])

    if clave in datos_indice:
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

    datos_indice[clave] = numero
    indice.guardar_indice(datos_indice)
    integridad.guardar_hash(ARCHIVO_CONTACTOS)

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

    integridad.guardar_hash(ARCHIVO_CONTACTOS)
    return numero, inicio, fin

def listar_contactos():
    lista = []
    total = contar_registros()
    for numero in range(total):
        contacto, inicio, fin = leer_registro(numero)
        lista.append((numero, contacto, inicio))
    return lista