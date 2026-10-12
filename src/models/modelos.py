from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Usuario:
    id: int
    nombre: str
    correo: str
    password: str
    rol: str

@dataclass(frozen=True)
class Tarea:
    id: int
    titulo: str
    prioridad: str
    estado: str
    asignadoA: int
    descripcion: Optional[str] = None  # <-- Siempre al final

@dataclass(frozen=True)
class EstadoSistema:
    tareas: tuple[Tarea, ...] = ()
    usuarios: tuple[Usuario, ...] = ()