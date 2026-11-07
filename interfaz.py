from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit,
    QTableWidget, QHeaderView, QAbstractItemView,
    QTableWidgetItem, QMessageBox,
)

import contactos

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
"""


def mensaje_exito(texto):
    QMessageBox.information(elementos["ventana"], "Operación exitosa", texto)


def mensaje_advertencia(texto):
    QMessageBox.warning(elementos["ventana"], "Advertencia", texto)


def mensaje_error(texto):
    QMessageBox.critical(elementos["ventana"], "Error", texto)


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
        mensaje_advertencia("Debe escribir el ID del contacto.")
        return None

    try:
        contacto["id"] = int(contacto["id"])
    except ValueError:
        mensaje_advertencia("El ID debe ser un número entero.")
        return None

    if contacto["id"] <= 0:
        mensaje_advertencia("El ID debe ser un número mayor que cero.")
        return None

    if (contacto["nombre"] == "" or contacto["telefono"] == ""
            or contacto["correo"] == "" or contacto["ciudad"] == ""):
        mensaje_advertencia("Debe llenar todos los campos del contacto.")
        return None

    problema = contactos.validar_largos(contacto)
    if problema != "":
        mensaje_advertencia(problema)
        return None

    return contacto


def leer_id_buscado():
    texto = elementos["campo_id"].text().strip()

    if texto == "":
        mensaje_advertencia("Escriba el ID que desea buscar.")
        return None

    try:
        numero = int(texto)
    except ValueError:
        mensaje_advertencia("El ID debe ser un número entero.")
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
        mensaje_error("No hay permisos para leer o escribir el archivo de contactos.")
    elif isinstance(error, ValueError):
        mensaje_error("El archivo de contactos está dañado o tiene datos incorrectos.\n\n"
                      + str(error))
    else:
        mensaje_error("No se pudo usar el archivo de contactos.\n\n" + str(error))


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
        return

    tabla.setRowCount(0)
    for numero, contacto, inicio in lista:
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        valores = [contacto["id"], contacto["nombre"], contacto["telefono"],
                   contacto["correo"], contacto["ciudad"], numero, inicio]
        for columna in range(len(valores)):
            tabla.setItem(fila, columna, QTableWidgetItem(str(valores[columna])))


def agregar_contacto():
    contacto = leer_formulario()
    if contacto is None:
        return

    try:
        resultado = contactos.agregar_contacto(contacto)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    if resultado is None:
        mensaje_advertencia("Ya existe un contacto con el ID " + str(contacto["id"]) + ".")
        return

    numero, inicio, fin = resultado
    mostrar_posiciones("Se escribió el", numero, inicio, fin)
    actualizar_tabla()
    limpiar_formulario()
    mensaje_exito("Contacto agregado en el registro N° " + str(numero) + ".")


def buscar_contacto():
    id_buscado = leer_id_buscado()
    if id_buscado is None:
        return

    try:
        resultado = contactos.buscar_por_id(id_buscado)
    except (OSError, ValueError) as error:
        mostrar_error_archivo(error)
        return

    if resultado is None:
        mensaje_advertencia("No existe un contacto con el ID " + str(id_buscado) + ".")
        return

    numero, contacto, inicio, fin = resultado
    llenar_formulario(contacto)
    mostrar_posiciones("Se leyó el", numero, inicio, fin)
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

    if resultado is None:
        mensaje_advertencia("No existe un contacto con el ID " + str(contacto["id"])
                            + ". Use el botón Agregar para crearlo.")
        return

    numero, inicio, fin = resultado
    mostrar_posiciones("Se sobrescribió el", numero, inicio, fin)
    actualizar_tabla()
    elementos["tabla_contactos"].selectRow(numero)
    mensaje_exito("Contacto modificado. Solo se sobrescribió el registro N° "
                  + str(numero) + ".")


def exportar_json():
    mensaje_advertencia("La exportación a JSON se implementa en el COMMIT 4.")


def generar_pdf():
    mensaje_advertencia("El reporte PDF se implementa en el COMMIT 4.")


def verificar_integridad():
    mensaje_advertencia("La verificación de integridad se implementa en el COMMIT 5.")


def crear_respaldo():
    mensaje_advertencia("El respaldo ZIP se implementa en el COMMIT 5.")


def informacion_archivo():
    mensaje_advertencia("La información del archivo se implementa en el COMMIT 6.")


def abrir_manual():
    mensaje_exito("MANUAL DE USUARIO (simulado)\n\n"
                  "1. Entre a la sección Contactos.\n"
                  "2. Llene el formulario y presione Agregar.\n"
                  "3. Para buscar, escriba el ID y presione Buscar por ID.\n"
                  "4. Para modificar, busque el contacto, cambie los datos "
                  "y presione Modificar.")


def acerca_de():
    mensaje_exito("Agenda de Contactos con Acceso Aleatorio\n\n"
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
    version = QLabel("Laboratorio 2 - v1.0")
    version.setObjectName("version")
    layout.addWidget(version)
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
    ventana.statusBar().showMessage("Listo")

    actualizar_tabla()

    cambiar_pagina(0)
    return ventana