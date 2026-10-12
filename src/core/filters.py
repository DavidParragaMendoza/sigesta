from src.models.modelos import Usuario
from src.models.modelos import Tarea


'''
Closure: captura 'correo' y 'password' en su entorno léxico.
'''
def crearFiltroCredenciales(correo: str, password: str):
    def criterio(user: Usuario) -> bool:
        return user.correo == correo and user.password == password

    return criterio


'''
Función pura: aplica el closure sobre 'filter' para buscar al usuario.
Retorna la instancia de Usuario si coincide, o None si no existe.
'''
def autenticarUsuario(usuarios: tuple[Usuario, ...], correo: str, password: str):
    filtroLogin = crearFiltroCredenciales(correo, password)
    usuariosCoincidentes: tuple[Usuario, ...] = tuple(filter(filtroLogin, usuarios)) 
    return usuariosCoincidentes[0] if len(usuariosCoincidentes) > 0 else None


'''
Closure: captura 'idUsuario' en su entorno léxico.
Devuelve un predicado para filtrar tareas.
'''
def crearFiltroPorAsignado(idUsuario: int):
    def criterio(t: Tarea) -> bool:
        return t.asignadoA == idUsuario

    return criterio


'''
Función pura: aplica el closure sobre 'filter' para listar tareas del usuario.
'''
def obtenerTareasPorUsuario(tareas: tuple[Tarea, ...], idUsuario: int) -> tuple[Tarea, ...]:
    filtroAsignado = crearFiltroPorAsignado(idUsuario)
    return tuple(filter(filtroAsignado, tareas))


'''
Función pura: filtra y retorna las tareas asignadas al personal (trabajadores).
Permite opcionalmente excluir un ID específico (por ejemplo, el ID del jefe).
'''
def obtenerTareasDelPersonal(tareas: tuple[Tarea, ...], usuarios: tuple[Usuario, ...], idExcluido: int = None) -> tuple[Tarea, ...]:
    idsTrabajadores = set(
        map(
            lambda u: u.id,
            filter(lambda u: u.rol == "TRABAJADOR" and (idExcluido is None or u.id != idExcluido), usuarios)
        )
    )
    return tuple(filter(lambda t: t.asignadoA in idsTrabajadores, tareas))