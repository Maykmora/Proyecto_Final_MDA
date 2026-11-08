import os
import json
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import contactos

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_JSON = os.path.join(CARPETA, "contactos.json")
ARCHIVO_JSON_TEMPORAL = os.path.join(CARPETA, "contactos.tmp")
ARCHIVO_PDF = os.path.join(CARPETA, "reporte_contactos.pdf")


def obtener_lista_contactos():
    lista = []
    for numero, contacto, inicio in contactos.listar_contactos():
        lista.append(contacto)
    return lista


def exportar_json():
    lista = obtener_lista_contactos()

    if len(lista) == 0:
        return 0

    with open(ARCHIVO_JSON_TEMPORAL, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, ensure_ascii=False, indent=4)
    os.replace(ARCHIVO_JSON_TEMPORAL, ARCHIVO_JSON)

    return len(lista)


def validar_lista(lista):
    if not isinstance(lista, list):
        raise ValueError("El archivo JSON no tiene el formato esperado.")

    for contacto in lista:
        if not isinstance(contacto, dict):
            raise ValueError("El archivo JSON no tiene el formato esperado.")
        for campo in contactos.CAMPOS:
            if campo not in contacto:
                raise ValueError("A un contacto del JSON le falta el campo " + campo + ".")


def dibujar_encabezado_tabla(pdf, y):
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(40, y, "ID")
    pdf.drawString(80, y, "Nombre")
    pdf.drawString(235, y, "Teléfono")
    pdf.drawString(315, y, "Correo")
    pdf.drawString(485, y, "Ciudad")
    pdf.line(40, y - 5, 572, y - 5)
    pdf.setFont("Helvetica", 9)


def dibujar_numero_pagina(pdf, numero_pagina):
    pdf.setFont("Helvetica", 9)
    pdf.drawString(500, 25, "Página " + str(numero_pagina))


def generar_pdf():
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        lista = json.load(archivo)

    validar_lista(lista)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    pdf = canvas.Canvas(ARCHIVO_PDF, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, 750, "Reporte de contactos")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, 730, "Fecha de generación: " + fecha)
    pdf.drawString(40, 716, "Total de contactos: " + str(len(lista)))

    y = 685
    dibujar_encabezado_tabla(pdf, y)
    y = y - 24
    numero_pagina = 1

    for contacto in lista:
        if y < 50:
            dibujar_numero_pagina(pdf, numero_pagina)
            pdf.showPage()
            numero_pagina = numero_pagina + 1
            y = 750
            dibujar_encabezado_tabla(pdf, y)
            y = y - 24

        pdf.drawString(40, y, str(contacto["id"]))
        pdf.drawString(80, y, contacto["nombre"])
        pdf.drawString(235, y, contacto["telefono"])
        pdf.drawString(315, y, contacto["correo"])
        pdf.drawString(485, y, contacto["ciudad"])
        y = y - 18

    dibujar_numero_pagina(pdf, numero_pagina)
    pdf.save()

    return len(lista), fecha