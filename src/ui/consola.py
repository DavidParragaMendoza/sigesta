from typing import Optional
from src.models.modelos import EstadoSistema, Usuario, Tarea
from src.core.filters import autenticarUsuario
from src.core.dispatcher import agregarUsuario
from src.storage.repository import guardarEstado
from src.core.filters import obtenerTareasPorUsuario
from src.core.dispatcher import agregarTarea, cambiarEstadoTarea
from src.core.transformations import calcularEstadisticasEstado, obtenerRankingCumplimiento


'''
Inicia la interfaz de línea de comandos (CLI) para la aplicación.
'''

def iniciarCli(estado: EstadoSistema) -> None:
    print("Bienvenido a la aplicacion CLI.")
    estadoActual = estado
    while True:
        opcion: int = menu()
        estadoActual = procesarOpcion(opcion, estadoActual)
        if opcion == 3:
            break


'''Muestra el menú principal y valida la opción.'''
def menu() -> int:
    while True:
        print("\nMenu principal:")
        print("1. Iniciar sesion")
        print("2. Crear cuenta")
        print("3. Salir")
        
        entrada: str = input("Seleccione una opcion: ")
        
        if entrada.isdigit():
            opcion: int = int(entrada)
            if 1 <= opcion <= 3:
                return opcion
        
        print("Opción inválida. Intente de nuevo.")


'''
Procesa la opción seleccionada y propaga el estado actualizado.
'''
def procesarOpcion(opcion: int, estado: EstadoSistema) -> EstadoSistema:
    match opcion:
        case 1:
            return iniciarSesion(estado)
        case 2:
            return crearCuenta(estado)
        case 3:
            print("Saliendo de la aplicación...")
            return estado
        case _:
            print("Opción inválida. Por favor, seleccione una opción válida.")
            return estado


'''
Pide credenciales y delega la verificación al núcleo funcional.
'''

def iniciarSesion(estado: EstadoSistema) -> EstadoSistema:
    correo: str = input("Ingrese su correo: ")
    password: str = input("Ingrese su contraseña: ")

    usuario: Optional[Usuario] = autenticarUsuario(estado.usuarios, correo, password)

    if usuario is not None:
        print(f"\nInicio de sesión exitoso. Bienvenido, {usuario.nombre} ({usuario.rol})")
        return menuSesion(usuario, estado)
    else:
        print("\nCorreo o contraseña incorrectos. Intente de nuevo.")
        return estado


'''
Pide datos, transforma el estado de forma inmutable y persiste en JSON.
'''
def crearCuenta(estado: EstadoSistema) -> EstadoSistema:
    print("\n--- Registro de nuevo usuario ---")
    nombre: str = input("Ingrese su nombre: ")
    correo: str = input("Ingrese su correo: ")
    password: str = input("Ingrese su contraseña: ")
    rol: str = input("Ingrese su rol (TRABAJADOR / JEFE): ").upper()

    # 1. Llamada al Núcleo Puro: obtiene un nuevo estado inmutable
    nuevoEstado: EstadoSistema = agregarUsuario(estado, nombre, correo, password, rol)

    # 2. Llamada a la Cáscara Impura: persiste el nuevo estado en el archivo JSON
    guardarEstado(nuevoEstado)

    print(f"Cuenta creada exitosamente para {nombre}. ¡Ahora puedes iniciar sesión!")
    return nuevoEstado


'''
Captura los campos comunes para reutilizar en cualquier creación de tarea.
'''
def pedirDatosTareaComunes() -> tuple[str, str, Optional[str]]:
    titulo: str = input("Título de la tarea: ")
    prioridad: str = input("Prioridad (ALTA / MEDIA / BAJA): ").upper()
    desc: str = input("Descripción (opcional, Enter para omitir): ")
    descripcion: Optional[str] = desc if desc.strip() != "" else None
    return titulo, prioridad, descripcion


'''
Imprime el listado de tareas en formato tabular de consola.
'''
def mostrarListaTareas(tareas: tuple[Tarea, ...]) -> None:
    if not tareas:
        print("\nNo hay tareas registradas en esta vista.")
        return

    print("\n--- Listado de Tareas ---")
    for t in tareas:
        print(f"[{t.id}] {t.titulo} | Estado: {t.estado} | Prioridad: {t.prioridad} | Asignado ID: {t.asignadoA}")


'''
Solicita el ID de la tarea y actualiza su estado de forma inmutable.
'''
def modificarEstadoConsola(estado: EstadoSistema, idUsuario: int) -> EstadoSistema:
    misTareas = obtenerTareasPorUsuario(estado.tareas, idUsuario)
    mostrarListaTareas(misTareas)
    
    idEntrada = input("\nIngrese el ID de la tarea a actualizar: ")
    if not idEntrada.isdigit():
        print("ID inválido.")
        return estado

    idTarea = int(idEntrada)
    print("Seleccione nuevo estado: 1. NO_INICIADO | 2. EN_PROCESO | 3. HECHO")
    op = input("Opción: ")
    nuevoEstado = "NO_INICIADO" if op == "1" else "EN_PROCESO" if op == "2" else "HECHO" if op == "3" else None

    if nuevoEstado:
        nuevoEstadoSistema = cambiarEstadoTarea(estado, idTarea, nuevoEstado)
        guardarEstado(nuevoEstadoSistema)
        print("Estado de la tarea actualizado con éxito.")
        return nuevoEstadoSistema
    
    print("Opción de estado inválida.")
    return estado


'''
Submenú dinámico para el usuario autenticado según su rol.
'''

def menuSesion(usuario: Usuario, estado: EstadoSistema) -> EstadoSistema:
    estadoActual = estado

    while True:
        print(f"\n--- Panel de {usuario.rol}: {usuario.nombre} ---")
        if usuario.rol == "JEFE":
            print("1. Agregar tarea (Personal o Asignada)")
            print("2. Ver mis tareas")
            print("3. Ver estadísticas y ranking")
            print("4. Cambiar estado de una tarea")
            print("5. Cerrar sesión")
        else:
            print("1. Ver mis tareas")
            print("2. Agregar tarea personal")
            print("3. Cambiar estado de una tarea")
            print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if usuario.rol == "JEFE":
            match opcion:   
                case "1":
                    titulo, prioridad, desc = pedirDatosTareaComunes()
                    print("¿Para quién es la tarea?: 1. Personal | 2. Asignar a un trabajador")
                    tipo = input("Opción: ")
                    destinatarioId = usuario.id if tipo == "1" else int(input("Ingrese el ID del trabajador: "))
                    estadoActual = agregarTarea(estadoActual, titulo, prioridad, destinatarioId, desc)
                    guardarEstado(estadoActual)
                    print("Tarea creada correctamente.")
                case "2":
                    misTareas = obtenerTareasPorUsuario(estadoActual.tareas, usuario.id)
                    mostrarListaTareas(misTareas)
                case "3":
                    stats = calcularEstadisticasEstado(estadoActual.tareas)
                    print(f"\n--- Resumen Global de Estados ---")
                    print(f"Hechas: {stats.get('HECHO', 0)} | En proceso: {stats.get('EN_PROCESO', 0)} | Sin comenzar: {stats.get('NO_INICIADO', 0)}")
                    print("\n--- Ranking de Cumplimiento ---")
                    for nombre, total in obtenerRankingCumplimiento(estadoActual.usuarios, estadoActual.tareas):
                        print(f"• {nombre}: {total} tareas completadas")
                case "4":
                    estadoActual = modificarEstadoConsola(estadoActual, usuario.id)
                case "5":
                    break
        else:
            match opcion:
                case "1":
                    misTareas = obtenerTareasPorUsuario(estadoActual.tareas, usuario.id)
                    mostrarListaTareas(misTareas)
                case "2":
                    titulo, prioridad, desc = pedirDatosTareaComunes()
                    estadoActual = agregarTarea(estadoActual, titulo, prioridad, usuario.id, desc)
                    guardarEstado(estadoActual)
                    print("Tarea personal agregada.")
                case "3":
                    estadoActual = modificarEstadoConsola(estadoActual, usuario.id)
                case "4":
                    break

    return estadoActual