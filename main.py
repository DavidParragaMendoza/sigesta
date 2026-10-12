import sys
from src.storage.repository import cargarEstado
from src.ui.consola import iniciarCli
from src.ui.gui import iniciarGui


if __name__ == "__main__":
    if "--cli" in sys.argv:
        estado = cargarEstado()
        iniciarCli(estado)
    else:
        iniciarGui()