from functools import reduce
from src.models.modelos import Tarea, Usuario


'''
Función pura: consume la colección de tareas y acumula el total por estado
utilizando 'functools.reduce' con un diccionario como acumulador inicial.
'''

def calcularEstadisticasEstado(tareas: tuple[Tarea, ...]) -> dict[str, int]:
    def acumulador(conteo: dict[str, int], t: Tarea) -> dict[str, int]:
        copia = dict(conteo)
        copia[t.estado] = copia.get(t.estado, 0) + 1
        return copia

    estadoInicial = {"HECHO": 0, "EN_PROCESO": 0, "NO_INICIADO": 0}
    return reduce(acumulador, tareas, estadoInicial)


'''
Función pura: filtra tareas completadas ('HECHO') y construye el ranking de cumplimiento.
'''
def obtenerRankingCumplimiento(usuarios: tuple[Usuario, ...], tareas: tuple[Tarea, ...]) -> list[tuple[str, int]]:
    tareasHechas: tuple[Tarea, ...] = tuple(filter(lambda t: t.estado == "HECHO", tareas))

    # Proyección con map calculando el conteo de tareas completadas por usuario
    ranking = list(
        map(
            lambda u: (
                u.nombre,
                len(tuple(filter(lambda t: t.asignadoA == u.id, tareasHechas)))
            ),
            usuarios
        )
    )

    # Ordenamiento descendente por tareas cumplidas
    return sorted(ranking, key=lambda item: item[1], reverse=True)