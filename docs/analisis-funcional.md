<div align="center">

# 🧠 Análisis funcional de SIGESTA

### Del problema operativo a un núcleo de dominio puro e inmutable

<p>
  <img src="https://img.shields.io/badge/Unidad_1-HOFs_%7C_Pattern_Matching-3776AB?style=for-the-badge" alt="Unidad 1">
  <img src="https://img.shields.io/badge/Unidad_2-Closures_%7C_Inmutabilidad-6C5CE7?style=for-the-badge" alt="Unidad 2">
  <img src="https://img.shields.io/badge/Arquitectura-Functional_Core-2E7D32?style=for-the-badge" alt="Functional Core">
</p>

**SIGESTA · Sistema de Gestión y Seguimiento de Tareas**  
**Autor:** Ronald David Párraga Mendoza · **Asignatura:** Programación Funcional

</div>

> Este documento explica dónde se aplican los conceptos funcionales, qué
> efectos secundarios existen y por qué cada decisión técnica responde al
> problema real del gestor de tareas.

**Arquitectura:** *Functional Core, Imperative Shell* (Núcleo Funcional, Cáscara Imperativa)

---

## 1. Problema que resuelve la aplicación

En entornos corporativos y pequeñas oficinas operativas, la asignación y supervisión de actividades diarias suele fragmentarse a través de canales dispersos e informales (instrucciones verbales, notas adhesivas, mensajería instantánea). Esta dispersión produce tres problemas críticos:
1. **Pérdida de trazabilidad y duplicidad de esfuerzos:** Dificultad para auditar quién es el responsable directo de una tarea y en qué fase del ciclo de vida se encuentra (`NO_INICIADO`, `EN_PROCESO`, `HECHO`).
2. **Conflicto entre tareas asignadas y autogestión:** Los colaboradores no solo deben dar cumplimiento a las órdenes impartidas por su supervisor directo, sino también gestionar subtareas personales u operativas de su día a día. Al no existir un sistema consolidado, se pierde la perspectiva integral de la jornada laboral.
3. **Falta de visibilidad de carga real y analítica:** El líder carece de una herramienta centralizada para consultar en tiempo real métricas acumuladas de productividad y rankings de cumplimiento por colaborador sin depender de reportes manuales propensos a error.

**SIGESTA** resuelve esta problemática centralizando la gestión de tareas mediante un modelo inmutable y funciones puras. Permite autenticar roles diferenciados (**JEFE** y **TRABAJADOR**), registrar tareas delegadas o autogestionadas, efectuar transiciones de estado libres de efectos colaterales y consolidar estadísticas globales en tiempo real.

---

## 2. Estructuras de datos utilizadas

El modelado del dominio se encuentra definido en el módulo [modelos.py](../src/models/modelos.py) utilizando decoradores `@dataclass(frozen=True)` y colecciones inmutables:

```python
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
    descripcion: Optional[str] = None  # Campo opcional al final

@dataclass(frozen=True)
class EstadoSistema:
    tareas: tuple[Tarea, ...] = ()
    usuarios: tuple[Usuario, ...] = ()
```

### Justificación técnica de las estructuras:
- **`@dataclass(frozen=True)`:** Garantiza que las instancias de [Usuario](../src/models/modelos.py#L4-L10), [Tarea](../src/models/modelos.py#L12-L19) y [EstadoSistema](../src/models/modelos.py#L21-L24) sean de sólo lectura. Cualquier intento de mutación in-place (como `tarea.estado = "HECHO"`) eleva en tiempo de ejecución una excepción `FrozenInstanceError`.
- **`tuple` en lugar de `list`:** En Python, las listas son mutables por referencia (`.append()`, `.pop()`, modificación por índice). Se empleó `tuple[Tarea, ...]` y `tuple[Usuario, ...]` porque las tuplas son tipos inmutables por diseño, lo que garantiza que la colección completa sea inalterable una vez instanciada.
- **`typing.Optional`:** Se utilizó `Optional[str]` para el campo `descripcion`, representando de forma explícita y tipada la presencia o ausencia de detalles adicionales en la tarea.

---

## 3. Dónde se aplicó la Unidad 1

La Unidad 1 abarca funciones de orden superior, pattern matching, modelado estructurado de datos y la comparativa entre paradigmas.

### 3.1. Funciones de Orden Superior (Higher-Order Functions)
Una función de orden superior es aquella que recibe funciones como argumentos y/o retorna una función como resultado:
- **Funciones como retorno (Fábricas / Closures):** En [filters.py](../src/core/filters.py), las funciones [crearFiltroCredenciales](../src/core/filters.py#L8-L12) y [crearFiltroPorAsignado](../src/core/filters.py#L29-L33) retornan predicados funcionales (`criterio`) que encapsulan condiciones de filtrado.
- **Funciones como argumento:** En [filters.py](../src/core/filters.py#L19-L22), [autenticarUsuario](../src/core/filters.py#L19-L22) y [obtenerTareasPorUsuario](../src/core/filters.py#L39-L41) suministran estos predicados a la función de orden superior nativa `filter`. Asimismo, en [transformations.py](../src/core/transformations.py), [calcularEstadisticasEstado](../src/core/transformations.py#L10-L17) pasa la función `acumulador` a `functools.reduce`.

### 3.2. Pattern Matching (`match / case`)
El control de flujo declarativo mediante `match/case` se aplicó en la capa de interacción en [consola.py](../src/ui/consola.py):
- **Despacho del menú principal:** En la función [procesarOpcion](../src/ui/consola.py#L46-L58):
  ```python
  match opcion:
      case 1:
          return iniciarSesion(estado)
      case 2:
          return crearCuenta(estado)
      case 3:
          print("Saliendo de la aplicación...")
          return estado
      case _:
          print("Opción inválida.")
          return estado
  ```
- **Ruteo de operaciones por rol:** En [menuSesion](../src/ui/consola.py#L153-L211), se evalúan las acciones correspondientes a `JEFE` o `TRABAJADOR` con patrones exhaustivos que gestionan la creación, asignación, filtrado y actualización de estados.

### 3.3. Modelado de Datos
Implementado formalmente en [modelos.py](../src/models/modelos.py) mediante `@dataclass(frozen=True)` para [Usuario](../src/models/modelos.py#L4), [Tarea](../src/models/modelos.py#L12) y [EstadoSistema](../src/models/modelos.py#L21), garantizando contratos inmutables sin recurrir a clases tradicionales basadas en mutación de estado interno (`self.__dict__`).

### 3.4. Comparativa Funcional vs. Imperativo
A continuación se contrasta el cálculo del resumen de estados de tareas:

* **Enfoque Imperativo tradicional (con mutación y variables de control):**
  ```python
  # Enfoque imperativo: mutación in-place de diccionario y bucle for
  def calcularEstadisticasImperativo(tareas):
      resultado = {"HECHO": 0, "EN_PROCESO": 0, "NO_INICIADO": 0}
      for t in tareas:
          if t.estado in resultado:
              resultado[t.estado] += 1  # Mutación del estado compartido
      return resultado
  ```
* **Enfoque Funcional en SIGESTA ([transformations.py](../src/core/transformations.py#L10-L17)):**
  ```python
  # Enfoque funcional: función pura, sin mutación externa, con reduce
  def calcularEstadisticasEstado(tareas: tuple[Tarea, ...]) -> dict[str, int]:
      def acumulador(conteo: dict[str, int], t: Tarea) -> dict[str, int]:
          copia = dict(conteo)
          copia[t.estado] = copia.get(t.estado, 0) + 1
          return copia

      estadoInicial = {"HECHO": 0, "EN_PROCESO": 0, "NO_INICIADO": 0}
      return reduce(acumulador, tareas, estadoInicial)
  ```
* **Beneficio del enfoque funcional:** No existen variables acumuladoras globales ni mutación de referencias compartidas. La función `acumulador` recibe el valor previo y el elemento actual, devolviendo una nueva proyección sin efectos secundarios.

---

## 4. Dónde se aplicó la Unidad 2

La Unidad 2 profundiza en el uso de funciones anónimas (`lambda`), clausuras léxicas (`closures`), inmutabilidad estricta, pureza referencial y operadores funcionales estándar (`map`, `filter`, `reduce`).

### 4.1. Lambdas
- En [dispatcher.py](../src/core/dispatcher.py#L51-L58): En [cambiarEstadoTarea](../src/core/dispatcher.py#L51-L58), se utiliza un `lambda` como transformación condicional para `map`:
  ```python
  map(lambda t: replace(t, estado=nuevoEstado) if t.id == idTarea else t, estadoActual.tareas)
  ```
- En [repository.py](../src/storage/repository.py#L19-L25): En [cargarEstado](../src/storage/repository.py#L12-L30), para hidratar los diccionarios leídos del archivo JSON en dataclasses inmutables:
  ```python
  map(lambda u: Usuario(**u), datos.get("usuarios", []))
  map(lambda t: Tarea(**t), datos.get("tareas", []))
  ```
- En [transformations.py](../src/core/transformations.py#L23-L38): En [obtenerRankingCumplimiento](../src/core/transformations.py#L23-L38), para aislar tareas terminadas (`lambda t: t.estado == "HECHO"`) y ordenar el ranking (`key=lambda item: item[1]`).

### 4.2. Closures
Implementados en [filters.py](../src/core/filters.py) para encapsular parámetros en un entorno léxico cerrado sin necesidad de recurrir a objetos con estado interno (`self`). Detallado en el punto 8.

### 4.3. Inmutabilidad
- Aplicación de *Copy-and-Update* mediante `dataclasses.replace` en [dispatcher.py](../src/core/dispatcher.py):
  - [agregarUsuario](../src/core/dispatcher.py#L13-L29): Genera una nueva tupla de usuarios mediante concatenación (`estadoActual.usuarios + (nuevoUsuario,)`) y retorna una nueva instancia de [EstadoSistema](../src/models/modelos.py#L21) sin alterar el estado previo.
  - [agregarTarea](../src/core/dispatcher.py#L37-L44): Idéntico mecanismo para la tupla de tareas.
  - [cambiarEstadoTarea](../src/core/dispatcher.py#L51-L58): Construye una nueva tupla proyectando la tarea modificada con `replace`.

### 4.4. Pureza y Efectos Secundarios
Toda la lógica de dominio en `src/core/` ([dispatcher.py](../src/core/dispatcher.py), [filters.py](../src/core/filters.py), [transformations.py](../src/core/transformations.py)) está compuesta exclusivamente por funciones puras. Los efectos secundarios (I/O, mutaciones de interfaz de usuario) se aislaron de manera estricta en `src/storage/` y `src/ui/`.

### 4.5. Operadores Funcionales (`map`, `filter`, `reduce`)
- **`map`:** Empleado en [dispatcher.py](../src/core/dispatcher.py#L53) para actualizar el estado de una tarea conservando las restantes intactas, y en [repository.py](../src/storage/repository.py#L20) para transformar diccionarios crudos a instancias de modelos.
- **`filter`:** Empleado en [filters.py](../src/core/filters.py#L21) para autenticación de credenciales, en [filters.py](../src/core/filters.py#L41) para segregar tareas por colaborador, y en [transformations.py](../src/core/transformations.py#L24) para seleccionar tareas completadas.
- **`reduce`:** Empleado en [transformations.py](../src/core/transformations.py#L17) mediante `functools.reduce` para agregar el total de tareas agrupadas por su estado.

### 4.6. Fragmento técnico: ¿Por qué NO convenía usar `lambda`?
En la función [calcularEstadisticasEstado](../src/core/transformations.py#L10-L17) de [transformations.py](../src/core/transformations.py):

```python
def calcularEstadisticasEstado(tareas: tuple[Tarea, ...]) -> dict[str, int]:
    def acumulador(conteo: dict[str, int], t: Tarea) -> dict[str, int]:
        copia = dict(conteo)
        copia[t.estado] = copia.get(t.estado, 0) + 1
        return copia

    estadoInicial = {"HECHO": 0, "EN_PROCESO": 0, "NO_INICIADO": 0}
    return reduce(acumulador, tareas, estadoInicial)
```

#### Justificación técnica de rechazo a `lambda`:
1. **Restricción sintáctica de Python:** Las funciones `lambda` en Python están limitadas a una única expresión evaluable. No permiten sentencias de asignación múltiple ni clonaciones explícitas de estado en líneas independientes.
2. **Preservación de inmutabilidad sin hacks crípticos:** Si se hubiera forzado el uso de una lambda para el acumulador de `reduce`, se habría tenido que escribir una expresión compleja como:
   ```python
   # Anti-patrón forzado con lambda:
   reduce(lambda c, t: {**c, t.estado: c.get(t.estado, 0) + 1}, tareas, estadoInicial)
   ```
   Aunque sintácticamente válida, desempaquetar diccionarios repetidamente `{**c, ...}` en cada iteración degrada el rendimiento de memoria ($O(N \cdot K)$ donde $K$ es el número de claves) y perjudica notablemente la legibilidad del código.
3. **Depuración y Stacktraces:** Una función definida nominalmente (`acumulador`) genera nombres claros en el stacktrace en caso de error y permite documentar y validar el tipo de entrada (`conteo: dict[str, int], t: Tarea`), mientras que un lambda anónimo oculta el contexto y dificulta el mantenimiento del software.

---

## 5. Qué partes son puras y cuáles impuras

El proyecto se diseñó bajo la arquitectura **Functional Core, Imperative Shell**, trazando una frontera estricta entre la lógica de negocio y las operaciones con el mundo exterior:

```
┌──────────────────────────────────────────────────────────────┐
│                  IMPERATIVE SHELL (IMPURA)                   │
│                                                              │
│  src/ui/gui.py       src/ui/consola.py    src/storage/       │
│  (Tkinter / Eventos) (print / input)      repository.py      │
│                                           (Lectura/Escritura)│
└──────────────────────────────┬───────────────────────────────┘
                               │ Invoca pasando estado
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   FUNCTIONAL CORE (PURA)                     │
│                                                              │
│  src/core/dispatcher.py  src/core/filters.py  src/core/      │
│  (Copy-and-Update)       (Closures / Filter)  transformations│
│                                               (Map / Reduce) │
│                                                              │
│  src/models/modelos.py (dataclasses frozen / Tuplas)         │
└──────────────────────────────────────────────────────────────┘
```

### 5.1. Partes Puras (Núcleo Funcional - `src/core/` y `src/models/`)
Cumplen con **transparencia referencial**: dadas las mismas entradas, siempre retornan la misma salida y no producen efectos secundarios observables fuera de su ámbito local.
1. [agregarUsuario](../src/core/dispatcher.py#L13): Recibe un [EstadoSistema](../src/models/modelos.py#L21) y strings; retorna un nuevo [EstadoSistema](../src/models/modelos.py#L21).
2. [agregarTarea](../src/core/dispatcher.py#L37): Recibe un [EstadoSistema](../src/models/modelos.py#L21) y datos de tarea; retorna un nuevo [EstadoSistema](../src/models/modelos.py#L21).
3. [cambiarEstadoTarea](../src/core/dispatcher.py#L51): Proyecta la tupla de tareas mediante `map` y retorna un nuevo [EstadoSistema](../src/models/modelos.py#L21).
4. [crearFiltroCredenciales](../src/core/filters.py#L8) y [crearFiltroPorAsignado](../src/core/filters.py#L29): Fábricas de predicados que no leen ni alteran variables externas.
5. [autenticarUsuario](../src/core/filters.py#L19) y [obtenerTareasPorUsuario](../src/core/filters.py#L39): Filtrado sobre tuplas inmutables.
6. [calcularEstadisticasEstado](../src/core/transformations.py#L10) y [obtenerRankingCumplimiento](../src/core/transformations.py#L23): Agregaciones analíticas con `reduce`, `map` y `filter`.

### 5.2. Partes Impuras (Cáscara Imperativa - `src/storage/`, `src/ui/` y `main.py`)
Contienen efectos secundarios inevitables para interactuar con el entorno exterior:
1. [cargarEstado](../src/storage/repository.py#L12): Lee el archivo `data/estado_sistema.json` del disco (su resultado depende del estado del sistema de archivos en ese instante).
2. [guardarEstado](../src/storage/repository.py#L37): Escribe y sobrescribe datos en el disco físico.
3. [iniciarCli](../src/ui/consola.py#L15), [menu](../src/ui/consola.py#L26), [crearCuenta](../src/ui/consola.py#L81): Utilizan `input()` y `print()` para I/O estándar.
4. [iniciarGui](../src/ui/gui.py) y vistas de Tkinter: Modifican widgets gráficos, escuchan eventos de ratón/teclado y ejecutan `mainloop()`.
5. [main.py](../main.py): Inspecciona argumentos del sistema operativo (`sys.argv`) para bifurcar el inicio del programa.

---

## 6. Qué efectos secundarios existen

En SIGESTA, los efectos secundarios se mantuvieron confinados a la periferia del sistema:
1. **Entrada/Salida en Disco (Disk I/O):**
   - Lectura y parsing de `data/estado_sistema.json` al iniciar la aplicación.
   - Serialización de dataclasses a diccionarios con `asdict` y escritura atómica en archivo local al guardar.
2. **Entrada/Salida Estándar (Terminal I/O):**
   - Emisión de cadenas en consola mediante `print()` para menús y tablas.
   - Bloqueo de hilo para captura de teclado del usuario mediante `input()`.
3. **Efectos de Interfaz Gráfica (GUI State Mutation):**
   - Modificación de la memoria de Tkinter al crear, destruir y redibujar componentes (`Frame`, `Treeview`, `Label`).
   - Apertura de diálogos modales del sistema operativo (`messagebox.showinfo`, `messagebox.showerror`).
4. **Acceso al Entorno de Ejecución:**
   - Lectura de parámetros de invocación de Python (`sys.argv`).

---

## 7. Qué parte del estado se manejó de forma inmutable

**La totalidad del estado del dominio se manejó de forma inmutable.**

1. **Entidades del Dominio:**
   - Ningún atributo de [Usuario](../src/models/modelos.py#L4) o [Tarea](../src/models/modelos.py#L12) puede reasignarse tras su creación debido a `frozen=True`.
2. **Colecciones:**
   - En lugar de listas dinámicas, las colecciones de tareas y usuarios se representan como `tuple[Tarea, ...]`. Las tuplas no poseen métodos como `.append()`, `.extend()` o `.pop()`, impidiendo alteraciones accidentales.
3. **Transición de Estados (Copy-and-Update):**
   - Para insertar un nuevo elemento, se genera una tupla derivada mediante el operador de concatenación `+`:
     ```python
     nuevasTareas: tuple[Tarea, ...] = estadoActual.tareas + (nuevaTarea,)
     return replace(estadoActual, tareas=nuevasTareas)
     ```
   - Para modificar una propiedad existente, se combina `map` con la función pura `dataclasses.replace`:
     ```python
     nuevasTareas: tuple[Tarea, ...] = tuple(
         map(
             lambda t: replace(t, estado=nuevoEstado) if t.id == idTarea else t,
             estadoActual.tareas
         )
     )
     return replace(estadoActual, tareas=nuevasTareas)
     ```
   - De esta manera, el estado anterior permanece inmutable en memoria y nunca es destruido ni corrompido durante las transformaciones.

---

## 8. Qué closure se implementó y para qué

Se implementaron dos clausuras léxicas (*closures*) en [filters.py](../src/core/filters.py):

### 8.1. Closure de Autenticación de Credenciales
```python
def crearFiltroCredenciales(correo: str, password: str):
    def criterio(user: Usuario) -> bool:
        return user.correo == correo and user.password == password

    return criterio
```
- **Ámbito Léxico (*Lexical Scope*):** La función interna `criterio` retiene y recuerda los parámetros `correo` y `password` provistos a la función contenedora `crearFiltroCredenciales`.
- **Para qué se implementó:** Permite fabricar un predicado unario `Usuario -> bool` configurable, el cual se transfiere directamente a la función de orden superior `filter` en [autenticarUsuario](../src/core/filters.py#L19-L22):
  ```python
  filtroLogin = crearFiltroCredenciales(correo, password)
  usuariosCoincidentes = tuple(filter(filtroLogin, usuarios))
  ```
  Esto evita crear clases autenticadoras con atributos internos mutables o acoplar la lógica de validación al bucle de búsqueda.

### 8.2. Closure de Filtrado de Tareas por Destinatario
```python
def crearFiltroPorAsignado(idUsuario: int):
    def criterio(t: Tarea) -> bool:
        return t.asignadoA == idUsuario

    return criterio
```
- **Ámbito Léxico:** La función interna `criterio` captura la variable `idUsuario`.
- **Para qué se implementó:** Genera un predicado unario reutilizable `Tarea -> bool` que permite a [obtenerTareasPorUsuario](../src/core/filters.py#L39-L41) filtrar la tupla global de tareas según el colaborador en sesión, garantizando que el jefe o el trabajador solo operen sobre las tareas correspondientes.

---

## 9. Qué partes sugirió la IA

Con base en la [bitácora de interacciones](../docs/bitacora-ia.md), la IA asistió en los siguientes componentes:
1. **Estructura Arquitectónica:** Sugirió desacoplar el proyecto separando el núcleo puro (`src/core/`) de la persistencia impura (`src/storage/`) y las interfaces (`src/ui/`), adoptando el patrón *Functional Core, Imperative Shell* en lugar de una arquitectura clásica orientada a objetos (Entity-Service-Controller).
2. **Modelado Inmutable Inicial:** Propuso el uso de `@dataclass(frozen=True)` para definir las entidades del dominio con verificación de tipos.
3. **Estructura Base de Closures:** Sugirió el diseño inicial de las fábricas de predicados para filtrado con funciones anidadas.
4. **Batería de Pruebas y Casos de Uso:** Generó secuencias exhaustivas de entradas para validar todos los caminos de ejecución del CLI (registro, autenticación, creación de tareas delegadas y personales, y cálculo de reportes analíticos).
5. **Esqueleto de Interfaz Gráfica:** Sugirió la integración de `ttkbootstrap` con paleta moderna oscura y los layouts iniciales de paneles y tablas.

---

## 10. Qué corrigieron o rechazaron de la IA

Durante el desarrollo se ejercitó un estricto criterio técnico sobre las propuestas generadas por la IA, rechazando y corrigiendo las siguientes decisiones erróneas o subóptimas:

### 10.1. Conflicto de nombres con la biblioteca estándar de Python (Rechazado y Corregido)
- **Problema sugerido por la IA:** Inicialmente la IA propuso ubicar los modelos en un archivo llamado `src/models/types.py`. Al ejecutar el sistema, Python arrojó el error crítico:  
  `ImportError: cannot import name 'dataclass' from partially initialized module 'dataclasses'`.
- **Causa técnica:** El nombre `types.py` colisionaba con el módulo nativo `types` de la biblioteca estándar de Python, provocando una importación circular en la inicialización del intérprete.
- **Corrección:** Se rechazó la sugerencia de la IA, renombrando el módulo a [modelos.py](../src/models/modelos.py).

### 10.2. Orden de campos con valores por defecto en Dataclasses (Corregido)
- **Problema sugerido por la IA:** La IA colocó el campo opcional `descripcion: Optional[str] = None` en medio de los atributos obligatorios de la dataclass `Tarea`.
- **Causa técnica:** En Python, un argumento sin valor por defecto no puede ir después de un argumento con valor por defecto (`SyntaxError: non-default argument follows default argument`).
- **Corrección:** Se reordenó la estructura colocando `descripcion` estrictamente al final de la definición de [Tarea](../src/models/modelos.py#L12-L19).

### 10.3. Sobreingeniería con `typing.Callable` en Closures (Rechazado y Simplificado)
- **Propuesta de la IA:** La IA sugirió tipar las funciones internas y de orden superior con `Callable[[Usuario], bool]`, requiriendo importaciones adicionales y aumentando la verbosidad de las firmas funcionales.
- **Decisión técnica:** Se rechazó la sobrecarga sintáctica en [filters.py](../src/core/filters.py), optando por firmas concisas, adaptando la nomenclatura a `camelCase` uniforme y retornando la entidad de usuario completa en lugar de un simple booleano para optimizar el flujo de sesión.

### 10.4. Pérdida del Estado Inmutable en el Bucle de Consola (Detectado y Corregido)
- **Problema detectado:** Al ejecutar las pruebas del CLI, se identificó que la función `procesarOpcion` ejecutaba `iniciarSesion(estado)`, pero retornaba la variable vieja `estado` previa a la sesión. Debido a esto, las nuevas tareas creadas por el usuario dentro del submenú se descartaban de la memoria al volver al menú principal.
- **Corrección:** Se modificó la firma a `iniciarSesion(estado: EstadoSistema) -> EstadoSistema` y se encadenó el retorno (`return iniciarSesion(estado)`), garantizando que la nueva versión del estado producida por *Copy-and-Update* fluya correctamente entre las iteraciones del bucle interactivo.

---

## 11. Qué aprendieron técnicamente

El desarrollo de SIGESTA permitió consolidar aprendizajes conceptuales y prácticos clave sobre la programación funcional:

1. **Comprensión profunda de la Inmutabilidad:** Se asimiló que en el paradigma funcional los objetos no se alteran "en el lugar" (*in-place*). El flujo de datos se basa en transformaciones que devuelven nuevas versiones del estado (*Copy-and-Update*). Esto elimina errores por aliasing, dependencias ocultas entre módulos y efectos colaterales imprevistos.
2. **Arquitectura *Functional Core, Imperative Shell*:** Se aprendió a desacoplar de forma rigurosa la lógica pura de negocio (la cual es determinista, fácilmente testeable y libre de efectos colaterales) de la cáscara impura (lectura de disco, formularios de interfaz gráfica y entradas de consola). Esto demostró que la programación funcional es compatible y altamente beneficiosa para aplicaciones con interfaz de usuario.
3. **Potencia expresiva de `map`, `filter` y `reduce`:** Se evidenció cómo las operaciones sobre colecciones pueden declararse de forma clara y concisa sin necesidad de recurrir a bucles `for` tradicionales con banderas mutables y contadores manuales.
4. **Dominio de Closures y Funciones de Primera Clase:** Se comprobó cómo una función puede comportarse como un valor más dentro del lenguaje, y cómo un closure permite encapsular configuraciones de manera elegante sin necesidad de instanciar clases orientadas a objetos con estado mutable.
5. **Criterio Crítico en el uso de IA:** Se consolidó que los modelos de lenguaje son aceleradores eficientes para tareas mecánicas y borradores iniciales, pero carecen de visión de integración profunda del entorno (como colisiones con librerías estándar o sutiles pérdidas de estado inmutable). El criterio del programador es el único garante de la corrección arquitectónica y de la fidelidad conceptual del paradigma.