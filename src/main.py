import sys
from PyQt6.QtWidgets import QApplication

import interfaz


def main():
    sys.excepthook = interfaz.mostrar_error_inesperado
    app = QApplication(sys.argv)
    ventana = interfaz.crear_ventana()
    ventana.show()
    interfaz.revisar_al_iniciar()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()