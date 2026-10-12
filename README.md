<div align="center">

# ✦ SIGESTA

### Sistema de Gestión y Seguimiento de Tareas

<p>
  <strong>Una aplicación de escritorio que convierte la programación funcional
  en una herramienta real para organizar, asignar y analizar tareas.</strong>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10 o superior">
  <img src="https://img.shields.io/badge/Tkinter-GUI-2E7D32?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/ttkbootstrap-Interfaz-6C5CE7?style=for-the-badge" alt="ttkbootstrap">
  <img src="https://img.shields.io/badge/Arquitectura-Functional%20Core-111212?style=for-the-badge" alt="Functional Core">
</p>

<p>
  <a href="#-qué-es-sigesta">Descubrir el proyecto</a>
  ·
  <a href="#-puesta-en-marcha">Ejecutarlo</a>
  ·
  <a href="#-documentación">Leer la documentación</a>
</p>

</div>

---

## 🧭 Qué es SIGESTA

SIGESTA es un gestor de tareas con interfaz gráfica para equipos pequeños y
entornos académicos u operativos. Centraliza el trabajo que normalmente se
reparte entre mensajes, notas y conversaciones: permite registrar usuarios,
autenticar roles, crear tareas personales o delegadas, actualizar estados y
consultar estadísticas de cumplimiento.

El proyecto nace como una **Actividad Integradora de Programación Funcional
(Unidades 1 y 2)**. Su objetivo no es solo funcionar, sino hacer visible cómo
los conceptos funcionales resuelven un problema cotidiano sin perder claridad
ni control sobre los efectos secundarios.

> **Idea central:** el núcleo de negocio transforma datos de forma pura e
> inmutable; la interfaz, la consola y el almacenamiento se encargan de
> interactuar con el mundo exterior.

## ✨ Lo que puedes hacer

| Capacidad | Descripción |
| --- | --- |
| 👤 **Usuarios y roles** | Registro y autenticación diferenciada para `JEFE` y `TRABAJADOR`. |
| 🗂️ **Gestión de tareas** | Crear tareas personales o asignarlas a un trabajador. |
| 🔄 **Estados controlados** | Avanzar tareas entre `NO_INICIADO`, `EN_PROCESO` y `HECHO`. |
| 📊 **Indicadores** | Consultar totales por estado y ranking de cumplimiento. |
| 🖥️ **Dos interfaces** | Experiencia gráfica con Tkinter o flujo alternativo por consola. |
| 💾 **Persistencia sencilla** | Estado guardado en `data/estado_sistema.json`. |

## 🧠 Programación funcional aplicada

SIGESTA convierte los requisitos de la guía en decisiones concretas:

- **Functional Core, Imperative Shell:** la lógica de negocio vive en
  `src/core/`; la GUI, la CLI y el repositorio concentran los efectos
  secundarios.
- **Modelado inmutable:** `Usuario`, `Tarea` y `EstadoSistema` son
  `@dataclass(frozen=True)` y usan tuplas para las colecciones.
- **Funciones de orden superior y closures:** los filtros configurables
  generan predicados reutilizables para autenticación y consulta de tareas.
- **`map`, `filter` y `reduce`:** transforman datos, seleccionan tareas y
  calculan estadísticas sin depender de acumuladores mutables.
- **Pattern matching:** `match/case` enruta las opciones de la consola y las
  operaciones disponibles según el rol.
- **Criterio técnico:** la documentación explica qué propuso la IA, qué se
  aceptó, qué se modificó y qué se rechazó.

## 🗺️ Arquitectura del proyecto

```text
SIGESTA/
├── main.py                         # Punto de entrada: GUI o CLI
├── requirements.txt                # Dependencias del proyecto
├── data/
│   └── estado_sistema.json         # Persistencia local del estado
├── docs/
│   ├── analisis-funcional.md       # Decisiones, conceptos y justificación
│   ├── bitacora-ia.md              # Uso crítico y trazabilidad de la IA
│   └── guia-estudiantes-...pdf     # Guía de la actividad integradora
└── src/
    ├── core/                       # Núcleo funcional y reglas del dominio
    ├── models/                     # Dataclasses inmutables
    ├── storage/                    # Lectura y escritura JSON
    └── ui/                         # GUI Tkinter y alternativa por consola
```

## 🚀 Puesta en marcha

### 1. Clonar y entrar al proyecto

```bash
git clone https://github.com/DavidParragaMendoza/sigesta.git
cd sigesta
```

### 2. Crear y activar un entorno virtual

En Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Ejecutar SIGESTA

La interfaz gráfica es el modo predeterminado:

```bash
python main.py
```

También puedes iniciar la versión de consola:

```bash
python main.py --cli
```

## 🎥 Video explicativo

> **Enlace pendiente:** reemplaza el texto siguiente por la URL final de
> YouTube cuando el video esté publicado.

🔗 **[Ver el video explicativo en YouTube](PEGAR_AQUI_EL_ENLACE_DE_YOUTUBE)**

El video debe mostrar dónde están la HOF, el `match/case`, el closure, la
inmutabilidad, las funciones puras, los efectos secundarios y las decisiones
tomadas frente a las sugerencias de IA.

## 📚 Documentación

La documentación está organizada para que puedas recorrer el proyecto desde la
comprensión funcional hasta la reflexión sobre el proceso:

| Documento | Qué encontrarás |
| --- | --- |
| 📘 [Análisis funcional](docs/analisis-funcional.md) | Problema, estructuras, arquitectura, Unidad 1, Unidad 2, pureza, efectos secundarios, inmutabilidad y aprendizajes. |
| 📓 [Bitácora de uso crítico de IA](docs/bitacora-ia.md) | Prompts, propuestas, decisiones aceptadas, modificaciones, rechazos y justificaciones técnicas. |
| 🧾 [Guía de la actividad integradora](docs/guia-estudiantes-actividad-integradora-u1-u2.pdf) | Requisitos académicos, entregables y criterios de evaluación de las Unidades 1 y 2. |

## 🧪 Revisión rápida de conceptos

| Concepto | Ubicación principal |
| --- | --- |
| `dataclass(frozen=True)` | [`src/models/modelos.py`](src/models/modelos.py) |
| HOFs y closures | [`src/core/filters.py`](src/core/filters.py) |
| `map`, `filter`, `reduce` | [`src/core/transformations.py`](src/core/transformations.py) |
| Transformaciones inmutables | [`src/core/dispatcher.py`](src/core/dispatcher.py) |
| `match/case` | [`src/ui/consola.py`](src/ui/consola.py) |
| GUI y efectos secundarios | [`src/ui/gui.py`](src/ui/gui.py) |
| Persistencia JSON | [`src/storage/repository.py`](src/storage/repository.py) |

## 👨‍💻 Autor

**Ronald David Párraga Mendoza**  
Programación Funcional · Universidad Estatal Península de Santa Elena (UPSE)

---

## 📫 Contacto

- 💼 **LinkedIn:** [David Parraga Mendoza](https://www.linkedin.com/in/davidparragamendoza/)
- 𝕏 **X:** [@DavidParragaMen](https://x.com/DavidParragaMen)

<div align="center">

✨ **Gracias por visitar este proyecto** ✨

</div>
