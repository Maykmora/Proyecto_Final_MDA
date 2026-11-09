# Agenda de Contactos con Acceso Aleatorio

Esta es una aplicación de escritorio hecha en Python que administra una agenda de contactos guardada en un archivo de registros de tamaño fijo. Gracias a ese formato, la aplicación puede llegar directamente a cualquier contacto sin leer el archivo completo. Además usa un índice en JSON para buscar por ID, exporta la información a JSON y a PDF, verifica que el archivo no haya sido alterado fuera de la aplicación y crea respaldos comprimidos en ZIP.

Fue desarrollada para el Laboratorio No. 2 del curso de Manejo de Archivos, en la Facultad de Ingeniería de la Universidad Rafael Landívar, Campus San Alberto Hurtado, S.J. de Quetzaltenango, carrera de Ingeniería en Informática y Sistemas.

## Comenzando 

Estas instrucciones te permitirán obtener una copia del proyecto funcionando en tu computadora, para usarlo y probarlo. La aplicación fue desarrollada y probada en Windows.

### Pre-requisitos 

Necesitas tener instalado Python 3.9 o superior y Git. Puedes comprobar la versión de Python con este comando:

```
python --version
```

También necesitas dos librerías externas: PyQt6, que se usa para la interfaz gráfica, y ReportLab, que se usa para generar el reporte PDF. Se instalan en el paso de instalación que aparece más abajo. Todo lo demás lo hace con módulos que ya vienen con Python.

### Instalación 

Primero descarga el proyecto y entra a su carpeta:

```
git clone URL-DEL-REPOSITORIO
cd ProyectoFinal
```

Si prefieres no instalar las librerías en todo tu sistema, crea y activa un entorno virtual. Este paso es opcional:

```
python -m venv .venv
.venv\Scripts\activate
```

Instala las dos librerías necesarias:

```
python -m pip install PyQt6 reportlab
```

Ejecuta la aplicación desde la carpeta principal del proyecto:

```
python src/main.py
```

Se abrirá la ventana de la agenda, con un menú lateral que tiene cuatro secciones: Contactos, Exportar, Herramientas y Ayuda.

Para probarla rápidamente, entra a Contactos, llena el formulario con un ID, un nombre, un teléfono, un correo y una ciudad, y presiona Agregar. El contacto aparecerá en la tabla junto con el número de registro y la posición en bytes donde quedó guardado. Luego escribe ese mismo ID, presiona Buscar por ID y verás cómo la aplicación indica el seek y el tell de esa lectura. Después entra a Exportar y genera el JSON y el reporte PDF, y por último entra a Herramientas y crea un respaldo ZIP. Los archivos que se generan se guardan solos en las carpetas data y reports.

## Cómo está organizado el proyecto

El código fuente está en la carpeta src. El archivo main.py arranca la aplicación e interfaz.py construye la ventana, el menú, los formularios, las tablas y los mensajes. El archivo contactos.py se encarga de los registros de tamaño fijo y del uso de seek y tell. El archivo indice.py maneja el índice en JSON, exportar.py genera el JSON y el PDF, integridad.py calcula el hash y crea los respaldos, metadatos.py consulta el tamaño, la fecha y los permisos de los archivos, y rutas.py define en qué carpeta se guarda cada cosa.

Los archivos que genera la aplicación quedan ordenados en dos carpetas. En la carpeta data quedan el archivo de contactos, el índice y el hash de integridad. En la carpeta reports quedan el JSON exportado, el reporte PDF y los respaldos ZIP. Ambas carpetas se crean solas si no existen. La carpeta docs queda para la documentación del laboratorio. Los archivos generados se incluyen en el repositorio porque el laboratorio los pide como entregables.

## Cómo funciona por dentro

### Cómo se guardan los contactos

Los contactos se guardan en el archivo contactos.dat y cada uno ocupa exactamente 100 bytes. El ID ocupa 5 bytes, el nombre 30, el teléfono 15, el correo 35 y la ciudad 14, y al final se agrega un salto de línea de 1 byte. Cada campo se rellena con espacios hasta completar su largo máximo.

Como todos los registros miden lo mismo, la posición de cualquiera se calcula multiplicando su número de registro por 100. El registro 0 empieza en el byte 0, el registro 1 en el byte 100, el registro 2 en el byte 200, y así sucesivamente.

Los largos se miden en bytes y no en caracteres, porque el archivo usa UTF-8 y letras como la eñe o las vocales con tilde ocupan 2 bytes. Si se contaran caracteres, un registro con acentos se pasaría de 100 bytes y todas las posiciones quedarían desalineadas. Por eso la aplicación avisa cuando un dato no cabe en su campo. También por eso el archivo se abre en modo binario, ya que en Windows el modo texto cambia los saltos de línea y rompería el cálculo de posiciones.

### Acceso aleatorio con seek y tell

Para leer o modificar un contacto, la aplicación usa seek para colocarse directamente en la posición del registro, sin recorrer lo que hay antes. Antes y después de cada operación usa tell para saber en qué byte está parada, y esas dos posiciones se muestran en la pantalla de Contactos.

Cuando se modifica un contacto, solo se sobrescriben los 100 bytes de su registro. El resto del archivo no se reescribe y su tamaño no cambia.

### El índice

El archivo indice.json relaciona cada ID con el número de registro donde está guardado su contacto. Por ejemplo, puede decir que el ID 40212 está en el registro 0 y que el ID 32 está en el registro 1.

Cuando se busca un contacto, la aplicación consulta primero el índice, calcula la posición con ese número de registro y hace seek directo a ese lugar. Así lee un solo registro del archivo de datos, sin importar si hay diez contactos o diez mil. En cambio, una búsqueda secuencial tendría que leer los registros uno por uno hasta encontrar el ID, y en el peor caso los leería todos.

Cada vez que se agrega un contacto, el índice se actualiza. Si el índice no existe, está dañado, tiene una cantidad de entradas distinta a la de registros o apunta a posiciones incorrectas, la aplicación lo reconstruye leyendo el archivo de contactos y le avisa al usuario.

### Integridad con SHA-256

Cada vez que la aplicación guarda un cambio, calcula el hash SHA-256 del archivo de contactos y lo guarda en contactos.sha256. Al abrir la aplicación, y también cuando se presiona el botón de verificar integridad, el hash se vuelve a calcular y se compara con el guardado. Si no coinciden, la aplicación avisa que el archivo fue modificado fuera de ella y muestra ambos hashes. La etiqueta de estado en la sección de Herramientas se pone verde cuando todo está bien y roja cuando se detecta una alteración.

### Respaldo comprimido

La opción de respaldo crea un archivo ZIP con el archivo de contactos y el índice, y lo guarda en la carpeta reports con la fecha y la hora en su nombre. Al terminar, muestra el tamaño original, el tamaño comprimido y el porcentaje de ahorro.

Con pocos contactos, el archivo ZIP en disco puede pesar más que los datos comprimidos, porque el formato ZIP agrega información de control por cada archivo. Con más contactos la compresión se aprovecha mucho mejor, sobre todo porque los espacios de relleno de los registros se comprimen muy bien.

### Escritura segura y manejo de errores

El índice, el hash y el JSON exportado se guardan primero en un archivo temporal y luego se renombran con os.replace. De esa forma, si algo falla a la mitad, el archivo anterior queda intacto. El archivo de contactos es la excepción, porque el laboratorio exige modificarlo en el lugar y no reescribirlo completo.

La aplicación no se cierra ante los errores más comunes. Avisa cuando un ID no existe o está repetido, cuando falta algún dato del formulario, cuando un dato es demasiado largo para su campo, cuando un archivo está dañado y cuando no hay permisos para leer o escribir. Si ocurre un error que no estaba previsto, muestra un mensaje en lugar de cerrarse.

## Ejecutando las pruebas 

Este proyecto no incluye pruebas automatizadas. Las pruebas se hicieron de forma manual, usando la propia aplicación y revisando los archivos que genera. Para repetirlas, ejecuta la aplicación y sigue este recorrido.

Agrega tres contactos y comprueba que en la tabla aparecen con las posiciones 0, 100 y 200, y que el archivo contactos.dat pesa exactamente 300 bytes. Busca uno por su ID y revisa que la aplicación muestre el seek y el tell de la lectura. Modifica un contacto y comprueba que el tamaño del archivo no cambia. Intenta agregar un ID repetido y buscar un ID que no existe, y verifica que salgan los avisos correspondientes.

Después exporta a JSON y genera el reporte PDF, y revisa que ambos aparezcan en la carpeta reports. Crea un respaldo ZIP y comprueba que muestre el tamaño original y el comprimido. Abre la ventana de información del archivo y revisa el tamaño, la fecha y los permisos.

### Qué verifican estas pruebas 

El recorrido anterior verifica los requisitos principales del laboratorio: que los registros miden siempre lo mismo, que el acceso se hace directamente por posición, que el índice se mantiene al día y que los archivos exportados y los respaldos se generan correctamente.

Para comprobar la verificación de integridad hay que alterar el archivo de contactos a mano. Con la aplicación cerrada, haz primero una copia de data/contactos.dat en otra carpeta y luego ejecuta este comando desde la carpeta principal del proyecto, que cambia un solo byte sin modificar el tamaño del archivo:

```
python -c "d=open('data/contactos.dat','r+b'); d.seek(10); d.write(b'X'); d.close()"
```

Al abrir la aplicación debe aparecer el aviso de archivo modificado, con el hash guardado y el hash actual, y la etiqueta de integridad en Herramientas debe verse en rojo. Para dejar todo como estaba, vuelve a copiar el archivo original a la carpeta data.

También se puede probar el manejo de errores borrando el archivo indice.json con la aplicación cerrada, para ver cómo se reconstruye solo, o marcando contactos.dat como solo lectura en sus propiedades de Windows, para ver el aviso de falta de permisos al intentar agregar un contacto.

### Pruebas de estilo de codificación 

El proyecto no usa herramientas automáticas de estilo. El código se escribió con criterios sencillos: funciones normales con def, sin clases propias, con listas, diccionarios, ciclos y condiciones básicas, y con nombres de funciones, variables y archivos en español. Los mensajes que ve el usuario también están en español.

## Construido con 

* [Python](https://www.python.org/) - Lenguaje de programación, junto con sus módulos estándar os, json, hashlib, zipfile y datetime
* [PyQt6](https://pypi.org/project/PyQt6/) - Librería usada para la interfaz gráfica
* [ReportLab](https://pypi.org/project/reportlab/) - Librería usada para generar el reporte en PDF

## Versionado 

El proyecto se construyó en etapas y cada una quedó registrada en un commit. Primero se armó la estructura y la interfaz gráfica. Después se agregaron los registros de tamaño fijo con seek y tell, luego el índice en JSON, la exportación a JSON y PDF, la integridad con SHA-256 junto con los respaldos ZIP, y los metadatos, los permisos y el manejo de errores. Al final se ordenaron los archivos generados en las carpetas data y reports. Puedes ver todo el historial con el comando git log.
