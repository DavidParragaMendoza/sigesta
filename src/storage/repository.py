import json
from dataclasses import asdict
from os import path
from src.models.modelos import EstadoSistema, Usuario, Tarea


"""
Función impura (I/O): Lee el archivo JSON del disco y reconstruye
el estado del sistema como estructuras inmutables en memoria.
"""

def cargarEstado(ruta: str = "data/estado_sistema.json") -> EstadoSistema:
    if not path.exists(ruta):
        return EstadoSistema()

    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    usuariosInmutables: tuple[Usuario, ...] = tuple(
        map(lambda u: Usuario(**u), datos.get("usuarios", []))
    )

    tareasInmutables: tuple[Tarea, ...] = tuple(
        map(lambda t: Tarea(**t), datos.get("tareas", []))
    )

    return EstadoSistema(
        tareas=tareasInmutables,
        usuarios=usuariosInmutables
    )


    """
    Función impura (I/O): Serializa las estructuras inmutables a diccionarios
    y sobrescribe el archivo JSON en el disco con formato legible (indent=2).
    """
def guardarEstado(estado: EstadoSistema, ruta: str = "data/estado_sistema.json") -> None:
    datosParaGuardar = asdict(estado)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datosParaGuardar, f, indent=2, ensure_ascii=False)