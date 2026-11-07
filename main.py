import sys
from PyQt6.QtWidgets import QApplication

import interfaz

def main():
    app = QApplication(sys.argv)
    ventana = interfaz.crear_ventana()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()