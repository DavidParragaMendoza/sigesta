from src.storage.repository import cargarEstado
from src.ui.consola import iniciarCli


if __name__ == "__main__":
    estado = cargarEstado()
    iniciarCli(estado)