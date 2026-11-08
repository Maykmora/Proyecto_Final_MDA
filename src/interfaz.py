import os
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit,
    QTableWidget, QHeaderView, QAbstractItemView,
    QTableWidgetItem, QMessageBox, QDialog,
)

import contactos
import exportar
import indice
import integridad
import metadatos

elementos = {}

ESTILO = """
QMainWindow, QWidget#contenido {
    background-color: #f1f5f9;
}
QWidget {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 14px;
    color: #0f172a;
}

QFrame#barra_lateral {
    background-color: #1e293b;
}
QLabel#titulo_app {
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
}
QLabel#subtitulo_app {
    color: #94a3b8;
    font-size: 12px;
}
QLabel#version {
    color: #64748b;
    font-size: 11px;
}
QPushButton#boton_menu {
    background-color: transparent;
    color: #cbd5e1;
    text-align: left;
    padding: 12px 18px;
    border: none;
    border-radius: 8px;
    font-size: 15px;
}
QPushButton#boton_menu:hover {
    background-color: #334155;
}
QPushButton#boton_menu:checked {
    background-color: #4f46e5;
    color: #ffffff;
    font-weight: bold;
}

QLabel#titulo_pagina {
    font-size: 26px;
    font-weight: bold;
}
QLabel#descripcion_pagina {
    color: #64748b;
}
QFrame#tarjeta {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}
QLabel#titulo_tarjeta {
    font-size: 16px;
    font-weight: bold;
}
QLabel#texto_tarjeta {
    color: #64748b;
}
QLabel#etiqueta_estado {
    background-color: #eef2ff;
    color: #3730a3;
    border-radius: 8px;
    padding: 8px 12px;
}

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 10px;
}
QLineEdit:focus {
    border: 2px solid #4f46e5;
}

QPushButton#primario {
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
}
QPushButton#primario:hover {
    background-color: #4338ca;
}
QPushButton#secundario {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 18px;
}
QPushButton#secundario:hover {
    background-color: #f1f5f9;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #e2e8f0;
    selection-background-color: #c7d2fe;
    selection-color: #0f172a;
}
QHeaderView::section {
    background-color: #e2e8f0;
    color: #334155;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QStatusBar {
    background-color: #ffffff;
    color: #64748b;
}

QDialog {
    background-color: #f1f5f9;
}

QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #475569;
    font-size: 14px;
    background-color: transparent;
}
QMessageBox QLabel#qt_msgbox_label {
    font-size: 18px;
    font-weight: bold;
    min-width: 380px;
}
QMessageBox[tipo="exito"] QLabel#qt_msgbox_label {
    color: #15803d;
}
QMessageBox[tipo="info"] QLabel#qt_msgbox_label {
    color: #3730a3;
}
QMessageBox[tipo="advertencia"] QLabel#qt_msgbox_label {
    color: #b45309;
}
QMessageBox[tipo="error"] QLabel#qt_msgbox_label {
    color: #b91c1c;
}
QMessageBox QPushButton {
    background-color: #4f46e5;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 28px;
    min-width: 70px;
    font-weight: bold;
}
QMessageBox QPushButton:hover {
    background-color: #4338ca;
}
"""


def mostrar_mensaje(tipo, icono, titulo_ventana, texto, detalle):
    caja = QMessageBox(elementos["ventana"])
    caja.setProperty("tipo", tipo)
    caja.setIcon(icono)
    caja.setWindowTitle(titulo_ventana)
    caja.setText(texto)
    if detalle != "":
        caja.setInformativeText(detalle)
    caja.setStandardButtons(QMessageBox.StandardButton.Ok)
    caja.exec()


def mensaje_exito(texto, detalle=""):
    mostrar_mensaje("exito", QMessageBox.Icon.Information, "Éxito", texto, detalle)


def mensaje_info(texto, detalle=""):
    mostrar_mensaje("info", QMessageBox.Icon.Information, "Información", texto, detalle)


def mensaje_advertencia(texto, detalle=""):
    mostrar_mensaje("advertencia", QMessageBox.Icon.Warning, "Atención", texto, detalle)


def mensaje_error(texto, detalle=""):
    mostrar_mensaje("error", QMessageBox.Icon.Critical, "Error", texto, detalle)


def mostrar_error_inesperado(tipo_error, valor, traza):
    traceback.print_exception(tipo_error, valor, traza)
    mensaje_error("Error inesperado",
                  "Ocurrió un problema que la aplicación no esperaba, "
                  "pero se mantiene abierta.\n\n"
                  "Detalle: " + str(valor))


def crear_boton(texto, funcion, tipo):
    boton = QPushButton(texto)
    boton.setObjectName(tipo)
    boton.setCursor(Qt.CursorShape.PointingHandCursor)
    boton.clicked.connect(funcion)
    return boton


def crear_titulo(titulo, descripcion):
    layout = QVBoxLayout()
    layout.setSpacing(2)

    etiqueta_titulo = QLabel(titulo)
    etiqueta_titulo.setObjectName("titulo_pagina")

    etiqueta_desc = QLabel(descripcion)
    etiqueta_desc.setObjectName("descripcion_pagina")

    layout.addWidget(etiqueta_titulo)
    layout.addWidget(etiqueta_desc)
    return layout


def crear_tarjeta(titulo, descripcion, texto_boton, funcion):
    tarjeta = QFrame()
    tarjeta.setObjectName("tarjeta")

    layout = QVBoxLayout(tarjeta)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(8)

    etiqueta_titulo = QLabel(titulo)
    etiqueta_titulo.setObjectName("titulo_tarjeta")

    etiqueta_texto = QLabel(descripcion)
    etiqueta_texto.setObjectName("texto_tarjeta")
    etiqueta_texto.setWordWrap(True)

    boton = crear_boton(texto_boton, funcion, "primario")

    layout.addWidget(etiqueta_titulo)
    layout.addWidget(etiqueta_texto)
    layout.addStretch()
    layout.addWidget(boton)
    return tarjeta


def crear_pagina_contactos():
    pagina = QWidget()
    pagina.setObjectName("contenido")
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(30, 25, 30, 20)
    layout.setSpacing(15)

    layout.addLayout(crear_titulo(
        "Contactos",
        "Agrega, busca por ID y modifica los contactos de la agenda."))

    tarjeta = QFrame()
    tarjeta.setObjectName("tarjeta")
    layout_tarjeta = QVBoxLayout(tarjeta)
    layout_tarjeta.setContentsMargins(20, 18, 20, 18)
    layout_tarjeta.setSpacing(12)

    formulario = QFormLayout()
    formulario.setSpacing(10)

    elementos["campo_id"] = QLineEdit()
    elementos["campo_id"].setPlaceholderText("Número entero único, por ejemplo 1")
    elementos["campo_nombre"] = QLineEdit()
    elementos["campo_telefono"] = QLineEdit()
    elementos["campo_correo"] = QLineEdit()
    elementos["campo_ciudad"] = QLineEdit()

    for nombre_campo in ["campo_id", "campo_nombre", "campo_telefono",
                         "campo_correo", "campo_ciudad"]:
        elementos[nombre_campo].setMinimumHeight(36)

    formulario.addRow("ID:", elementos["campo_id"])
    formulario.addRow("Nombre:", elementos["campo_nombre"])
    formulario.addRow("Teléfono:", elementos["campo_telefono"])
    formulario.addRow("Correo:", elementos["campo_correo"])
    formulario.addRow("Ciudad:", elementos["campo_ciudad"])
    layout_tarjeta.addLayout(formulario)

    fila_botones = QHBoxLayout()
    fila_botones.setSpacing(10)
    fila_botones.addWidget(crear_boton("Agregar", agregar_contacto, "primario"))
    fila_botones.addWidget(crear_boton("Buscar por ID", buscar_contacto, "primario"))
    fila_botones.addWidget(crear_boton("Modificar", modificar_contacto, "primario"))
    fila_botones.addWidget(crear_boton("Limpiar", limpiar_formulario, "secundario"))
    fila_botones.addStretch()
    layout_tarjeta.addLayout(fila_botones)

    elementos["etiqueta_posicion"] = QLabel(
        "Posición en el archivo (tell): todavía no se ha realizado ninguna operación")
    elementos["etiqueta_posicion"].setObjectName("etiqueta_estado")
    elementos["etiqueta_posicion"].setWordWrap(True)
    layout_tarjeta.addWidget(elementos["etiqueta_posicion"])

    layout.addWidget(tarjeta)

    columnas = ["ID", "Nombre", "Teléfono", "Correo", "Ciudad",
                "N° registro", "Posición (byte)"]
    tabla = QTableWidget(0, len(columnas))
    tabla.setHorizontalHeaderLabels(columnas)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.verticalHeader().setVisible(False)
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    tabla.setAlternatingRowColors(True)
    elementos["tabla_contactos"] = tabla

    layout.addWidget(tabla)
    return pagina


def crear_pagina_exportar():
    pagina = QWidget()
    pagina.setObjectName("contenido")
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(30, 25, 30, 20)
    layout.setSpacing(15)

    layout.addLayout(crear_titulo(
        "Exportar",
        "Genera archivos con la información de la agenda."))

    fila = QHBoxLayout()
    fila.setSpacing(20)
    fila.addWidget(crear_tarjeta(
        "Exportar a JSON",
        "Guarda todos los contactos de la agenda en un archivo JSON.",
        "Exportar a JSON", exportar_json))
    fila.addWidget(crear_tarjeta(
        "Reporte PDF",
        "Crea un reporte en PDF con la lista de contactos y la fecha de generación.",
        "Generar reporte PDF", generar_pdf))
    layout.addLayout(fila)

    layout.addStretch()
    return pagina


def crear_pagina_herramientas():
    pagina = QWidget()
    pagina.setObjectName("contenido")
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(30, 25, 30, 20)
    layout.setSpacing(15)

    layout.addLayout(crear_titulo(
        "Herramientas",
        "Integridad, respaldos e información del archivo de contactos."))

    elementos["etiqueta_integridad"] = QLabel("Estado de integridad: sin verificar")
    elementos["etiqueta_integridad"].setObjectName("etiqueta_estado")
    layout.addWidget(elementos["etiqueta_integridad"])

    fila = QHBoxLayout()
    fila.setSpacing(20)
    fila.addWidget(crear_tarjeta(
        "Verificar integridad",
        "Compara el hash SHA-256 del archivo con el guardado para detectar cambios externos.",
        "Verificar integridad", verificar_integridad))
    fila.addWidget(crear_tarjeta(
        "Respaldo ZIP",
        "Comprime el archivo de contactos y el índice, y muestra el tamaño original y comprimido.",
        "Crear respaldo ZIP", crear_respaldo))
    fila.addWidget(crear_tarjeta(
        "Información del archivo",
        "Muestra el tamaño, la fecha de última modificación y los permisos.",
        "Ver información", informacion_archivo))
    layout.addLayout(fila)

    layout.addStretch()
    return pagina


def crear_pagina_ayuda():
    pagina = QWidget()
    pagina.setObjectName("contenido")
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(30, 25, 30, 20)
    layout.setSpacing(15)

    layout.addLayout(crear_titulo(
        "Ayuda",
        "Información general sobre la aplicación."))

    fila = QHBoxLayout()
    fila.setSpacing(20)
    fila.addWidget(crear_tarjeta(
        "Manual de usuario",
        "Explica cómo agregar, buscar y modificar contactos.",
        "Abrir manual", abrir_manual))
    fila.addWidget(crear_tarjeta(
        "Acerca de",
        "Datos del proyecto: Laboratorio de Agenda de Contactos con Acceso Aleatorio.",
        "Acerca de", acerca_de))
    layout.addLayout(fila)

    layout.addStretch()
    return pagina


def leer_formulario():
    contacto = {
        "id": elementos["campo_id"].text().strip(),
        "nombre": elementos["campo_nombre"].text().strip(),
        "telefono": elementos["campo_telefono"].text().strip(),
        "correo": elementos["campo_correo"].text().strip(),
        "ciudad": elementos["campo_ciudad"].text().strip(),
    }

    if contacto["id"] == "":
        mensaje_advertencia("Falta el ID",
                            "Escriba el ID del contacto antes de continuar.")
        return None

    try:
        contacto["id"] = int(contacto["id"])
    except ValueError:
        mensaje_advertencia("ID no válido",
                            "El ID debe ser un número entero, por ejemplo 1.")
        return None

    if contacto["id"] <= 0:
        mensaje_advertencia("ID no válido",
                            "El ID debe ser un número mayor que cero.")
        return None

    if (contacto["nombre"] == "" or contacto["telefono"] == ""
            or contacto["correo"] == "" or contacto["ciudad"] == ""):
        mensaje_advertencia("Faltan datos",
                            "Llene todos los campos: nombre, teléfono, correo y ciudad.")
        return None

    problema = contactos.validar_largos(contacto)
    if problema != "":
        mensaje_advertencia("Dato demasiado largo", problema)
        return None

    return contacto


def leer_id_buscado():
    texto = elementos["campo_id"].text().strip()

    if texto == "":
        mensaje_advertencia("Falta el ID",
                            "Escriba el ID del contacto que desea buscar.")
        return None

    try:
        numero = int(texto)
    except ValueError:
        mensaje_advertencia("ID no válido",
                            "El ID debe ser un número entero, por ejemplo 1.")
        return None

    return numero


def limpiar_formulario():
    elementos["campo_id"].clear()
    elementos["campo_nombre"].clear()
    elementos["campo_telefono"].clear()
    elementos["campo_correo"].clear()
    elementos["campo_ciudad"].clear()
    elementos["campo_id"].setFocus()
    elementos["ventana"].statusBar().showMessage("Formulario limpio", 3000)


def mostrar_error_archivo(error):
    if isinstance(error, PermissionError):
        mensaje_error("Sin permisos",
                      "No se puede leer ni escribir en los archivos de la agenda.\n"
                      "Revise los permisos de la carpeta del proyecto y que el "
                      "archivo no esté abierto en otro programa.")
    elif isinstance(error, ValueError):
        mensaje_error("Archivo dañado",
                      "Un archivo de la agenda tiene datos incorrectos y no se pudo leer.\n\n"
                      "Detalle: " + str(error))
    else:
        mensaje_error("No se pudo usar el archivo",
                      "Ocurrió un problema al acceder a los archivos de la agenda.\n\n"
                      "Detalle: " + str(error))


def mostrar_avisos():
    for aviso in contactos.avisos:
        mensaje_advertencia("Índice reconstruido", aviso)
    contactos.avisos.clear()


def mostrar_posiciones(operacion, numero, inicio, fin):
    texto = (operacion + " registro N° " + str(numero)
             + "   |   seek(" + str(inicio) + ") -> tell() = " + str(inicio)
             + "   |   después de la operación: tell() = " + str(fin))
    elementos["etiqueta_posicion"].setText(texto)


def llenar_formulario(contacto):
    elementos["campo_id"].setText(str(contacto["id"]))
    elementos["campo_nombre"].setText(contacto["nombre"])
    elementos["campo_telefono"].setText(contacto["telefono"])
    elementos["campo_correo"].setText(contacto["correo"])
    elementos["campo_ciudad"].setText(contacto["ciudad"])


def actualizar_tabla():
    tabla = elementos["tabla_contactos"]
    try:
        lista = contactos.listar_contactos()
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return False

    tabla.setRowCount(0)
    for numero, contacto, inicio in lista:
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        valores = [contacto["id"], contacto["nombre"], contacto["telefono"],
                   contacto["correo"], contacto["ciudad"], numero, inicio]
        for columna in range(len(valores)):
            tabla.setItem(fila, columna, QTableWidgetItem(str(valores[columna])))

    return True

def agregar_contacto():
    contacto = leer_formulario()
    if contacto is None:
        return

    try:
        resultado = contactos.agregar_contacto(contacto)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    mostrar_avisos()

    if resultado is None:
        mensaje_advertencia("ID repetido",
                            "Ya existe un contacto con el ID " + str(contacto["id"]) + ".\n"
                            "Use otro ID o el botón Modificar.")
        return

    numero, inicio, fin = resultado
    mostrar_posiciones("Se escribió el", numero, inicio, fin)
    actualizar_tabla()
    limpiar_formulario()
    mensaje_exito("Contacto agregado",
                  "Se guardó en el registro N° " + str(numero)
                  + ", que empieza en el byte " + str(inicio) + " del archivo.\n"
                  "El índice también se actualizó.")


def buscar_contacto():
    id_buscado = leer_id_buscado()
    if id_buscado is None:
        return

    try:
        resultado = contactos.buscar_por_id(id_buscado)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    mostrar_avisos()

    if resultado is None:
        mensaje_advertencia("Contacto no encontrado",
                            "No existe ningún contacto con el ID " + str(id_buscado) + ".")
        return

    numero, contacto, inicio, fin = resultado
    llenar_formulario(contacto)
    mostrar_posiciones("Según el índice, el ID " + str(id_buscado) + " está en el",
                       numero, inicio, fin)
    elementos["tabla_contactos"].selectRow(numero)
    elementos["ventana"].statusBar().showMessage("Contacto encontrado", 3000)


def modificar_contacto():
    contacto = leer_formulario()
    if contacto is None:
        return

    try:
        resultado = contactos.modificar_contacto(contacto)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    mostrar_avisos()

    if resultado is None:
        mensaje_advertencia("Contacto no encontrado",
                            "No existe ningún contacto con el ID " + str(contacto["id"]) + ".\n"
                            "Use el botón Agregar para crearlo.")
        return

    numero, inicio, fin = resultado
    mostrar_posiciones("Se sobrescribió el", numero, inicio, fin)
    actualizar_tabla()
    elementos["tabla_contactos"].selectRow(numero)
    mensaje_exito("Contacto modificado",
                  "Solo se sobrescribió el registro N° " + str(numero)
                  + ". El resto del archivo no cambió.")


def partir_hash(texto):
    return texto[:32] + "\n" + texto[32:]


def mostrar_estado_integridad(texto, tipo):
    etiqueta = elementos["etiqueta_integridad"]
    etiqueta.setText("Estado de integridad: " + texto)
    if tipo == "bueno":
        etiqueta.setStyleSheet("background-color: #dcfce7; color: #15803d; "
                               "border-radius: 8px; padding: 8px 12px; font-weight: bold;")
    elif tipo == "malo":
        etiqueta.setStyleSheet("background-color: #fee2e2; color: #b91c1c; "
                               "border-radius: 8px; padding: 8px 12px; font-weight: bold;")
    else:
        etiqueta.setStyleSheet("")


def revisar_integridad(es_manual):
    try:
        estado, hash_guardado, hash_actual = integridad.verificar_integridad(
            contactos.ARCHIVO_CONTACTOS)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return False

    if estado == "correcto":
        mostrar_estado_integridad("correcto, sin cambios externos", "bueno")
        if es_manual:
            mensaje_exito("Integridad correcta",
                          "El archivo de contactos no fue modificado fuera de la aplicación.\n\n"
                          "Hash SHA-256:\n" + partir_hash(hash_actual))

    elif estado == "modificado":
        mostrar_estado_integridad("ARCHIVO MODIFICADO fuera de la aplicación", "malo")
        mensaje_advertencia("Archivo modificado",
                            "El archivo de contactos fue modificado fuera de la aplicación.\n\n"
                            "Hash guardado:\n" + partir_hash(hash_guardado) + "\n\n"
                            "Hash actual:\n" + partir_hash(hash_actual))

    elif estado == "hash_creado":
        mostrar_estado_integridad("hash generado con el estado actual", "bueno")
        mensaje_info("Hash generado",
                     "No se encontró un hash válido del archivo de contactos.\n"
                     "Se generó uno nuevo con el contenido actual.")

    elif estado == "archivo_faltante":
        mostrar_estado_integridad("el archivo de contactos no existe", "malo")
        mensaje_advertencia("Archivo no encontrado",
                            "Existe un hash guardado, pero el archivo de contactos no está.\n"
                            "Fue eliminado o movido fuera de la aplicación.")

    else:
        mostrar_estado_integridad("sin datos para verificar", "normal")
        if es_manual:
            mensaje_info("Sin datos",
                         "Todavía no hay contactos guardados, no hay nada que verificar.")

    return True


def revisar_al_iniciar():
    if not revisar_integridad(False):
        return
    if not actualizar_tabla():
        return
    try:
        contactos.obtener_indice()
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return
    mostrar_avisos()


def exportar_json():
    try:
        cantidad = exportar.exportar_json()
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    if cantidad == 0:
        mensaje_advertencia("No hay contactos",
                            "Agregue al menos un contacto antes de exportar.")
        return

    mensaje_exito("Exportación completada",
                  "Contactos exportados: " + str(cantidad) + "\n\n"
                  "Archivo:\n" + exportar.ARCHIVO_JSON)


def generar_pdf():
    try:
        cantidad = exportar.exportar_json()
        if cantidad > 0:
            total, fecha = exportar.generar_pdf()
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    if cantidad == 0:
        mensaje_advertencia("No hay contactos",
                            "Agregue al menos un contacto antes de generar el reporte.")
        return

    mensaje_exito("Reporte PDF generado",
                  "Contactos incluidos: " + str(total) + "\n"
                  "Fecha de generación: " + fecha + "\n\n"
                  "Archivo:\n" + exportar.ARCHIVO_PDF)


def verificar_integridad():
    revisar_integridad(True)


def crear_respaldo():
    try:
        resultado = integridad.crear_respaldo(
            [contactos.ARCHIVO_CONTACTOS, indice.ARCHIVO_INDICE])
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    if resultado is None:
        mensaje_advertencia("Nada que respaldar",
                            "Todavía no hay archivos de contactos para respaldar.")
        return

    ruta_zip, detalle, original, comprimido, tamano_zip = resultado

    lineas = ""
    for nombre, tamano_original, tamano_comprimido in detalle:
        lineas = (lineas + nombre + ": " + str(tamano_original)
                  + " bytes -> " + str(tamano_comprimido) + " bytes\n")

    ahorro = 0
    if original > 0:
        ahorro = round((1 - comprimido / original) * 100, 1)

    mensaje_exito("Respaldo creado",
                  lineas + "\n"
                  "Tamaño original: " + str(original) + " bytes\n"
                  "Tamaño comprimido: " + str(comprimido) + " bytes (ahorro de "
                  + str(ahorro) + " %)\n"
                  "Tamaño del archivo ZIP: " + str(tamano_zip) + " bytes\n\n"
                  "Archivo:\n" + ruta_zip)


def informacion_archivo():
    rutas = [contactos.ARCHIVO_CONTACTOS, indice.ARCHIVO_INDICE, integridad.ARCHIVO_HASH]

    try:
        lista = metadatos.obtener_informacion_archivos(rutas)
    except OSError as error:
        mostrar_error_archivo(error)
        return

    try:
        total = contactos.contar_registros()
        if os.path.exists(contactos.ARCHIVO_CONTACTOS):
            resumen = ("Registros guardados: " + str(total) + "   |   Tamaño de cada registro: "
                       + str(contactos.TAMANO_REGISTRO) + " bytes")
        else:
            resumen = "El archivo de contactos todavía no existe."
    except ValueError:
        resumen = "No se pudo contar los registros: el archivo de contactos está dañado."

    dialogo = QDialog(elementos["ventana"])
    dialogo.setWindowTitle("Información del archivo")
    dialogo.setMinimumWidth(860)

    layout = QVBoxLayout(dialogo)
    layout.setContentsMargins(25, 22, 25, 22)
    layout.setSpacing(12)

    layout.addLayout(crear_titulo(
        "Información del archivo",
        "Carpeta: " + contactos.CARPETA))

    etiqueta_resumen = QLabel(resumen)
    etiqueta_resumen.setObjectName("etiqueta_estado")
    etiqueta_resumen.setWordWrap(True)
    layout.addWidget(etiqueta_resumen)

    columnas = ["Archivo", "Tamaño", "Última modificación", "Lectura", "Escritura"]
    tabla = QTableWidget(len(lista), len(columnas))
    tabla.setHorizontalHeaderLabels(columnas)
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    tabla.verticalHeader().setVisible(False)
    tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    tabla.setAlternatingRowColors(True)
    tabla.setMinimumHeight(170)

    for fila in range(len(lista)):
        datos = lista[fila]
        if datos["existe"]:
            valores = [datos["nombre"], str(datos["tamano"]) + " bytes", datos["modificado"],
                       "Sí" if datos["lectura"] else "No",
                       "Sí" if datos["escritura"] else "No"]
        else:
            valores = [datos["nombre"] + " (no existe)", "-", "-", "-", "-"]
        for columna in range(len(valores)):
            tabla.setItem(fila, columna, QTableWidgetItem(valores[columna]))

    layout.addWidget(tabla)

    fila_boton = QHBoxLayout()
    fila_boton.addStretch()
    fila_boton.addWidget(crear_boton("Cerrar", dialogo.accept, "primario"))
    layout.addLayout(fila_boton)

    dialogo.exec()


def abrir_manual():
    mensaje_info("Manual de usuario",
                 "FUNCIÓN SIMULADA")


def acerca_de():
    mensaje_info("Agenda de Contactos con Acceso Aleatorio",
                 "Laboratorio No. 2 - Manejo de archivos\n"
                 "Universidad Rafael Landívar - Campus de Quetzaltenango")


def cambiar_pagina(numero):
    elementos["paginas"].setCurrentIndex(numero)

    for i in range(len(elementos["botones_menu"])):
        elementos["botones_menu"][i].setChecked(i == numero)


def ir_contactos():
    cambiar_pagina(0)


def ir_exportar():
    cambiar_pagina(1)


def ir_herramientas():
    cambiar_pagina(2)


def ir_ayuda():
    cambiar_pagina(3)


def crear_barra_lateral():
    barra = QFrame()
    barra.setObjectName("barra_lateral")
    barra.setFixedWidth(230)

    layout = QVBoxLayout(barra)
    layout.setContentsMargins(15, 25, 15, 15)
    layout.setSpacing(6)

    titulo = QLabel("Agenda")
    titulo.setObjectName("titulo_app")
    subtitulo = QLabel("Acceso aleatorio de contactos")
    subtitulo.setObjectName("subtitulo_app")
    layout.addWidget(titulo)
    layout.addWidget(subtitulo)
    layout.addSpacing(25)

    textos = ["Contactos", "Exportar", "Herramientas", "Ayuda"]
    funciones = [ir_contactos, ir_exportar, ir_herramientas, ir_ayuda]
    botones = []

    for i in range(len(textos)):
        boton = QPushButton(textos[i])
        boton.setObjectName("boton_menu")
        boton.setCheckable(True)
        boton.setCursor(Qt.CursorShape.PointingHandCursor)
        boton.clicked.connect(funciones[i])
        layout.addWidget(boton)
        botones.append(boton)

    elementos["botones_menu"] = botones

    layout.addStretch()
    return barra


def crear_ventana():
    ventana = QMainWindow()
    ventana.setWindowTitle("Agenda de Contactos")
    ventana.resize(1150, 700)
    ventana.setMinimumSize(900, 600)
    ventana.setStyleSheet(ESTILO)
    elementos["ventana"] = ventana

    central = QWidget()
    layout = QHBoxLayout(central)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    layout.addWidget(crear_barra_lateral())

    paginas = QStackedWidget()
    paginas.addWidget(crear_pagina_contactos())
    paginas.addWidget(crear_pagina_exportar())
    paginas.addWidget(crear_pagina_herramientas())
    paginas.addWidget(crear_pagina_ayuda())
    elementos["paginas"] = paginas
    layout.addWidget(paginas)

    ventana.setCentralWidget(central)

    cambiar_pagina(0)
    return ventana