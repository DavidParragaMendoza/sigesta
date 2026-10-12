# Bitácora de Uso de Inteligencia Artificial (bitacora-ia.md)

**Proyecto:** SIGESTA Funcional  
**Autor:** Ronald David Párraga Mendoza  
**Asignatura:** Programación Funcional  

---

## 1. Filosofía de Uso de la IA en el Proyecto
La Inteligencia Artificial se utilizó estrictamente como un consultor técnico, generador de escenarios de prueba y acelerador de código repetitivo, manteniendo en todo momento el control de la arquitectura, el modelado de datos y el criterio funcional exigido por la rúbrica.

---

## 2. Registro de Interacciones y Criterio Crítico

### Interacción 1: Consulta Arquitectónica (Java vs. Paradigma Funcional)
* **Prompt/Consulta realizada:**  
  *Pregunté por qué organizar el proyecto como `src/core`, `models`, `storage` y no bajo una arquitectura tradicional de capas orientada a objetos (Entity, Repository, Service, Controller como en Spring/Java).*
* **Sugerencia recibida:**  
  La IA explicó la equivalencia conceptual y justificó que en programación funcional el patrón adecuado es *Functional Core, Imperative Shell* para aislar los efectos secundarios (I/O) de la lógica pura.
* **Decisión y Criterio Técnico:**  
  * **Aceptado:** La estructura desacoplada en tres paquetes (`core` para funciones puras, `models` para tipos inmutables, `storage` para I/O impuro).
  * **Motivo:** Evita mezclar consultas de disco o mutaciones dentro de las reglas del negocio, cumpliendo la regla crítica de diseño de la guía.

---

### Interacción 2: Modelado Inmutable y Conflicto con la Biblioteca Estándar
* **Prompt/Consulta realizada:**  
  *Modelé las entidades `Tarea`, `Usuario` y `EstadoSistema` con `@dataclass(frozen=True)` en `src/models/types.py`. Al ejecutar, Python arrojó `ImportError: cannot import name 'dataclass' from partially initialized module 'dataclasses'`.*
* **Diagnóstico de la IA:**  
  Explicó que llamar al archivo `types.py` colisionaba con el módulo estándar `types` de Python, provocando una importación circular.
* **Decisión y Criterio Técnico:**  
  * **Modificado:** Renombré el módulo a `src/models/modelos.py` y reorganicé la dataclass `Tarea` colocando el campo opcional `descripcion: Optional[str] = None` al final de la definición para evitar el error de argumentos con valores por defecto.

---

### Interacción 3: Implementación del Closure y Filtro de Autenticación
* **Prompt/Consulta realizada:**  
  *Solicité una estructura para autenticar credenciales en `src/core/filters.py` utilizando un closure y la función de orden superior `filter`.*
* **Sugerencia de la IA:**  
  Propuso una fábrica `crearFiltroCredenciales` usando `from typing import Callable` y anotaciones `Callable[[Usuario], bool]`.
* **Decisión y Criterio Técnico:**  
  * **Rechazado:** El uso de `Callable` por añadir complejidad y verbosidad innecesaria.
  * **Modificado:** Adapté la función a mi estándar de nomenclatura en `camelCase` (`crearFiltroCredenciales`, `autenticarUsuario`), simplificando el closure para capturar léxicamente el correo y la contraseña, y retornando la instancia de `Usuario` (o `None`) en lugar de solo un booleano para aprovechar los datos en la vista.

---

### Interacción 4: Generación de Batería de Pruebas y Validación con Agente de IA
* **Prompt/Consulta realizada:**  
  *Solicité una secuencia exhaustiva de entradas para probar todas las rutas del CLI (creación de cuentas, creación de tareas del jefe, asignación a terceros, tareas personales, filtrado, reporte con `reduce` y cambios de estado).*
* **Intervención y Corrección del Agente:**  
  Al ejecutar las pruebas con el agente, este detectó un fallo crítico en la propagación del estado inmutable:
  * **Problema:** En `src/ui/consola.py`, la función `procesarOpcion` ejecutaba `iniciarSesion(estado)` pero retornaba `estado` (el estado viejo anterior a la sesión), descartando de memoria las nuevas tareas creadas por el usuario.
  * **Corrección aplicada:** Se modificó la firma de `iniciarSesion(estado: EstadoSistema) -> EstadoSistema` y se encadenó el retorno (`return iniciarSesion(estado)`), asegurando que la nueva versión del estado producida por *Copy-and-Update* persista a lo largo de las siguientes iteraciones del bucle de consola.

---

## 3. Balance de Aprendizaje
El uso asistido permitió validar la separación estricta entre la cáscara impura y el núcleo funcional, evidenciando que en un entorno inmutable el estado no se "actualiza en el lugar", sino que debe fluir explícitamente a través del retorno de las funciones.