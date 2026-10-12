# 1. Redacción del Problema:

## 1.1. Contexto:

- En una pequeña empresa u oficina operativa, la coordinación diaria entre la administración (el jefe/líder de equipo) y los colaboradores (trabajadores) suele realizarse mediante canales dispersos (mensajes de texto, notas en papel o instrucciones verbales), lo que provoca falta de seguimiento y duplicidad de esfuerzos.

## 1.2. Problema puntual:

- El líder del equipo necesita asignar tareas directas a cada colaborador y supervisar su avance en tiempo real.
- El colaborador necesita gestionar no solo lo que le asigna su líder, sino también sus propias subtareas o compromisos operativos diarios para organizar su jornada de trabajo de forma integral.
- Al carecer de una herramienta centralizada y simple, se pierde visibilidad sobre la carga real de trabajo de cada persona (por ejemplo, saber que un colaborador tiene 3 tareas asignadas por el líder más 2 personales, totalizando 5 pendientes).

# 2. Idea de la Solución (SIGESTA)

## 2.1. Propuesta

- Desarrollar una aplicación de escritorio ligera basada en **`Python` (tkinter + ttkbootstrap)** que gestione el flujo de tareas bajo un modelo de datos inmutable y funciones puras.

## 2.2. Dinámica del sistema:

1. **`Roles y perfiles simples:`** La aplicación permite seleccionar el usuario activo (Jefe o Trabajadores específicos como Juan, María, etc.).
2. **`Origen de la tarea:`** Cada tarea cuenta con un tipo de origen:
3. **`Asignada por líder:`** Creada por el jefe para un trabajador específico.
4. **`Personal / Autogestionada:`** Creada directamente por el trabajador para su propio día.
5. **`Flujo de estados:`** Cada trabajador puede actualizar el estado de sus tareas entre:
    - NO_INICIADO
    - EN_PROCESO
    - HECHO
6. **`Visibilidad y métricas:`**
    - El trabajador ve su lista consolidada de la jornada (asignadas + propias).
    - El jefe puede alternar vistas, filtrar la carga global por trabajador mediante funciones de orden superior (filter) y ver estadísticas acumuladas usando reduce.


# Posible arquitectura Modular:

```txt
SIGESTA/
│
├── data/
│   └── estado_sistema.json         # Persistencia en JSON (efecto secundario)
│
├── docs/
│   ├── analisis-funcional.md       # Entregable obligatorio
│   ├── bitacora-ia.md              # Entregable obligatorio
│   └── enlace-video.txt            # Enlace de exposición
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/                     # CAPA DE DATOS / MODELADO (Unidad 1)
│   │   ├── __init__.py
│   │   └── types.py                # dataclass(frozen=True) o NamedTuple (Tarea, Usuario, Estado)
│   │
│   ├── core/                       # CAPA LÓGICA PURA (Unidades 1 y 2)
│   │   ├── __init__.py
│   │   ├── transformations.py      # map, filter, reduce, funciones de orden superior
│   │   ├── filters.py              # Closures reales para generar filtros dinámicos
│   │   └── dispatcher.py           # Pattern matching (match/case) para procesar acciones
│   │
│   ├── storage/                    # CAPA DE EFECTOS SECUNDARIOS / I/O
│   │   ├── __init__.py
│   │   └── repository.py           # Funciones impuras: carga y guardado del JSON
│   │
│   └── ui/                         # CAPA VISUAL (Separada por completo)
│       ├── __init__.py
│       ├── cli.py                  # Tu primera interfaz por consola para pruebas
│       └── gui.py                  # Interfaz con Tkinter + ttkbootstrap generada después
│
├── main.py                         # Punto de entrada / orquestador principal
├── requirements.txt
└── README.md
```