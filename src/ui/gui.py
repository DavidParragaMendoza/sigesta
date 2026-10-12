"""
Módulo de Interfaz Gráfica de Usuario (GUI) para SIGESTA Funcional.
Implementado con Tkinter y ttkbootstrap siguiendo la arquitectura
'Functional Core, Imperative Shell'.

Regla de oro de la rúbrica:
- Cero lógica de negocio en callbacks.
- Los eventos extraen los datos de los widgets, delegan en las funciones
  puras de 'src.core', persisten con 'guardarEstado' y actualizan la UI.
"""

from os import path
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import ttkbootstrap as tb
from PIL import Image, ImageTk

# En Windows, registrar AppID para que la barra de tareas use el icono de la app y no Python (pluma azul)
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("sigesta.app.desktop.v2")
    except Exception:
        pass

from src.models.modelos import EstadoSistema, Usuario, Tarea
from src.core.dispatcher import agregarUsuario, agregarTarea, cambiarEstadoTarea
from src.core.filters import autenticarUsuario, obtenerTareasPorUsuario, obtenerTareasDelPersonal
from src.core.transformations import calcularEstadisticasEstado, obtenerRankingCumplimiento
from src.storage.repository import cargarEstado, guardarEstado


# ============================================================================
# CONSTANTES DE DISEÑO Y PALETA DE COLORES (Notion / Linear Dark Minimal)
# ============================================================================
COLOR_FONDO_CANVAS = "#111212"
COLOR_FONDO_SIDEBAR = "#191919"
COLOR_FONDO_CARD = "#202222"
COLOR_FONDO_CARD_LOW = "#161717"
COLOR_FONDO_INPUT = "#141515"
COLOR_BORDE = "#2D3230"
COLOR_BORDE_ENFOCADO = "#4B6349"

COLOR_PRIMARIO_BASE = "#354333"
COLOR_PRIMARIO_HOVER = "#3E513C"
COLOR_ACENTO_MENTA = "#9FE3A7"

COLOR_TEXTO_PRINCIPAL = "#E3E6E4"
COLOR_TEXTO_SECUNDARIO = "#8F9691"
COLOR_TEXTO_ATENUADO = "#5B625D"

# Semáforo Pastel para Estados de Tareas
COLOR_ESTADO_NO_INICIADO_BG = "#3A2325"
COLOR_ESTADO_NO_INICIADO_FG = "#F29E99"

COLOR_ESTADO_EN_PROCESO_BG = "#36301D"
COLOR_ESTADO_EN_PROCESO_FG = "#F7D486"

COLOR_ESTADO_HECHO_BG = "#233427"
COLOR_ESTADO_HECHO_FG = "#9FE3A7"

# Badges de Prioridad
COLOR_PRIORIDAD_ALTA = "#E06C75"
COLOR_PRIORIDAD_MEDIA = "#E5C07B"
COLOR_PRIORIDAD_BAJA = "#7AA2F7"


def obtenerRutaLogo() -> Optional[str]:
    """Retorna la ruta al logo si existe en alguna de las ubicaciones esperadas."""
    rutasPosibles = [
        path.join("src", "ui", "sigestaLogo.png"),
        path.join("src", "ui", "sigestaLogo.jpg"),
        path.join("src", "ui", "sigestaLogo.ico"),
        "sigestaLogo.png",
        "sigestaLogo.jpg",
    ]
    for ruta in rutasPosibles:
        if path.exists(ruta):
            return ruta
    return None


def obtenerRutaIcono() -> Optional[str]:
    """Retorna la ruta al archivo .ico si existe para la barra de título de Windows."""
    rutas = [
        path.join("src", "ui", "sigestaLogo.ico"),
        "sigestaLogo.ico"
    ]
    for r in rutas:
        if path.exists(r):
            return r
    return None


def cargarImagenLogo(dimensiones: tuple[int, int]) -> Optional[ImageTk.PhotoImage]:
    """Carga y redimensiona el logo corporativo conservando proporciones."""
    ruta = obtenerRutaLogo()
    if not ruta:
        return None
    try:
        imagen = Image.open(ruta)
        imagenRedimensionada = imagen.resize(dimensiones, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagenRedimensionada)
    except Exception:
        return None


# ============================================================================
# COMPONENTE: MODAL CAMBIO DE ESTADO (PANTALLA COMPLETA Y CENTRADA)
# ============================================================================
class DialogoCambioEstado(tb.Toplevel):
    """
    Ventana modal que se ejecuta en pantalla completa (maximizada) con una tarjeta
    central amplia, para garantizar accesibilidad total a botones y controles.
    """

    def __init__(self, parent: tk.Widget, tarea: Tarea, alConfirmar: Callable[[str], None], iconoVentana=None):
        super().__init__(parent)
        self.title("SIGESTA - Cambiar Estado de Tarea")
        self.alConfirmar = alConfirmar

        # Aplicar icono personalizado a la ventana modal
        if iconoVentana:
            try:
                self.iconphoto(False, iconoVentana)
            except Exception:
                pass
        rutaIco = obtenerRutaIcono()
        if rutaIco and sys.platform == "win32":
            try:
                self.iconbitmap(rutaIco)
            except Exception:
                pass

        # Ejecutar en pantalla completa / maximizada
        try:
            self.state("zoomed")
        except Exception:
            self.geometry("900x650")

        self.transient(parent)
        self.grab_set()
        self.configure(bg=COLOR_FONDO_CANVAS)

        # Contenedor centrado para la tarjeta
        contenedorBackdrop = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        contenedorBackdrop.pack(fill=tk.BOTH, expand=True)

        tarjetaExterior = tk.Frame(contenedorBackdrop, bg=COLOR_BORDE, padx=1, pady=1)
        tarjetaExterior.place(relx=0.5, rely=0.5, anchor="center")

        contenedor = tk.Frame(tarjetaExterior, bg=COLOR_FONDO_CARD, padx=36, pady=32, width=540)
        contenedor.pack()

        # Cabecera técnica
        lblTag = tk.Label(
            contenedor,
            text=f"SIGESTA // ACTUALIZACIÓN DE ESTADO // TAREA #SG-{tarea.id:02d}",
            font=("JetBrains Mono", 9, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_ACENTO_MENTA
        )
        lblTag.pack(anchor="w")

        lblTitulo = tk.Label(
            contenedor,
            text=tarea.titulo,
            font=("Inter", 14, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_PRINCIPAL,
            wraplength=480,
            justify="left"
        )
        lblTitulo.pack(anchor="w", pady=(8, 14))

        lblInfo = tk.Label(
            contenedor,
            text=f"Estado actual: {tarea.estado.replace('_', ' ')}  |  Prioridad: {tarea.prioridad}",
            font=("Inter", 10),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblInfo.pack(anchor="w", pady=(0, 20))

        # Divisor
        divisor = tk.Frame(contenedor, bg=COLOR_BORDE, height=1)
        divisor.pack(fill=tk.X, pady=(0, 20))

        lblSeleccionar = tk.Label(
            contenedor,
            text="SELECCIONAR NUEVO ESTADO DE EJECUCIÓN",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_ATENUADO
        )
        lblSeleccionar.pack(anchor="w", pady=(0, 10))

        self.varEstado = tk.StringVar(value=tarea.estado)
        opcionesFrame = tk.Frame(contenedor, bg=COLOR_FONDO_CARD)
        opcionesFrame.pack(fill=tk.X, pady=(0, 24))

        estados = [
            ("Sin Comenzar (NO_INICIADO)", "NO_INICIADO", COLOR_ESTADO_NO_INICIADO_FG, "⏳ Tarea en cola de espera"),
            ("En Proceso (EN_PROCESO)", "EN_PROCESO", COLOR_ESTADO_EN_PROCESO_FG, "⚙ Trabajo actualmente en ejecución"),
            ("Completada (HECHO)", "HECHO", COLOR_ESTADO_HECHO_FG, "✓ Tarea finalizada satisfactoriamente")
        ]

        for etiqueta, valor, colorFg, descripcion in estados:
            filaOpcion = tk.Frame(opcionesFrame, bg=COLOR_FONDO_CARD_LOW, padx=14, pady=10, highlightthickness=1, highlightbackground=COLOR_BORDE)
            filaOpcion.pack(fill=tk.X, pady=4)

            rb = tk.Radiobutton(
                filaOpcion,
                text=etiqueta,
                value=valor,
                variable=self.varEstado,
                bg=COLOR_FONDO_CARD_LOW,
                fg=colorFg,
                selectcolor=COLOR_FONDO_SIDEBAR,
                activebackground=COLOR_FONDO_CARD_LOW,
                activeforeground=colorFg,
                font=("Inter", 10, "bold")
            )
            rb.pack(anchor="w")

            lblDesc = tk.Label(
                filaOpcion,
                text=descripcion,
                font=("Inter", 8),
                bg=COLOR_FONDO_CARD_LOW,
                fg=COLOR_TEXTO_ATENUADO
            )
            lblDesc.pack(anchor="w", padx=(24, 0))

        # Botones de Acción
        botonesFrame = tk.Frame(contenedor, bg=COLOR_FONDO_CARD)
        botonesFrame.pack(fill=tk.X, pady=(12, 0))

        btnCancelar = tk.Button(
            botonesFrame,
            text="Cancelar",
            font=("Inter", 10),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO,
            activebackground=COLOR_BORDE,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.destroy
        )
        btnCancelar.pack(side=tk.RIGHT, padx=(12, 0))

        btnGuardar = tk.Button(
            botonesFrame,
            text="Confirmar Cambio de Estado",
            font=("Inter", 10, "bold"),
            bg=COLOR_PRIMARIO_BASE,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_HOVER,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=24,
            pady=10,
            cursor="hand2",
            command=self.confirmarAccion
        )
        btnGuardar.pack(side=tk.RIGHT)

    def confirmarAccion(self):
        nuevoEstado = self.varEstado.get()
        self.alConfirmar(nuevoEstado)
        self.destroy()


# ============================================================================
# VISTA 1: AUTENTICACIÓN (LOGIN Y REGISTRO)
# ============================================================================
class AuthFrame(tk.Frame):
    """
    Tarjeta central minimalista inspirada en Notion/Linear para login y registro.
    Extrae los datos de widgets y delega en 'autenticarUsuario' o 'agregarUsuario'.
    """

    def __init__(self, parent: tk.Widget, appController):
        super().__init__(parent, bg=COLOR_FONDO_CANVAS)
        self.appController = appController
        self.modoRegistro = False
        self.imagenLogo = None

        self.construirInterfaz()

    def construirInterfaz(self):
        contenedorCentral = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        contenedorCentral.place(relx=0.5, rely=0.5, anchor="center")

        tarjetaExterior = tk.Frame(contenedorCentral, bg=COLOR_BORDE, padx=1, pady=1)
        tarjetaExterior.pack()

        self.tarjeta = tk.Frame(tarjetaExterior, bg=COLOR_FONDO_SIDEBAR, padx=38, pady=34)
        self.tarjeta.pack()

        # Cabecera: Logo corporativo y Título
        cabeceraFrame = tk.Frame(self.tarjeta, bg=COLOR_FONDO_SIDEBAR)
        cabeceraFrame.pack(fill=tk.X, pady=(0, 20))

        self.imagenLogo = cargarImagenLogo((64, 64))
        if self.imagenLogo:
            lblLogo = tk.Label(cabeceraFrame, image=self.imagenLogo, bg=COLOR_FONDO_SIDEBAR)
            lblLogo.pack(pady=(0, 10))
        else:
            monograma = tk.Label(
                cabeceraFrame,
                text="SG",
                font=("JetBrains Mono", 20, "bold"),
                bg=COLOR_FONDO_CARD,
                fg=COLOR_ACENTO_MENTA,
                padx=16,
                pady=10
            )
            monograma.pack(pady=(0, 10))

        lblTitulo = tk.Label(
            cabeceraFrame,
            text="SIGESTA",
            font=("Inter", 20, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblTitulo.pack()

        # Pestañas: Iniciar Sesión / Crear Cuenta
        selectorFrame = tk.Frame(self.tarjeta, bg=COLOR_FONDO_INPUT, padx=3, pady=3)
        selectorFrame.pack(fill=tk.X, pady=(16, 20))

        self.btnTabLogin = tk.Button(
            selectorFrame,
            text="Iniciar Sesión",
            font=("Inter", 9, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            command=self.activarModoLogin
        )
        self.btnTabLogin.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btnTabRegistro = tk.Button(
            selectorFrame,
            text="Crear Cuenta",
            font=("Inter", 9),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_SECUNDARIO,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            command=self.activarModoRegistro
        )
        self.btnTabRegistro.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Contenedor de formulario dinámico
        self.formularioFrame = tk.Frame(self.tarjeta, bg=COLOR_FONDO_SIDEBAR)
        self.formularioFrame.pack(fill=tk.X)

        self.lblMensaje = tk.Label(
            self.tarjeta,
            text="",
            font=("Inter", 9),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_ESTADO_NO_INICIADO_FG
        )
        self.lblMensaje.pack(pady=(12, 0))

        self.renderizarCamposLogin()

    def activarModoLogin(self):
        self.modoRegistro = False
        self.btnTabLogin.configure(bg=COLOR_FONDO_CARD, fg=COLOR_TEXTO_PRINCIPAL, font=("Inter", 9, "bold"))
        self.btnTabRegistro.configure(bg=COLOR_FONDO_INPUT, fg=COLOR_TEXTO_SECUNDARIO, font=("Inter", 9))
        self.lblMensaje.configure(text="")
        self.renderizarCamposLogin()

    def activarModoRegistro(self):
        self.modoRegistro = True
        self.btnTabLogin.configure(bg=COLOR_FONDO_INPUT, fg=COLOR_TEXTO_SECUNDARIO, font=("Inter", 9))
        self.btnTabRegistro.configure(bg=COLOR_FONDO_CARD, fg=COLOR_TEXTO_PRINCIPAL, font=("Inter", 9, "bold"))
        self.lblMensaje.configure(text="")
        self.renderizarCamposRegistro()

    def limpiarFormulario(self):
        for widget in self.formularioFrame.winfo_children():
            widget.destroy()

    def renderizarCamposLogin(self):
        self.limpiarFormulario()

        lblCorreo = tk.Label(
            self.formularioFrame,
            text="CORREO ELECTRÓNICO",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblCorreo.pack(anchor="w", pady=(0, 4))

        self.entryCorreo = tk.Entry(
            self.formularioFrame,
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryCorreo.pack(fill=tk.X, ipady=6, pady=(0, 14))

        lblPassword = tk.Label(
            self.formularioFrame,
            text="CONTRASEÑA",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblPassword.pack(anchor="w", pady=(0, 4))

        self.entryPassword = tk.Entry(
            self.formularioFrame,
            show="•",
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryPassword.pack(fill=tk.X, ipady=6, pady=(0, 20))
        self.entryPassword.bind("<Return>", lambda _: self.callbackIniciarSesion())

        btnAcceso = tk.Button(
            self.formularioFrame,
            text="Acceder al Sistema",
            font=("Inter", 10, "bold"),
            bg=COLOR_PRIMARIO_BASE,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_HOVER,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            pady=9,
            cursor="hand2",
            command=self.callbackIniciarSesion
        )
        btnAcceso.pack(fill=tk.X)

    def renderizarCamposRegistro(self):
        self.limpiarFormulario()

        lblNombre = tk.Label(
            self.formularioFrame,
            text="NOMBRE COMPLETO",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblNombre.pack(anchor="w", pady=(0, 4))

        self.entryNombre = tk.Entry(
            self.formularioFrame,
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryNombre.pack(fill=tk.X, ipady=6, pady=(0, 10))

        lblCorreo = tk.Label(
            self.formularioFrame,
            text="CORREO ELECTRÓNICO",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblCorreo.pack(anchor="w", pady=(0, 4))

        self.entryCorreoReg = tk.Entry(
            self.formularioFrame,
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryCorreoReg.pack(fill=tk.X, ipady=6, pady=(0, 10))

        lblPassword = tk.Label(
            self.formularioFrame,
            text="CONTRASEÑA",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblPassword.pack(anchor="w", pady=(0, 4))

        self.entryPasswordReg = tk.Entry(
            self.formularioFrame,
            show="•",
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryPasswordReg.pack(fill=tk.X, ipady=6, pady=(0, 10))

        lblRol = tk.Label(
            self.formularioFrame,
            text="ROL ASIGNADO",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblRol.pack(anchor="w", pady=(0, 4))

        self.comboRol = ttk.Combobox(
            self.formularioFrame,
            values=["TRABAJADOR", "JEFE"],
            state="readonly",
            font=("Inter", 9)
        )
        self.comboRol.set("TRABAJADOR")
        self.comboRol.pack(fill=tk.X, ipady=4, pady=(0, 16))

        btnRegistrar = tk.Button(
            self.formularioFrame,
            text="Crear Usuario",
            font=("Inter", 10, "bold"),
            bg=COLOR_PRIMARIO_BASE,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_HOVER,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            pady=9,
            cursor="hand2",
            command=self.callbackRegistrarCuenta
        )
        btnRegistrar.pack(fill=tk.X)

    # ------------------------------------------------------------------------
    # CALLBACKS: RÚBRICA CERO LÓGICA DE NEGOCIO
    # ------------------------------------------------------------------------
    def callbackIniciarSesion(self):
        correo = self.entryCorreo.get().strip()
        password = self.entryPassword.get().strip()

        if not correo or not password:
            self.lblMensaje.configure(
                text="Por favor ingrese su correo y contraseña",
                fg=COLOR_ESTADO_NO_INICIADO_FG
            )
            return

        estadoActual = self.appController.obtenerEstado()
        usuarioAutenticado = autenticarUsuario(estadoActual.usuarios, correo, password)

        if usuarioAutenticado:
            self.lblMensaje.configure(text="")
            self.appController.iniciarSesion(usuarioAutenticado)
        else:
            self.lblMensaje.configure(
                text="Credenciales no válidas",
                fg=COLOR_ESTADO_NO_INICIADO_FG
            )

    def callbackRegistrarCuenta(self):
        nombre = self.entryNombre.get().strip()
        correo = self.entryCorreoReg.get().strip()
        password = self.entryPasswordReg.get().strip()
        rol = self.comboRol.get().strip().upper()

        if not nombre or not correo or not password or not rol:
            self.lblMensaje.configure(
                text="Todos los campos son requeridos",
                fg=COLOR_ESTADO_NO_INICIADO_FG
            )
            return

        estadoActual = self.appController.obtenerEstado()
        coincidentes = tuple(filter(lambda u: u.correo.lower() == correo.lower(), estadoActual.usuarios))
        if len(coincidentes) > 0:
            self.lblMensaje.configure(
                text="El correo ya se encuentra registrado",
                fg=COLOR_ESTADO_NO_INICIADO_FG
            )
            return

        nuevoEstado = agregarUsuario(estadoActual, nombre, correo, password, rol)
        self.appController.actualizarEstado(nuevoEstado)

        usuarioNuevo = autenticarUsuario(nuevoEstado.usuarios, correo, password)
        if usuarioNuevo:
            self.appController.iniciarSesion(usuarioNuevo)


# ============================================================================
# COMPONENTE: BARRA LATERAL (SIDEBAR)
# ============================================================================
class SidebarFrame(tk.Frame):
    """
    Barra de navegación lateral persistente (250px) estilo Notion.
    Condiciona las pestañas estrictamente según el rol (JEFE vs TRABAJADOR).
    """

    def __init__(self, parent: tk.Widget, appController, vistaActiva: str = "mis_tareas"):
        super().__init__(parent, bg=COLOR_FONDO_SIDEBAR, width=250)
        self.pack_propagate(False)
        self.appController = appController
        self.vistaActiva = vistaActiva
        self.imagenLogo = None

        self.construirSidebar()

    def construirSidebar(self):
        # 1. Cabecera con Logo Corporativo
        cabeceraFrame = tk.Frame(self, bg=COLOR_FONDO_SIDEBAR, padx=16, pady=18)
        cabeceraFrame.pack(fill=tk.X)

        self.imagenLogo = cargarImagenLogo((32, 32))
        filaMarca = tk.Frame(cabeceraFrame, bg=COLOR_FONDO_SIDEBAR)
        filaMarca.pack(fill=tk.X)

        if self.imagenLogo:
            lblLogo = tk.Label(filaMarca, image=self.imagenLogo, bg=COLOR_FONDO_SIDEBAR)
            lblLogo.pack(side=tk.LEFT, padx=(0, 8))
        else:
            lblIsotipo = tk.Label(
                filaMarca,
                text="SG",
                font=("JetBrains Mono", 11, "bold"),
                bg=COLOR_FONDO_CARD,
                fg=COLOR_ACENTO_MENTA,
                padx=6,
                pady=2
            )
            lblIsotipo.pack(side=tk.LEFT, padx=(0, 8))

        lblTitulo = tk.Label(
            filaMarca,
            text="SIGESTA",
            font=("Inter", 12, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblTitulo.pack(side=tk.LEFT)

        lblVersion = tk.Label(
            filaMarca,
            text="v2.4",
            font=("JetBrains Mono", 8),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO,
            padx=4,
            pady=1
        )
        lblVersion.pack(side=tk.RIGHT)

        # Divisor
        divisor1 = tk.Frame(self, bg=COLOR_BORDE, height=1)
        divisor1.pack(fill=tk.X, padx=12, pady=(8, 12))

        # 2. Navegación por Espacio de Trabajo
        navLabel = tk.Label(
            self,
            text="ESPACIO DE TRABAJO",
            font=("JetBrains Mono", 7, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_ATENUADO,
            padx=16
        )
        navLabel.pack(anchor="w", pady=(0, 6))

        # Pestaña "Mis Tareas" (Disponible para todos: JEFE y TRABAJADOR)
        self.crearBotonNavegacion("Mis Tareas", "mis_tareas", "☑")

        # Rol actual
        esJefe = self.appController.esJefe()

        # Pestaña "Tareas del Personal" (Exclusiva de JEFE)
        if esJefe:
            self.crearBotonNavegacion("Tareas del Personal", "tareas_personal", "👥")

        # Pestaña "Nueva Tarea"
        self.crearBotonNavegacion("Nueva Tarea", "nueva_tarea", "➕")

        # Pestaña "Estadísticas y Ranking" (Exclusiva de JEFE)
        if esJefe:
            self.crearBotonNavegacion("Estadísticas y Ranking", "ranking", "📊", badge="Jefe")

        # 3. Pie de sidebar: Perfil y Logout
        pieFrame = tk.Frame(self, bg=COLOR_FONDO_SIDEBAR)
        pieFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=12, pady=16)

        divisor2 = tk.Frame(pieFrame, bg=COLOR_BORDE, height=1)
        divisor2.pack(fill=tk.X, pady=(0, 12))

        usuario = self.appController.obtenerUsuarioActual()
        tarjetaPerfil = tk.Frame(pieFrame, bg=COLOR_FONDO_CARD, padx=10, pady=8)
        tarjetaPerfil.pack(fill=tk.X, pady=(0, 8))

        nombreUsuario = usuario.nombre if usuario else "Invitado"
        partes = nombreUsuario.strip().split()
        iniciales = "".join(p[0].upper() for p in partes[:2]) if partes else "U"

        avatarLbl = tk.Label(
            tarjetaPerfil,
            text=iniciales,
            font=("JetBrains Mono", 9, "bold"),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_ACENTO_MENTA,
            padx=6,
            pady=4
        )
        avatarLbl.pack(side=tk.LEFT, padx=(0, 8))

        datosFrame = tk.Frame(tarjetaPerfil, bg=COLOR_FONDO_CARD)
        datosFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lblNombre = tk.Label(
            datosFrame,
            text=nombreUsuario,
            font=("Inter", 9, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_PRINCIPAL,
            anchor="w"
        )
        lblNombre.pack(fill=tk.X)

        rolUsuario = usuario.rol if usuario else "ANÓNIMO"
        colorRolFg = COLOR_ACENTO_MENTA if rolUsuario == "JEFE" else COLOR_TEXTO_SECUNDARIO
        colorRolBg = COLOR_ESTADO_HECHO_BG if rolUsuario == "JEFE" else COLOR_FONDO_SIDEBAR

        lblRol = tk.Label(
            datosFrame,
            text=rolUsuario,
            font=("JetBrains Mono", 7, "bold"),
            bg=colorRolBg,
            fg=colorRolFg,
            padx=4,
            pady=1
        )
        lblRol.pack(anchor="w", pady=(2, 0))

        btnLogout = tk.Button(
            pieFrame,
            text="⎋  Cerrar Sesión",
            font=("Inter", 9),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO,
            activebackground=COLOR_ESTADO_NO_INICIADO_BG,
            activeforeground=COLOR_ESTADO_NO_INICIADO_FG,
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=6,
            anchor="w",
            cursor="hand2",
            command=self.appController.cerrarSesion
        )
        btnLogout.pack(fill=tk.X)

    def crearBotonNavegacion(self, texto: str, destino: str, icono: str, badge: str = ""):
        esActivo = (self.vistaActiva == destino)
        bg = COLOR_FONDO_CARD if esActivo else COLOR_FONDO_SIDEBAR
        fg = COLOR_TEXTO_PRINCIPAL if esActivo else COLOR_TEXTO_SECUNDARIO

        btnFrame = tk.Frame(self, bg=bg, cursor="hand2")
        btnFrame.pack(fill=tk.X, padx=8, pady=2)

        lblIcono = tk.Label(btnFrame, text=icono, font=("Inter", 9), bg=bg, fg=COLOR_ACENTO_MENTA if esActivo else fg)
        lblIcono.pack(side=tk.LEFT, padx=(8, 6), pady=7)

        lblTexto = tk.Label(btnFrame, text=texto, font=("Inter", 9, "bold" if esActivo else "normal"), bg=bg, fg=fg)
        lblTexto.pack(side=tk.LEFT, pady=7)

        if badge:
            badgeLbl = tk.Label(
                btnFrame,
                text=badge,
                font=("JetBrains Mono", 7, "bold"),
                bg=COLOR_ESTADO_HECHO_BG,
                fg=COLOR_ACENTO_MENTA,
                padx=4,
                pady=1
            )
            badgeLbl.pack(side=tk.RIGHT, padx=(0, 8))

        def alHacerClick(_=None):
            self.appController.mostrarVista(destino)

        btnFrame.bind("<Button-1>", alHacerClick)
        lblIcono.bind("<Button-1>", alHacerClick)
        lblTexto.bind("<Button-1>", alHacerClick)


# ============================================================================
# VISTA 2: TABLERO DE TAREAS (MIS TAREAS / TAREAS DEL PERSONAL)
# ============================================================================
class DashboardFrame(tk.Frame):
    """
    Panel de tareas con métricas calculadas con reduce, tabla interactiva Treeview,
    buscador, filtros y botón prominente de 'Cambiar Estado' ubicado en la barra superior.
    Soporta modo 'mis_tareas' (solo tareas asignadas al usuario activo) y
    modo 'personal' (solo tareas de trabajadores).
    """

    def __init__(self, parent: tk.Widget, appController, modo: str = "mis_tareas"):
        super().__init__(parent, bg=COLOR_FONDO_CANVAS)
        self.appController = appController
        self.modo = modo  # "mis_tareas" o "personal"
        self.filtroTexto = tk.StringVar(value="")
        self.filtroEstado = tk.StringVar(value="TODAS")

        self.construirInterfaz()
        self.refrescarDatos()

    def construirInterfaz(self):
        # 1. Cabecera contextual
        cabeceraFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        cabeceraFrame.pack(fill=tk.X, padx=28, pady=(22, 14))

        if self.modo == "personal":
            subtitulo = "SIGESTA // SUPERVISIÓN DE EQUIPO // TAREAS DEL PERSONAL"
            titulo = "Tareas del Personal"
        else:
            subtitulo = "SIGESTA // MIS TAREAS ASIGNADAS // OPERACIÓN"
            titulo = "Mis Tareas"

        lblSub = tk.Label(
            cabeceraFrame,
            text=subtitulo,
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_ACENTO_MENTA
        )
        lblSub.pack(anchor="w")

        lblTitulo = tk.Label(
            cabeceraFrame,
            text=titulo,
            font=("Inter", 18, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblTitulo.pack(anchor="w", pady=(2, 0))

        # 2. Tarjetas Métricas Rápidas (reduce)
        self.metricasFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        self.metricasFrame.pack(fill=tk.X, padx=28, pady=(0, 16))

        self.cardSinComenzar = self.crearTarjetaMetrica(
            "Sin Comenzar", "0", COLOR_ESTADO_NO_INICIADO_FG, "⏳ En cola"
        )
        self.cardEnProceso = self.crearTarjetaMetrica(
            "En Proceso", "0", COLOR_ESTADO_EN_PROCESO_FG, "⚙ Sprint activo"
        )
        self.cardCompletadas = self.crearTarjetaMetrica(
            "Completadas", "0", COLOR_ESTADO_HECHO_FG, "✓ Cumplidas"
        )

        # 3. Barra de control superior con Buscador, Filtros y Acciones
        controlFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        controlFrame.pack(fill=tk.X, padx=28, pady=(0, 12))

        # Buscador reactivo
        buscadorContenedor = tk.Frame(controlFrame, bg=COLOR_FONDO_CARD, padx=8, pady=4)
        buscadorContenedor.pack(side=tk.LEFT)

        lblBuscarIcono = tk.Label(buscadorContenedor, text="🔍", font=("Inter", 9), bg=COLOR_FONDO_CARD, fg=COLOR_TEXTO_SECUNDARIO)
        lblBuscarIcono.pack(side=tk.LEFT, padx=(0, 6))

        self.entryBuscar = tk.Entry(
            buscadorContenedor,
            textvariable=self.filtroTexto,
            font=("Inter", 9),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            width=24
        )
        self.entryBuscar.pack(side=tk.LEFT)
        self.filtroTexto.trace_add("write", lambda *_: self.refrescarDatos())

        # Filtros rápidos por estado
        botonesFiltroFrame = tk.Frame(controlFrame, bg=COLOR_FONDO_CANVAS)
        botonesFiltroFrame.pack(side=tk.LEFT, padx=(12, 0))

        self.crearBotonFiltro(botonesFiltroFrame, "Todas", "TODAS")
        self.crearBotonFiltro(botonesFiltroFrame, "Sin Comenzar", "NO_INICIADO")
        self.crearBotonFiltro(botonesFiltroFrame, "En Proceso", "EN_PROCESO")
        self.crearBotonFiltro(botonesFiltroFrame, "Completadas", "HECHO")

        # Botón CAMBIAR ESTADO ubicado en la barra superior (Siempre visible sin importar el tamaño)
        btnCambiarEstadoTop = tk.Button(
            controlFrame,
            text="⚡  Cambiar Estado",
            font=("Inter", 9, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_BASE,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.callbackAbrirDialogoEstado
        )
        btnCambiarEstadoTop.pack(side=tk.RIGHT, padx=(8, 0))

        # Botón Nueva Tarea
        btnNuevaTarea = tk.Button(
            controlFrame,
            text="➕  Nueva Tarea",
            font=("Inter", 9, "bold"),
            bg=COLOR_PRIMARIO_BASE,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_HOVER,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self.appController.mostrarVista("nueva_tarea")
        )
        btnNuevaTarea.pack(side=tk.RIGHT)

        # 4. Tabla Treeview de Tareas
        tablaExterior = tk.Frame(self, bg=COLOR_BORDE, padx=1, pady=1)
        tablaExterior.pack(fill=tk.BOTH, expand=True, padx=28, pady=(0, 16))

        tablaFrame = tk.Frame(tablaExterior, bg=COLOR_FONDO_SIDEBAR)
        tablaFrame.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "titulo", "prioridad", "estado", "asignado")
        self.treeview = ttk.Treeview(
            tablaFrame,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=10
        )

        self.treeview.heading("id", text="CÓDIGO", anchor="w")
        self.treeview.heading("titulo", text="DESCRIPCIÓN DE LA TAREA", anchor="w")
        self.treeview.heading("prioridad", text="PRIORIDAD", anchor="center")
        self.treeview.heading("estado", text="ESTADO", anchor="center")
        self.treeview.heading("asignado", text="RESPONSABLE", anchor="w")

        self.treeview.column("id", width=80, minwidth=70, stretch=False)
        self.treeview.column("titulo", width=360, minwidth=220, stretch=True)
        self.treeview.column("prioridad", width=100, minwidth=90, stretch=False, anchor="center")
        self.treeview.column("estado", width=140, minwidth=120, stretch=False, anchor="center")
        self.treeview.column("asignado", width=180, minwidth=140, stretch=False)

        scrollbar = ttk.Scrollbar(tablaFrame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview.bind("<Double-1>", lambda _: self.callbackAbrirDialogoEstado())

        # Configurar colores de tags de estado
        self.treeview.tag_configure(
            "NO_INICIADO",
            background=COLOR_FONDO_SIDEBAR,
            foreground=COLOR_ESTADO_NO_INICIADO_FG
        )
        self.treeview.tag_configure(
            "EN_PROCESO",
            background=COLOR_FONDO_SIDEBAR,
            foreground=COLOR_ESTADO_EN_PROCESO_FG
        )
        self.treeview.tag_configure(
            "HECHO",
            background=COLOR_FONDO_SIDEBAR,
            foreground=COLOR_ESTADO_HECHO_FG
        )

    def crearTarjetaMetrica(self, titulo: str, valorInicial: str, colorAcento: str, pie: str) -> dict:
        tarjetaExterior = tk.Frame(self.metricasFrame, bg=COLOR_BORDE, padx=1, pady=1)
        tarjetaExterior.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        tarjeta = tk.Frame(tarjetaExterior, bg=COLOR_FONDO_CARD, padx=16, pady=12)
        tarjeta.pack(fill=tk.BOTH, expand=True)

        cabecera = tk.Frame(tarjeta, bg=COLOR_FONDO_CARD)
        cabecera.pack(fill=tk.X)

        punto = tk.Label(cabecera, text="●", font=("Inter", 7), bg=COLOR_FONDO_CARD, fg=colorAcento)
        punto.pack(side=tk.LEFT, padx=(0, 6))

        lblTitulo = tk.Label(
            cabecera,
            text=titulo.upper(),
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblTitulo.pack(side=tk.LEFT)

        lblValor = tk.Label(
            tarjeta,
            text=valorInicial,
            font=("Inter", 20, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblValor.pack(anchor="w", pady=(4, 2))

        lblPie = tk.Label(
            tarjeta,
            text=pie,
            font=("Inter", 8),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_ATENUADO
        )
        lblPie.pack(anchor="w")

        return {"valor": lblValor}

    def crearBotonFiltro(self, parent: tk.Widget, texto: str, valor: str):
        btn = tk.Button(
            parent,
            text=texto,
            font=("Inter", 8),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO,
            activebackground=COLOR_BORDE,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=4,
            cursor="hand2",
            command=lambda: self.establecerFiltroEstado(valor)
        )
        btn.pack(side=tk.LEFT, padx=2)

    def establecerFiltroEstado(self, estado: str):
        self.filtroEstado.set(estado)
        self.refrescarDatos()

    def obtenerNombreUsuario(self, idUsuario: int) -> str:
        estado = self.appController.obtenerEstado()
        coincidentes = tuple(filter(lambda u: u.id == idUsuario, estado.usuarios))
        return coincidentes[0].nombre if len(coincidentes) > 0 else f"ID #{idUsuario}"

    # ------------------------------------------------------------------------
    # ACTUALIZACIÓN Y SINCRONIZACIÓN DE UI CON FUNCIONES PURAS
    # ------------------------------------------------------------------------
    def refrescarDatos(self):
        estado = self.appController.obtenerEstado()
        usuarioActual = self.appController.obtenerUsuarioActual()

        # REGLA 6 & 7: Separar estrictamente tareas del jefe y tareas del personal
        if self.modo == "personal":
            # Tareas del personal (trabajadores)
            idJefeExcluido = usuarioActual.id if usuarioActual else None
            tareasBase = obtenerTareasDelPersonal(estado.tareas, estado.usuarios, idExcluido=idJefeExcluido)
        else:
            # Mis Tareas: Solo las asignadas al usuario activo (sea Jefe o Trabajador)
            idUsuarioActivo = usuarioActual.id if usuarioActual else 0
            tareasBase = obtenerTareasPorUsuario(estado.tareas, idUsuarioActivo)

        # 1. Métricas con la función pura 'calcularEstadisticasEstado' (reduce)
        stats = calcularEstadisticasEstado(tareasBase)
        self.cardSinComenzar["valor"].configure(text=f"{stats.get('NO_INICIADO', 0):02d}")
        self.cardEnProceso["valor"].configure(text=f"{stats.get('EN_PROCESO', 0):02d}")
        self.cardCompletadas["valor"].configure(text=f"{stats.get('HECHO', 0):02d}")

        # 2. Filtrado de tareas para la tabla (closures y filters puros)
        textoBusqueda = self.filtroTexto.get().strip().lower()
        filtroEst = self.filtroEstado.get()

        def criterioBusqueda(t: Tarea) -> bool:
            nombreAsignado = self.obtenerNombreUsuario(t.asignadoA).lower()
            cumpleTexto = (
                not textoBusqueda or
                textoBusqueda in t.titulo.lower() or
                textoBusqueda in f"sg-{t.id:02d}".lower() or
                textoBusqueda in nombreAsignado
            )
            cumpleEstado = (filtroEst == "TODAS" or t.estado == filtroEst)
            return cumpleTexto and cumpleEstado

        tareasFiltradas = tuple(filter(criterioBusqueda, tareasBase))

        # 3. Limpiar y repoblar Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for t in tareasFiltradas:
            nombreResp = self.obtenerNombreUsuario(t.asignadoA)
            estadoLegible = t.estado.replace("_", " ")
            self.treeview.insert(
                "",
                tk.END,
                values=(f"SG-{t.id:02d}", t.titulo, t.prioridad, estadoLegible, nombreResp),
                tags=(t.estado,)
            )

    # ------------------------------------------------------------------------
    # CALLBACK: CERO LÓGICA DE NEGOCIO
    # ------------------------------------------------------------------------
    def callbackAbrirDialogoEstado(self):
        seleccion = self.treeview.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Por favor selecciona una tarea en la tabla para cambiar su estado.")
            return

        valores = self.treeview.item(seleccion[0])["values"]
        codigo = str(valores[0]).replace("SG-", "").strip()
        idTarea = int(codigo)

        estado = self.appController.obtenerEstado()
        tareaEncontrada = next((t for t in estado.tareas if t.id == idTarea), None)
        if not tareaEncontrada:
            return

        def alConfirmarNuevoEstado(nuevoEstado: str):
            # 1. Extraer ID y llamar a la función pura
            nuevoEstadoSistema = cambiarEstadoTarea(
                self.appController.obtenerEstado(),
                idTarea,
                nuevoEstado
            )
            # 2. Persistir
            self.appController.actualizarEstado(nuevoEstadoSistema)
            # 3. Refrescar interfaz
            self.refrescarDatos()

        DialogoCambioEstado(
            self,
            tareaEncontrada,
            alConfirmarNuevoEstado,
            iconoVentana=self.appController.iconoVentana
        )


# ============================================================================
# VISTA 3: FORMULARIO DE CREACIÓN DE TAREAS
# ============================================================================
class TaskFormFrame(tk.Frame):
    """
    Formulario minimalista para registrar nuevas tareas.
    Extrae los datos y delega en 'agregarTarea' persistiendo inmutablemente.
    """

    def __init__(self, parent: tk.Widget, appController):
        super().__init__(parent, bg=COLOR_FONDO_CANVAS)
        self.appController = appController
        self.varPrioridad = tk.StringVar(value="MEDIA")
        self.mapaUsuariosCombo = {}

        self.construirInterfaz()

    def construirInterfaz(self):
        cabeceraFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        cabeceraFrame.pack(fill=tk.X, padx=28, pady=(24, 16))

        lblSub = tk.Label(
            cabeceraFrame,
            text="SIGESTA // TASK_DISPATCHER // REGISTRO",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_ACENTO_MENTA
        )
        lblSub.pack(anchor="w")

        lblTitulo = tk.Label(
            cabeceraFrame,
            text="Crear Nueva Tarea",
            font=("Inter", 18, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblTitulo.pack(anchor="w", pady=(2, 0))

        formularioExterior = tk.Frame(self, bg=COLOR_BORDE, padx=1, pady=1)
        formularioExterior.pack(fill=tk.BOTH, expand=True, padx=28, pady=(0, 24))

        formulario = tk.Frame(formularioExterior, bg=COLOR_FONDO_CARD, padx=28, pady=24)
        formulario.pack(fill=tk.BOTH, expand=True)

        # 1. Campo: Título
        lblTituloCampo = tk.Label(
            formulario,
            text="TÍTULO DE LA TAREA *",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblTituloCampo.pack(anchor="w", pady=(0, 4))

        self.entryTitulo = tk.Entry(
            formulario,
            font=("Inter", 10),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.entryTitulo.pack(fill=tk.X, ipady=6, pady=(0, 16))

        # 2. Selector de Prioridad (Segmentado)
        lblPrioCampo = tk.Label(
            formulario,
            text="PRIORIDAD DE EJECUCIÓN *",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblPrioCampo.pack(anchor="w", pady=(0, 6))

        prioFrame = tk.Frame(formulario, bg=COLOR_FONDO_CARD)
        prioFrame.pack(fill=tk.X, pady=(0, 16))

        prioridades = [
            ("BAJA", COLOR_PRIORIDAD_BAJA),
            ("MEDIA", COLOR_PRIORIDAD_MEDIA),
            ("ALTA", COLOR_PRIORIDAD_ALTA)
        ]

        for prio, color in prioridades:
            rb = tk.Radiobutton(
                prioFrame,
                text=prio,
                value=prio,
                variable=self.varPrioridad,
                font=("JetBrains Mono", 9, "bold"),
                bg=COLOR_FONDO_CARD,
                fg=color,
                selectcolor=COLOR_FONDO_SIDEBAR,
                activebackground=COLOR_FONDO_CARD,
                activeforeground=color
            )
            rb.pack(side=tk.LEFT, padx=(0, 18))

        # 3. Asignación (según Rol)
        lblAsignadoCampo = tk.Label(
            formulario,
            text="RESPONSABLE ASIGNADO *",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblAsignadoCampo.pack(anchor="w", pady=(0, 4))

        usuarioActual = self.appController.obtenerUsuarioActual()
        esJefe = self.appController.esJefe()

        if esJefe:
            estado = self.appController.obtenerEstado()
            opciones = []
            for u in estado.usuarios:
                etiqueta = f"{u.nombre} (ID: {u.id} - {u.rol})"
                opciones.append(etiqueta)
                self.mapaUsuariosCombo[etiqueta] = u.id

            self.comboAsignado = ttk.Combobox(
                formulario,
                values=opciones,
                state="readonly",
                font=("Inter", 9)
            )
            if opciones:
                self.comboAsignado.set(opciones[0])
            self.comboAsignado.pack(fill=tk.X, ipady=4, pady=(0, 16))
        else:
            self.entryAsignadoFijo = tk.Entry(
                formulario,
                font=("Inter", 9),
                bg=COLOR_FONDO_INPUT,
                fg=COLOR_TEXTO_SECUNDARIO,
                relief=tk.FLAT,
                bd=0,
                highlightthickness=1,
                highlightbackground=COLOR_BORDE
            )
            nombrePropio = usuarioActual.nombre if usuarioActual else "Propio"
            idPropio = usuarioActual.id if usuarioActual else 0
            self.entryAsignadoFijo.insert(0, f"{nombrePropio} (Asignación automática a ti mismo - ID: {idPropio})")
            self.entryAsignadoFijo.configure(state="readonly")
            self.entryAsignadoFijo.pack(fill=tk.X, ipady=6, pady=(0, 16))

        # 4. Descripción opcional
        lblDescCampo = tk.Label(
            formulario,
            text="DESCRIPCIÓN OPERATIVA (OPCIONAL)",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblDescCampo.pack(anchor="w", pady=(0, 4))

        self.textDescripcion = tk.Text(
            formulario,
            height=4,
            font=("Inter", 9),
            bg=COLOR_FONDO_INPUT,
            fg=COLOR_TEXTO_PRINCIPAL,
            insertbackground=COLOR_ACENTO_MENTA,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
            highlightcolor=COLOR_BORDE_ENFOCADO
        )
        self.textDescripcion.pack(fill=tk.X, pady=(0, 20))

        # 5. Barra de botones
        botonesFrame = tk.Frame(formulario, bg=COLOR_FONDO_CARD)
        botonesFrame.pack(fill=tk.X)

        btnCancelar = tk.Button(
            botonesFrame,
            text="Cancelar",
            font=("Inter", 9),
            bg=COLOR_FONDO_SIDEBAR,
            fg=COLOR_TEXTO_SECUNDARIO,
            activebackground=COLOR_BORDE,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=lambda: self.appController.mostrarVista("mis_tareas")
        )
        btnCancelar.pack(side=tk.RIGHT, padx=(10, 0))

        btnGuardar = tk.Button(
            botonesFrame,
            text="Guardar Tarea",
            font=("Inter", 9, "bold"),
            bg=COLOR_PRIMARIO_BASE,
            fg=COLOR_ACENTO_MENTA,
            activebackground=COLOR_PRIMARIO_HOVER,
            activeforeground=COLOR_TEXTO_PRINCIPAL,
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.callbackGuardarTarea
        )
        btnGuardar.pack(side=tk.RIGHT)

    # ------------------------------------------------------------------------
    # CALLBACK: CERO LÓGICA DE NEGOCIO
    # ------------------------------------------------------------------------
    def callbackGuardarTarea(self):
        titulo = self.entryTitulo.get().strip()
        if not titulo:
            messagebox.showwarning("Atención", "El título de la tarea es obligatorio.")
            return

        prioridad = self.varPrioridad.get()
        descripcionBruta = self.textDescripcion.get("1.0", tk.END).strip()
        descripcion = descripcionBruta if descripcionBruta else None

        if self.appController.esJefe():
            seleccion = self.comboAsignado.get()
            idAsignado = self.mapaUsuariosCombo.get(seleccion, 1)
        else:
            usuarioActual = self.appController.obtenerUsuarioActual()
            idAsignado = usuarioActual.id if usuarioActual else 1

        # 1. Función pura
        nuevoEstado = agregarTarea(
            self.appController.obtenerEstado(),
            titulo=titulo,
            prioridad=prioridad,
            asignadoA=idAsignado,
            descripcion=descripcion
        )

        # 2. Persistir
        self.appController.actualizarEstado(nuevoEstado)

        # 3. Transicionar según corresponda
        if self.appController.esJefe() and idAsignado != self.appController.obtenerUsuarioActual().id:
            self.appController.mostrarVista("tareas_personal")
        else:
            self.appController.mostrarVista("mis_tareas")


# ============================================================================
# VISTA 4: PANEL DE ESTADÍSTICAS Y RANKING DE EQUIPO (SOLO JEFE)
# ============================================================================
class AnalyticsFrame(tk.Frame):
    """
    Panel de analítica y auditoría operativa exclusivo para el JEFE.
    Consume exclusivamente 'calcularEstadisticasEstado' y 'obtenerRankingCumplimiento'.
    """

    def __init__(self, parent: tk.Widget, appController):
        super().__init__(parent, bg=COLOR_FONDO_CANVAS)
        self.appController = appController

        self.construirInterfaz()
        self.refrescarDatos()

    def construirInterfaz(self):
        cabeceraFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        cabeceraFrame.pack(fill=tk.X, padx=28, pady=(24, 16))

        lblSub = tk.Label(
            cabeceraFrame,
            text="SIGESTA // AUDITORÍA & ANALÍTICA // RENDIMIENTO // EXCLUSIVO JEFE",
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_ACENTO_MENTA
        )
        lblSub.pack(anchor="w")

        lblTitulo = tk.Label(
            cabeceraFrame,
            text="Estadísticas y Rendimiento del Equipo",
            font=("Inter", 18, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_TEXTO_PRINCIPAL
        )
        lblTitulo.pack(anchor="w", pady=(2, 0))

        lblDesc = tk.Label(
            cabeceraFrame,
            text="Métricas consolidadas de ejecución y tabla de cumplimiento por colaborador.",
            font=("Inter", 9),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblDesc.pack(anchor="w", pady=(2, 0))

        self.resumenFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        self.resumenFrame.pack(fill=tk.X, padx=28, pady=(0, 20))

        self.cardTotal = self.crearCardMetrica("Total Tareas", "0", COLOR_TEXTO_PRINCIPAL)
        self.cardHecho = self.crearCardMetrica("Completadas", "0", COLOR_ESTADO_HECHO_FG)
        self.cardEnProceso = self.crearCardMetrica("En Proceso", "0", COLOR_ESTADO_EN_PROCESO_FG)
        self.cardNoIniciado = self.crearCardMetrica("No Iniciadas", "0", COLOR_ESTADO_NO_INICIADO_FG)

        seccionFrame = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        seccionFrame.pack(fill=tk.BOTH, expand=True, padx=28, pady=(0, 24))

        lblLeaderboard = tk.Label(
            seccionFrame,
            text="RANKING DE CUMPLIMIENTO (TAREAS HECHAS)",
            font=("JetBrains Mono", 9, "bold"),
            bg=COLOR_FONDO_CANVAS,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblLeaderboard.pack(anchor="w", pady=(0, 8))

        tablaExterior = tk.Frame(seccionFrame, bg=COLOR_BORDE, padx=1, pady=1)
        tablaExterior.pack(fill=tk.BOTH, expand=True)

        tablaFrame = tk.Frame(tablaExterior, bg=COLOR_FONDO_SIDEBAR)
        tablaFrame.pack(fill=tk.BOTH, expand=True)

        columnas = ("posicion", "colaborador", "completadas", "tasa")
        self.treeviewRanking = ttk.Treeview(
            tablaFrame,
            columns=columnas,
            show="headings",
            height=10
        )

        self.treeviewRanking.heading("posicion", text="POSICIÓN", anchor="center")
        self.treeviewRanking.heading("colaborador", text="COLABORADOR", anchor="w")
        self.treeviewRanking.heading("completadas", text="TAREAS COMPLETADAS", anchor="center")
        self.treeviewRanking.heading("tasa", text="NIVEL DE CUMPLIMIENTO", anchor="center")

        self.treeviewRanking.column("posicion", width=90, minwidth=80, stretch=False, anchor="center")
        self.treeviewRanking.column("colaborador", width=340, minwidth=220, stretch=True)
        self.treeviewRanking.column("completadas", width=180, minwidth=140, stretch=False, anchor="center")
        self.treeviewRanking.column("tasa", width=200, minwidth=150, stretch=False, anchor="center")

        self.treeviewRanking.pack(fill=tk.BOTH, expand=True)

    def crearCardMetrica(self, titulo: str, valorInicial: str, color: str) -> dict:
        tarjetaExterior = tk.Frame(self.resumenFrame, bg=COLOR_BORDE, padx=1, pady=1)
        tarjetaExterior.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        tarjeta = tk.Frame(tarjetaExterior, bg=COLOR_FONDO_CARD, padx=16, pady=12)
        tarjeta.pack(fill=tk.BOTH, expand=True)

        lblTit = tk.Label(
            tarjeta,
            text=titulo.upper(),
            font=("JetBrains Mono", 8, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=COLOR_TEXTO_SECUNDARIO
        )
        lblTit.pack(anchor="w")

        lblVal = tk.Label(
            tarjeta,
            text=valorInicial,
            font=("Inter", 20, "bold"),
            bg=COLOR_FONDO_CARD,
            fg=color
        )
        lblVal.pack(anchor="w", pady=(4, 0))

        return {"valor": lblVal}

    def refrescarDatos(self):
        estado = self.appController.obtenerEstado()

        stats = calcularEstadisticasEstado(estado.tareas)
        total = len(estado.tareas)
        hecho = stats.get("HECHO", 0)
        enProceso = stats.get("EN_PROCESO", 0)
        noIniciado = stats.get("NO_INICIADO", 0)

        self.cardTotal["valor"].configure(text=f"{total:02d}")
        self.cardHecho["valor"].configure(text=f"{hecho:02d}")
        self.cardEnProceso["valor"].configure(text=f"{enProceso:02d}")
        self.cardNoIniciado["valor"].configure(text=f"{noIniciado:02d}")

        ranking = obtenerRankingCumplimiento(estado.usuarios, estado.tareas)

        for item in self.treeviewRanking.get_children():
            self.treeviewRanking.delete(item)

        for idx, (nombre, completadas) in enumerate(ranking, start=1):
            medalla = f"#{idx:02d}"
            if idx == 1:
                medalla = "🥇 #01"
            elif idx == 2:
                medalla = "🥈 #02"
            elif idx == 3:
                medalla = "🥉 #03"

            tasaTexto = "Alto Desempeño" if completadas >= 2 else "En Progreso"
            self.treeviewRanking.insert(
                "",
                tk.END,
                values=(medalla, nombre, f"{completadas} tareas", tasaTexto)
            )


# ============================================================================
# CONTROLADOR PRINCIPAL DE LA APLICACIÓN (IMPERATIVE SHELL)
# ============================================================================
class App(tb.Window):
    """
    Imperative Shell:
    Controlador de la ventana principal de SIGESTA.
    Mantiene la referencia inmutable al 'EstadoSistema', coordina la navegación
    y sincroniza la persistencia con 'guardarEstado'.
    """

    def __init__(self, rutaEstado: str = "data/estado_sistema.json"):
        super().__init__(themename="darkly")
        self.rutaEstado = rutaEstado
        self.estadoSistema: EstadoSistema = cargarEstado(self.rutaEstado)
        self.usuarioActual: Optional[Usuario] = None
        self.iconoVentana = None

        self.title("SIGESTA - Sistema Integral de Gestión de Tareas")

        # 1. PANTALLA COMPLETA AUTOMÁTICA
        try:
            self.state("zoomed")
        except Exception:
            self.geometry("1200x760")
        self.minsize(980, 620)
        self.configure(bg=COLOR_FONDO_CANVAS)

        # 2. LOGO DE LA APLICACIÓN (Reemplaza la pluma azul de Tkinter)
        self.configurarIconoAplicacion()

        self.configurarEstilosPersonalizados()

        self.contenedorPrincipal = tk.Frame(self, bg=COLOR_FONDO_CANVAS)
        self.contenedorPrincipal.pack(fill=tk.BOTH, expand=True)

        self.vistaActual: Optional[tk.Widget] = None
        self.sidebar: Optional[SidebarFrame] = None

        self.mostrarVista("auth")

    def configurarIconoAplicacion(self):
        """Asigna el logo de SIGESTA como icono de la ventana y de la barra de tareas."""
        rutaLogo = obtenerRutaLogo()
        if rutaLogo:
            try:
                img = Image.open(rutaLogo)
                self.iconoVentana = ImageTk.PhotoImage(img.resize((64, 64), Image.Resampling.LANCZOS))
                self.iconphoto(True, self.iconoVentana)
            except Exception:
                pass

        rutaIco = obtenerRutaIcono()
        if rutaIco and sys.platform == "win32":
            try:
                self.iconbitmap(rutaIco)
            except Exception:
                pass

    def configurarEstilosPersonalizados(self):
        estilo = tb.Style()

        estilo.configure(
            "Treeview",
            background=COLOR_FONDO_SIDEBAR,
            foreground=COLOR_TEXTO_PRINCIPAL,
            fieldbackground=COLOR_FONDO_SIDEBAR,
            rowheight=34,
            font=("Inter", 9),
            borderwidth=0
        )
        estilo.configure(
            "Treeview.Heading",
            background=COLOR_FONDO_CARD,
            foreground=COLOR_TEXTO_SECUNDARIO,
            font=("JetBrains Mono", 8, "bold"),
            relief="flat",
            borderwidth=0
        )
        estilo.map(
            "Treeview",
            background=[("selected", COLOR_PRIMARIO_BASE)],
            foreground=[("selected", COLOR_ACENTO_MENTA)]
        )

        estilo.configure(
            "TCombobox",
            background=COLOR_FONDO_INPUT,
            fieldbackground=COLOR_FONDO_INPUT,
            foreground=COLOR_TEXTO_PRINCIPAL,
            arrowcolor=COLOR_TEXTO_SECUNDARIO
        )

    # ------------------------------------------------------------------------
    # MÉTODOS DE ESTADO Y CONTROL
    # ------------------------------------------------------------------------
    def obtenerEstado(self) -> EstadoSistema:
        return self.estadoSistema

    def obtenerUsuarioActual(self) -> Optional[Usuario]:
        return self.usuarioActual

    def esJefe(self) -> bool:
        return bool(self.usuarioActual and self.usuarioActual.rol == "JEFE")

    def actualizarEstado(self, nuevoEstado: EstadoSistema) -> None:
        guardarEstado(nuevoEstado, self.rutaEstado)
        self.estadoSistema = nuevoEstado

    def iniciarSesion(self, usuario: Usuario) -> None:
        self.usuarioActual = usuario
        self.mostrarVista("mis_tareas")

    def cerrarSesion(self) -> None:
        self.usuarioActual = None
        self.mostrarVista("auth")

    # ------------------------------------------------------------------------
    # GESTIÓN DE VISTAS Y TRANSICIONES
    # ------------------------------------------------------------------------
    def limpiarContenedor(self):
        for widget in self.contenedorPrincipal.winfo_children():
            widget.destroy()

    def mostrarVista(self, nombreVista: str):
        self.limpiarContenedor()

        if nombreVista == "auth":
            vista = AuthFrame(self.contenedorPrincipal, self)
            vista.pack(fill=tk.BOTH, expand=True)
            self.vistaActual = vista
            return

        # Vistas autenticadas con Sidebar
        layoutFrame = tk.Frame(self.contenedorPrincipal, bg=COLOR_FONDO_CANVAS)
        layoutFrame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = SidebarFrame(layoutFrame, self, vistaActiva=nombreVista)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        areaTrabajo = tk.Frame(layoutFrame, bg=COLOR_FONDO_CANVAS)
        areaTrabajo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        if nombreVista == "mis_tareas":
            vista = DashboardFrame(areaTrabajo, self, modo="mis_tareas")
        elif nombreVista == "tareas_personal":
            # Exclusiva de Jefe
            if not self.esJefe():
                self.mostrarVista("mis_tareas")
                return
            vista = DashboardFrame(areaTrabajo, self, modo="personal")
        elif nombreVista == "nueva_tarea":
            vista = TaskFormFrame(areaTrabajo, self)
        elif nombreVista == "ranking":
            # Exclusiva de Jefe
            if not self.esJefe():
                self.mostrarVista("mis_tareas")
                return
            vista = AnalyticsFrame(areaTrabajo, self)
        else:
            vista = DashboardFrame(areaTrabajo, self, modo="mis_tareas")

        vista.pack(fill=tk.BOTH, expand=True)
        self.vistaActual = vista


def iniciarGui(rutaEstado: str = "data/estado_sistema.json"):
    """Punto de entrada para ejecutar la interfaz gráfica de SIGESTA."""
    app = App(rutaEstado)
    app.mainloop()


if __name__ == "__main__":
    iniciarGui()
