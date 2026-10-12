from dataclasses import replace
from src.models.modelos import EstadoSistema, Usuario
from src.models.modelos import Tarea
from typing import Optional


'''
Función pura:
Aplica el patrón Copy-and-Update (dataclasses.replace).
Produce un nuevo EstadoSistema sin mutar la colección anterior.
'''

def agregarUsuario(estadoActual: EstadoSistema, nombre: str, correo: str, password: str, rol: str) -> EstadoSistema:
    # 1. Calcular el siguiente ID de manera funcional
    siguienteId: int = len(estadoActual.usuarios) + 1
    # 2. Construir la nueva entidad inmutable
    nuevoUsuario = Usuario(
        id=siguienteId,
        nombre=nombre,
        correo=correo,
        password=password,
        rol=rol
    )

    # 3. Crear una nueva tupla inmutable sin usar .append() (concatenación)
    nuevosUsuarios: tuple[Usuario, ...] = estadoActual.usuarios + (nuevoUsuario,)

    # 4. Retornar un nuevo EstadoSistema conservando las tareas intactas
    return replace(estadoActual, usuarios=nuevosUsuarios)




'''
Función pura: genera una nueva tarea de forma inmutable (Copy-and-Update).
'''
def agregarTarea(estadoActual: EstadoSistema, titulo: str, prioridad: str, asignadoA: int, descripcion: Optional[str] = None) -> EstadoSistema:
    
    siguienteId: int = len(estadoActual.tareas) + 1
    
    nuevaTarea = Tarea(id=siguienteId, titulo=titulo, prioridad=prioridad, estado="NO_INICIADO", asignadoA=asignadoA, descripcion=descripcion)

    nuevasTareas: tuple[Tarea, ...] = estadoActual.tareas + (nuevaTarea,)
    return replace(estadoActual, tareas=nuevasTareas)


'''
Función pura: transforma la colección con map y actualiza con replace
sin mutar la tarea original.
'''
def cambiarEstadoTarea(estadoActual: EstadoSistema, idTarea: int, nuevoEstado: str) -> EstadoSistema:
    nuevasTareas: tuple[Tarea, ...] = tuple(
        map(
            lambda t: replace(t, estado=nuevoEstado) if t.id == idTarea else t,
            estadoActual.tareas
        )
    )
    return replace(estadoActual, tareas=nuevasTareas)