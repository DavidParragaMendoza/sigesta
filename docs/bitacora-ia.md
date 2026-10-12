<div align="center">

# 🤖 Bitácora de IA

### Pensar, cuestionar, corregir: IA con criterio de ingeniería

<p>
  <img src="https://img.shields.io/badge/Proceso-Transparente-3776AB?style=for-the-badge" alt="Proceso transparente">
  <img src="https://img.shields.io/badge/Decisiones-Críticas-F39C12?style=for-the-badge" alt="Decisiones críticas">
  <img src="https://img.shields.io/badge/Resultado-Explicable-2E7D32?style=for-the-badge" alt="Resultado explicable">
</p>

</div>

> Registro de prompts, propuestas, correcciones y decisiones técnicas tomadas
> durante la construcción de SIGESTA. La IA acelera el trabajo; el criterio
> del desarrollador valida cada resultado.

**Proyecto:** SIGESTA Funcional — Gestor de Tareas con Interfaz Gráfica  
**Autor:** Ronald David Párraga Mendoza · **Asignatura:** Programación Funcional  
**Docente:** Ing. Anthony Pachay Espinoza · **Institución:** UPSE · **Semestre:** 2026-1

---

## 📌 1. Filosofía de Uso de la IA y Criterio de Control

De acuerdo con las exigencias de la **Guía de la Actividad Integradora (Unidades 1 y 2)**, la Inteligencia Artificial se utilizó como un **consultor de arquitectura, asistente de diseño visual, formulador de pruebas y acelerador de código repetitivo**, manteniendo en todo momento el criterio técnico humano como filtro obligatorio:

1. **Aislamiento Arquitectónico (*Functional Core, Imperative Shell*):** Se garantizó que la lógica del núcleo (`src/core/`) permanezca 100% pura, sin dependencias de disco, base de datos ni elementos de interfaz gráfica.
2. **Inmutabilidad Estricta:** Se rechazó cualquier sugerencia de la IA que utilizara `.append()`, mutación directa de atributos o reasignación en el lugar, imponiendo el patrón *Copy-and-Update* con `dataclasses.replace` y tuplas inmutables.
3. **Cero Lógica en Callbacks:** Se estructuró la GUI (`src/ui/gui.py`) para que los eventos de botones y tablas actúen como invocadores pasivos que extraen datos, delegan al núcleo puro, persisten con `storage` y refrescan la vista.
4. **Filtro de Relevancia Académica:** Cada concepto evaluado (**closures**, **HOFs**, **pattern matching**, **inmutabilidad**, **reduce**) responde a un problema de dominio real del gestor de tareas y no a un adorno sintáctico.

---

## 🗺️ 2. Resumen Ejecutivo de Interacciones

| # | Fase / Hito | Prompt / Consulta Central | Sugerencia de IA | Veredicto | Justificación Técnica |
|---|---|---|---|:---:|---|
| **01** | Fase 1: CLI | ¿Reutilizar C++/SQL o crear un gestor funcional en memoria? | Transicionar a *Functional Core, Imperative Shell* con persistencia JSON | 🟢 **Aceptado** | Evita que SQL contamine la pureza referencial de las funciones y deja espacio real para `map`, `filter` y `reduce`. |
| **02** | Fase 1: CLI | ¿Por qué usar paquetes `models`, `core`, `storage` y no MVC / Java Spring? | Explicó choque de paradigmas: OOP muta estado, PF aísla pureza de I/O | 🟢 **Aceptado** | Nombres claros que justifican ante la rúbrica las capas puras vs. las impuras con I/O. |
| **03** | Fase 1: CLI | Crear prueba de humo en consola (`main.py` llamando a `cli.py`) | Importación modular relativa `from src.ui.cli import iniciarCli` | 🟢 **Aceptado** | Permite verificar rutas de paquetes en Python antes de definir las entidades. |
| **04** | Fase 1: CLI | Resolver `ImportError` cíclico en `types.py` y `TypeError` en `Tarea` | Renombrar archivo a `modelos.py` y mover campos con default al final | 🟡 **Modificado** | Solucionó la colisión con la librería nativa `types.py` de Python y habilitó `@dataclass(frozen=True)`. |
| **05** | Fase 1: CLI | Explicar desempaquetado `**t` en `map(lambda t: Tarea(**t), datos)` | Explicó conversión declarativa de diccionarios JSON a tuplas inmutables | 🟢 **Aceptado** | Mapeo declarativo de JSON a estructuras inmutables sin usar loops imperativos `for`. |
| **06** | Fase 1: CLI | Implementación de closure en `src/core/filters.py` | Propuso fábrica con `from typing import Callable` y retorno puramente booleano | 🔴 **Rechazado / Modificado** | Se rechazó `Callable` por verbosidad. Se adaptó a `camelCase` y se retornó la entidad `Usuario` (o `None`). |
| **07** | Fase 1: CLI | Corregir pérdida de tareas en consola al cambiar de sesión | Detección de descarte del estado en `procesarOpcion` de `consola.py` | 🟢 **Aceptado** | Encadenar `return iniciarSesion(estado)` para propagar la inmutabilidad vía *Copy-and-Update*. |
| **08** | Fase 1: CLI | Lógica de tareas, estadísticas con `reduce` y actualización inmutable | `agregarTarea`, `cambiarEstadoTarea` con `replace` y `reduce` en `transformations.py` | 🟢 **Aceptado** | Implementación pura de métricas acumuladas con `functools.reduce` y actualización inmutable. |
| **09** | Fase 2: Stitch | Prompts para maquetación Notion Dark (#111212) en Google Stitch | Fichas de estado semáforo pastel y 4 vistas conceptuales | 🟡 **Modificado** | Se tomaron los tokens de color y distribución visual, descartando por completo el código web/Tailwind. |
| **10** | Fase 3: GUI | Ensamblar `src/ui/gui.py` con `ttkbootstrap` y cero lógica en callbacks | Estrategia de Frames modulares coordinados por el controlador `App` | 🟢 **Aceptado** | Callbacks pasivos que delegan a `src/core/`, persisten y actualizan el estado inmutable. |
| **11** | Fase 3: GUI | Depuración de 7 fallos de usabilidad y seguridad de roles | Separación de "Mis Tareas" y "Tareas del Personal" con nueva función pura | 🟢 **Aceptado** | Aislamiento estricto de permisos entre el rol JEFE y TRABAJADOR mediante `filter()`. |

---

## ⏱️ 3. Línea de Tiempo Detallada de Interacciones

```
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                                LÍNEA DE TIEMPO DE INTERACCIONES CON IA                              │
  └─────────────────────────────────────────────────────────────────────────────────────────────────────┘
     │
     ├── 🟢 FASE 1: NÚCLEO FUNCIONAL Y ARQUITECTURA EN CONSOLA (CLI)
     │    ├── Interacción 1.1: Transición de C++/SQL a Monolito Funcional en Memoria
     │    ├── Interacción 1.2: Justificación de Arquitectura (Functional Core vs. MVC)
     │    ├── Interacción 1.3: Prueba de Humo y Conexión Inicial `main.py` -> `cli.py`
     │    ├── Interacción 1.4: Modelado Inmutable y Resolución de Conflictos (`modelos.py`)
     │    ├── Interacción 1.5: Desempaquetado `**t` en `map` para Deserialización JSON
     │    ├── Interacción 1.6: Closure de Autenticación en `src/core/filters.py`
     │    ├── Interacción 1.7: Corrección de Pérdida de Estado Inmutable en Consola
     │    └── Interacción 1.8: Creación de Tareas y Estadísticas con `functools.reduce`
     │
     ├── 🎨 FASE 2: IDEACIÓN Y MAQUETACIÓN VISUAL (Gemini + Google Stitch)
     │    ├── Interacción 2.1: Especificación de Tokens de Diseño Notion Dark
     │    └── Interacción 2.2: Descarte de HTML/Tailwind y Traducción a Desktop
     │
     └── 💻 FASE 3: CONSTRUCCIÓN Y REFINAMIENTO DE LA GUI (Tkinter & Ttkbootstrap)
          ├── Interacción 3.1: Ensamblaje de `src/ui/gui.py` con Cero Lógica en Callbacks
          └── Interacción 3.2: Corrección de 7 Fallos de Usabilidad y Control Estricto de Roles
```

---

### 🟢 FASE 1: NÚCLEO FUNCIONAL Y ARQUITECTURA EN CONSOLA (CLI)

#### 🔹 Interacción 1.1: Transición de Paradigma (C++/SQL vs. Monolito Funcional)

* **Prompt Real del Desarrollador:**
  > *"Hablemos de programación funcional, Python, interfaces gráficas y un PDF que te voy a pasar. Yo tengo un proyecto antiguo que realicé en C++, es un gestor de tareas, que se conectaba a una base de datos y podías compartir las tareas con ciertos usuarios. Quiero que me digas por qué es mala idea: ¿crees que sea buena idea crear una versión de SIGESTA para este proyecto de mi materia de programación funcional? ¿Crees que sea posible implementar todos los requisitos? Mi duda es: ¿no es posible hacer o usar sentencias SQL en Python usando lambdas o funciones de orden superior, o eso complica de más el proyecto?"*

* **Sugerencia de la IA:**
  Explicó que arrastrar sentencias SQL (`INSERT`, `UPDATE`, `cursor.fetchall()`) destruye la pureza referencial exigida por la rúbrica y hace redundantes a `map`, `filter` y `reduce`. Propuso adaptarlo como un monolito modular con estado inmutable en memoria (*Functional Core, Imperative Shell*) con un único archivo JSON para persistencia atómica.

* **Fragmento Sugerido por la IA:**
  ```python
  # Patrón propuesto: Functional Core, Imperative Shell
  # storage/repository.py -> Carga/guarda el JSON (efecto secundario / I/O)
  # core/ -> Lógica pura que transforma tuplas inmutables en memoria
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Descartar por completo el motor MySQL y adoptar la arquitectura *Functional Core, Imperative Shell*.
  * 🎯 **Por qué:** Permite aislar los efectos secundarios de I/O en `src/storage/repository.py`, garantizando que el 100% de las reglas del negocio en `src/core/` sean funciones deterministas y puras, cumpliendo la regla de diseño obligatoria de la guía.

---

#### 🔹 Interacción 1.2: Justificación Arquitectónica (Estructura de Paquetes vs. Java Spring/MVC)

* **Prompt Real del Desarrollador:**
  > *"¿Por qué usamos estos nombres de paquetes: `src -> core, models, storage` y no algo como modelo, vista, controlador o es algo parecido (como en Java: `Entity, Repository, DTO, Service, Controller`)?"*

* **Sugerencia de la IA:**
  Explicó la diferencia conceptual entre POO (entidades mutables y servicios que mezclan llamadas a BD con lógica) y la Programación Funcional (tipos inmutables, núcleo puro sin I/O, y cáscara de almacenamiento).

* **Matriz Comparativa Presentada por la IA:**
  ```
  Java / POO (Spring)        ──>  SIGESTA Funcional (Python)
  -------------------             --------------------------
  Entity / DTO                ──>  models/modelos.py (@dataclass frozen=True)
  Service (Lógica + I/O)      ──>  core/ (Transformaciones y Filtros Puros)
  Repository (SQL)            ──>  storage/repository.py (I/O JSON Impuro)
  Controller / View           ──>  ui/ (cli.py / gui.py)
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Nombres `models` (modelos inmutables), `core` (cálculo puro) y `storage` (persistencia JSON impura).
  * 🎯 **Por qué:** Evita mezclar consultas de disco o mutaciones dentro de las "Services" y justifica claramente ante la rúbrica qué partes son 100% puras y cuáles son impuras por I/O.

---

#### 🔹 Interacción 1.3: Prueba de Humo y Conexión Inicial (`main.py` -> `cli.py`)

* **Prompt Real del Desarrollador:**
  > *"Ah, tú quieres comenzar a crear las entidades, dice uno. (Hago un símil: en una API de Java hacemos primero el paquete model que es el que se conecta con JPA y crea la base de datos). ¿Quieres hacer algo similar tú? Pero lo que yo quiero es ir a CLI, poner un 'Hola Mundo', y luego ir a main y ejecutar y que salga el 'Hola Mundo'."*

* **Sugerencia de la IA:**
  Propuso crear primero la función `iniciarCli()` en `src/ui/cli.py` e importarla en `main.py` mediante la ruta de paquetes relativa `from src.ui.cli import iniciarCli`, validando la estructura del proyecto antes de escribir las clases de dominio.

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Ejecutar una prueba de humo (*smoke test*) en consola.
  * 🎯 **Por qué:** Asegura que el intérprete de Python reconozca el paquete `src` (con sus archivos `__init__.py`) sin errores de módulo antes de construir las estructuras de datos.

---

#### 🔹 Interacción 1.4: Modelado Inmutable y Conflicto en el Espacio de Nombres

* **Prompt Real del Desarrollador:**
  > *"Tengo este error: `ImportError: cannot import name 'dataclass' from partially initialized module 'dataclasses' (most likely due to a circular import) (C:\Users\ASUS\Desktop\SIGESTA\src\models\types.py)`. Y luego me salió: `TypeError: non-default argument 'prioridad' follows default argument 'descripcion'`."*

* **Sugerencia de la IA:**
  Identificó dos errores fundamentales:
  1. Nombrar el archivo como `src/models/types.py` colisionaba con el módulo nativo `types.py` de la biblioteca estándar de Python (utilizado por `dataclasses` y `enum`), provocando una importación circular.
  2. En `@dataclass`, colocar `descripcion: Optional[str] = None` (con valor por defecto) antes de campos obligatorios (`prioridad: str`).

* **Código Comparativo (`diff`):**
  ```diff
  # En src/models/ (renombrado de types.py a modelos.py)
   from dataclasses import dataclass
   from typing import Optional

   @dataclass(frozen=True)
   class Tarea:
       id: int
       titulo: str
  -    descripcion: Optional[str] = None  # ERROR: Campo opcional con default antes de obligatorios
       prioridad: str
       estado: str
       asignadoA: int
  +    descripcion: Optional[str] = None  # SOLUCIÓN: Campos opcionales siempre al final
  ```

* **Criterio Técnico y Decisión:**
  * 🟡 **Modificado:** Se renombró el módulo a `src/models/modelos.py` y se reordenaron los atributos de la dataclass inmutable `Tarea`.
  * 🎯 **Por qué:** Elimina la colisión en `sys.path` y permite instanciar tipos inmutables con `@dataclass(frozen=True)` respetando las reglas sintácticas de Python.

---

#### 🔹 Interacción 1.5: Desempaquetado `**t` en `map` para Deserialización JSON

* **Prompt Real del Desarrollador:**
  > *"Sí, quiero que crees el JSON para crearlo de una vez y luego vamos despacio para ver cómo leer ese archivo... ¿Por qué usas `**` en la variable de la lambda? ¿Qué significa `map(lambda t: Tarea(**t), datos.get("tareas", []))`?"*

* **Sugerencia de la IA:**
  Explicó que `**t` es el operador de desempaquetado de diccionarios (*dictionary unpacking* / `**kwargs`), el cual convierte las claves del diccionario JSON en argumentos nombrados para el constructor de la dataclass `Tarea`.

* **Estructura Declarativa Implementada:**
  ```python
  # Transforma diccionarios mutables leídos del JSON en tuplas de objetos inmutables
  tareasInmutables: tuple[Tarea, ...] = tuple(
      map(lambda t: Tarea(**t), datos.get("tareas", []))
  )
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Uso de `map()` combinado con `**t` en `src/storage/repository.py`.
  * 🎯 **Por qué:** Permite deserializar el JSON de forma declarativa y funcional en una sola línea, transformando diccionarios mutables en tuplas inmutables sin usar bucles imperativos `for`.

---

#### 🔹 Interacción 1.6: Closure de Autenticación en `src/core/filters.py`

* **Prompt Real del Desarrollador:**
  > *"La verdad no tengo idea de cómo hacer eso solo, tengo claro que debo poner esta línea: `from src.storage.repository import cargar_estado ... def iniciarSesion(correo: str, password: str) -> bool: estado = cargar_estado()`... ¿Y aquí qué hago? ¿Cómo hago un closure o un map o un filter? (...) ¿Es necesario usar el Callable? Siento que lo hace más verboso. Dato curioso: yo no defino con `funcion_nombre`, yo uso `camelCase`: `funcionNombre`, `variableNombre`, `crearFiltroCredenciales`."*

* **Sugerencia de la IA:**
  La IA propuso inicialmente un diseño con tipado verboso `from typing import Callable` y firma `Callable[[Usuario], bool]`, haciendo que la función de autenticación devolviera únicamente `True` o `False`.

* **Código Comparativo (`diff`):**
  ```diff
  - # Sugerido inicialmente por la IA (Verbosidad innecesaria y retorno puramente booleano):
  - from typing import Callable
  - def crear_filtro_credenciales(correo: str, password: str) -> Callable[[Usuario], bool]:
  -     def criterio(u: Usuario) -> bool:
  -         return u.correo == correo and u.password == password
  -     return criterio
  - def autenticar_usuario(...) -> bool:
  -     return len(tuple(filter(filtro, usuarios))) > 0

  + # Implementación adaptada por el desarrollador (camelCase y retorno de entidad):
  + def crearFiltroCredenciales(correo: str, password: str):
  +     """Closure puro: captura 'correo' y 'password' en su entorno léxico."""
  +     def criterio(user: Usuario) -> bool:
  +         return user.correo == correo and user.password == password
  +     return criterio
  +
  + def autenticarUsuario(usuarios: tuple[Usuario, ...], correo: str, password: str) -> Optional[Usuario]:
  +     filtroLogin = crearFiltroCredenciales(correo, password)
  +     coincidentes = tuple(filter(filtroLogin, usuarios))
  +     return coincidentes[0] if len(coincidentes) > 0 else None
  ```

* **Criterio Técnico y Decisión:**
  * 🔴 **Rechazado:** El uso de `Callable` (descartado por sobrecarga de tipos) e importar `cargar_estado` dentro de `core` (rompería la pureza del núcleo).
  * 🟡 **Modificado:** Adaptación a `camelCase` y cambio de retorno para entregar la entidad `Usuario` (o `None`).
  * 🎯 **Por qué:** Cumple con la exigencia de un closure real que captura variables en su ámbito léxico para alimentar a `filter()`, permitiendo a la UI mostrar el nombre y rol del usuario sin hacer búsquedas redundantes.

---

#### 🔹 Interacción 1.7: Corrección de Pérdida de Estado Inmutable en el CLI

* **Prompt Real del Desarrollador:**
  > *"Dame las opciones para escribir en el teclado para probar todo, pero todas las opciones del programa... Mira, le dije a un agente de IA que haga las pruebas de la guía que me diste y detectó esto: al entrar como Carlos (Jefe) y crear una tarea para Ronald (Trabajador), cuando Ronald inicia sesión sale 'No hay tareas registradas'. En `consola.py` se descartaba el nuevo estado."*

* **Sugerencia de la IA (Agente de Pruebas):**
  Identificó que en `procesarOpcion` de `src/ui/consola.py`, la opción 1 ejecutaba `iniciarSesion(estado)`, pero hacía `return estado` devolviendo la variable de estado vieja en memoria y descartando las tareas recién agregadas mediante *Copy-and-Update*.

* **Código Corregido (`diff`):**
  ```diff
  # En src/ui/consola.py
   def procesarOpcion(opcion: int, estado: EstadoSistema) -> EstadoSistema:
       match opcion:
           case 1:
  -            iniciarSesion(estado)
  -            return estado   # ERROR CRÍTICO: Devolvía el estado viejo descartando cambios
  +            return iniciarSesion(estado)  # Propaga la nueva versión del estado

  -def iniciarSesion(estado: EstadoSistema) -> None:
  +def iniciarSesion(estado: EstadoSistema) -> EstadoSistema:
       ...
       if usuario is not None:
           return menuSesion(usuario, estado)
       else:
  +        return estado
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Encadenar el retorno del objeto `EstadoSistema` a lo largo de toda la jerarquía de funciones del CLI.
  * 🎯 **Por qué:** En programación funcional el estado no se modifica mediante variables globales ni punteros mutables. Debe fluir y transformarse explícitamente a través del retorno de cada función.

---

#### 🔹 Interacción 1.8: Creación de Tareas y Estadísticas con `functools.reduce`

* **Prompt Real del Desarrollador:**
  > *"Ahora el sentido del proyecto: la creación de tareas por el jefe y la asignación a un trabajador... En la consola cuando se inicia sesión y es el jefe debe salir: 1. Asignar tarea 2. Ver mis tareas 3. Estadísticas: creamos un reporte de los trabajadores que más tareas han cumplido, algo como un ranking. Y en el lado de los trabajadores solo: 1. Listar tareas 2. Agregar tarea personal. Pero no olvidamos la lógica de cambiar el estado de hecho, en proceso, terminado."*

* **Sugerencia de la IA:**
  Implementó `agregarTarea` y `cambiarEstadoTarea` en `src/core/dispatcher.py` aplicando `dataclasses.replace` y `map`, y diseñó `calcularEstadisticasEstado` en `src/core/transformations.py` utilizando `functools.reduce`.

* **Fragmento Destacado (`reduce` puro en `transformations.py`):**
  ```python
  def calcularEstadisticasEstado(tareas: tuple[Tarea, ...]) -> dict[str, int]:
      """
      Función pura: acumula el conteo de tareas por estado utilizando 'reduce'
      con un diccionario como valor inicial de identidad.
      """
      def acumulador(conteo: dict[str, int], t: Tarea) -> dict[str, int]:
          copia = dict(conteo)
          copia[t.estado] = copia.get(t.estado, 0) + 1
          return copia

      estadoInicial = {"HECHO": 0, "EN_PROCESO": 0, "NO_INICIADO": 0}
      return reduce(acumulador, tareas, estadoInicial)
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** Implementar `reduce` para sintetizar los estados en un único diccionario y `dataclasses.replace` para actualizar el estado inmutablemente.
  * 🎯 **Por qué:** Cumple con el requisito obligatorio de la Unidad 2 (`reduce`, pureza e inmutabilidad), eliminando bucles imperativos `for` con contadores mutables.

---

### 🎨 FASE 2: IDEACIÓN Y MAQUETACIÓN VISUAL (Gemini + Google Stitch)

#### 🔹 Interacción 2.1: Especificación de Tokens de Diseño para Stitch

* **Prompt Real del Desarrollador:**
  > *"Tú que sabes toda la lógica del proyecto: es momento de usar https://stitch.withgoogle.com/ para mediante prompt crear una interfaz y así el agente de IA que use no empiece de cero. Considerando que quiero una paleta de color oscura tipo Notion: #191919, y colores tipo semáforo para los estados de las tareas, también me gustaría algo tipo colores pasteles para los detalles... Tengo creado un logo con colores #354333, #111212. Stitch solo me generó una ventana... Dame un prompt que le diga que genere las que faltan... Ahora un prompt maestro."*

* **Sugerencia de la IA:**
  Diseñó un conjunto de prompts con especificaciones de color (*Design Tokens*):
  * **Fondo Principal:** `#111212` | **Sidebar / Paneles:** `#191919` | **Tarjetas:** `#202222`
  * **Acento Primario (Logo SG):** `#354333` (Verde bosque oscuro)
  * **Etiquetas Semáforo Pastel:**
    * `NO_INICIADO`: Fondo `#3A2325` / Texto coral pastel `#F29E99`
    * `EN_PROCESO`: Fondo `#36301D` / Texto ámbar pastel `#F7D486`
    * `HECHO`: Fondo `#233427` / Texto menta pastel `#9FE3A7`

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** La paleta minimalista *Notion Dark* y la división modular en 4 pantallas.
  * 🎯 **Por qué:** Proporcionó un lenguaje de diseño profesional unificado antes de programar la GUI.

---

#### 🔹 Interacción 2.2: Descarte de Código Web y Traducción a Desktop Nativo

* **Intervención Técnica del Desarrollador:**
  Google Stitch generó componentes con marcado HTML y clases de Tailwind CSS.

* **Criterio Técnico y Decisión:**
  * 🔴 **Rechazado:** Todo el código HTML/Tailwind producido por la herramienta web.
  * 🟡 **Modificado:** Se extrajeron únicamente las proporciones, paleta hexadecimal y disposición espacial para traducirlas manualmente a Tkinter y `ttkbootstrap`.
  * 🎯 **Por qué:** La guía integradora exige una aplicación de escritorio nativa en Python con `tkinter` y `ttkbootstrap`, prohibiendo tecnologías web o empaquetadores HTML.

---

### 💻 FASE 3: CONSTRUCCIÓN Y REFINAMIENTO DE LA GUI (`ttkbootstrap`)

#### 🔹 Interacción 3.1: Ensamblado de `src/ui/gui.py` y Regla de Oro en Callbacks

* **Prompt Real del Desarrollador (Prompt Maestro):**
  > *"El proyecto SIGESTA es completamente funcional por consola... Vamos a la creación de una interfaz gráfica utilizando Tkinter y ttkbootstrap apoyándote visualmente en la maquetación... Regla crítica: CERO lógica en callbacks. Los callbacks solo extraen datos, llaman al core inmutable, guardan con repository y refrescan la vista."*

* **Sugerencia de la IA:**
  Estructuró la interfaz en `src/ui/gui.py` con una clase controladora principal `App` que almacena la referencia inmutable al `EstadoSistema`, dividiendo las pantallas en componentes `Frame`:
  * `AuthFrame`: Autenticación y registro de usuarios.
  * `DashboardFrame`: Tabla `Treeview`, contadores métricos y selector de estados.
  * `TaskFormFrame`: Formulario modal de creación con permisos por rol.
  * `AnalyticsFrame`: Visualización del reporte calculado con `reduce`.

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado:** La arquitectura de Frames y el protocolo estricto en los callbacks.
  * 🎯 **Por qué:** Garantiza la total separación entre la cáscara imperativa visual y el núcleo puro, evitando la penalización severa impuesta por la rúbrica al concentrar reglas de negocio dentro de los eventos de la GUI.

---

#### 🔹 Interacción 3.2: Corrección de 7 Fallos Operativos y Control Estricto de Roles

* **Supervisión Humana y Detección de Errores:**
  Durante las pruebas interactivas de la interfaz gráfica, detecté 7 fallos en la experiencia de usuario y en la seguridad de roles del sistema:
  1. *Identidad visual:* Aparecía el icono de pluma azul por defecto de Tkinter.
  2. *Sobrecarga visual:* Había un subtítulo redundante en el panel de Login.
  3. *Seguridad de roles:* El rol TRABAJADOR podía ver la pestaña de Analítica/Ranking.
  4. *Diseño responsive:* El botón de "Cambiar Estado" se cortaba en resoluciones bajas.
  5. *Modales:* El diálogo de cambio de estado se abría como una ventana diminuta en la esquina superior.
  6. *Confusión de dominio:* El botón "Mis Tareas" del Jefe mostraba las tareas de toda la empresa mezcladas.
  7. *Falta funcional:* El Jefe no tenía forma de auditar por separado las tareas asignadas al personal.

* **Solución Implementada en `src/core/filters.py`:**
  ```python
  def obtenerTareasDelPersonal(tareas: tuple[Tarea, ...], idJefe: int) -> tuple[Tarea, ...]:
      """
      Función pura: aísla las tareas asignadas a colaboradores,
      excluyendo las tareas personales creadas por el propio jefe.
      """
      return tuple(filter(lambda t: t.asignadoA != idJefe, tareas))
  ```

* **Ajustes en `src/ui/gui.py`:**
  ```python
  # Ocultamiento declarativo de pestañas según el rol activo
  if usuarioActivo.rol == "JEFE":
      self.crearBotonSidebar("Tareas del Personal", self.mostrarTareasPersonal)
      self.crearBotonSidebar("Estadísticas", self.mostrarAnalitica)
  ```

* **Criterio Técnico y Decisión:**
  * 🟢 **Aceptado e Implementado:** Creación de `obtenerTareasDelPersonal` con `filter`, ajuste de layout maximizado (`state('zoomed')`), inyección del icono `sigestaLogo.jpg` mediante `iconphoto`, e independización de vistas ("Mis Tareas" vs "Tareas del Personal").
  * 🎯 **Por qué:** Corrigió fallos reales de usabilidad y garantizó el control estricto de roles exigido por el negocio sin violar la pureza del núcleo.

---

## 📊 4. Matriz de Cumplimiento de la Rúbrica Asistida por IA

| Requisito de la Guía | Implementación en SIGESTA | Rol de la IA | Decisión y Control Humano |
| :--- | :--- | :--- | :--- |
| **Modelado Inmutable** *(Unidades 1 y 2)* | `@dataclass(frozen=True)` en `src/models/modelos.py` | Sugirió estructura inicial con tipos | Se corrigió colisión nativa con `types.py` y se ordenaron atributos por defecto. |
| **Closure Real** *(Unidad 2)* | `crearFiltroCredenciales` y `crearFiltroPorAsignado` en `filters.py` | Propuso fábrica con `typing.Callable` | Se rechazó `Callable` por verbosidad; se adoptó `camelCase` y retorno de la entidad. |
| **Funciones HOF** *(Unidad 2)* | `filter()` en búsquedas, `map()` en transformaciones, `reduce()` en analítica | Redactó borradores iniciales de funciones | Se verificó que `reduce` consuma la tupla inmutable con un diccionario acumulador inicial. |
| **Pattern Matching** *(Unidad 1)* | `match/case` en despachadores de opciones y eventos | Propuso esquemas `if/elif` imperativos | Se impuso `match/case` declarativo conforme a la Unidad 1. |
| **Cero Lógica en Callbacks** *(Restricción Crítica)* | Eventos pasivos en `src/ui/gui.py` | Ensambló los componentes de Tkinter | Se auditó que cada callback extraiga valores, llame al núcleo puro y persista con `storage`. |

---

## 💡 5. Balance Crítico y Conclusión

1. **La IA como copiloto, no como arquitecto:** La Inteligencia Artificial fue fundamental para acelerar tareas mecánicas (como la maquetación de los widgets de Tkinter y la formulación de pruebas), pero carece de visión arquitectónica global si no se le imponen restricciones strictly.
2. **El peligro de la mutación oculta:** La IA propuso inicialmente retornos desactualizados en la consola que destruían la persistencia del estado inmutable en memoria. Fue indispensable comprender el patrón *Copy-and-Update* para diagnosticar y corregir el error.
3. **Mantenibilidad mediante separación de responsabilidades:** Al mantener la lógica de negocio 100% aislada en `src/core/`, la transición de la consola (CLI) a la interfaz gráfica (`ttkbootstrap`) se realizó sin tocar ni una sola línea del núcleo puro, demostrando en la práctica las ventajas del patrón *Functional Core, Imperative Shell*.
