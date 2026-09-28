import tkinter as tk
from tkinter import ttk
from pathlib import Path

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """Pantalla de acceso al sistema."""

    def __init__(self, parent: tk.Misc, servicio: RestauranteServicio, al_ingresar) -> None:
        super().__init__(parent, padding=30)
        self.servicio = servicio
        self.al_ingresar = al_ingresar
        self.columnconfigure(0, weight=1)

        tarjeta = ttk.LabelFrame(self, text="Acceso al sistema", padding=24)
        tarjeta.grid(row=0, column=0, padx=80, pady=55, sticky="nsew")
        tarjeta.columnconfigure(1, weight=1)

        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            self.logo = tk.PhotoImage(file=str(logo_path)).subsample(4, 4)
            ttk.Label(tarjeta, image=self.logo).grid(row=0, column=0, columnspan=2, pady=(0, 8))

        ttk.Label(tarjeta, text="RESTAURANTE APP", font=("Segoe UI", 20, "bold")).grid(
            row=1, column=0, columnspan=2, pady=(0, 5))
        ttk.Label(tarjeta, text="Semana 15 - Manejo de eventos y ventas").grid(
            row=2, column=0, columnspan=2, pady=(0, 22))

        ttk.Label(tarjeta, text="Usuario:").grid(row=3, column=0, sticky="e", padx=8, pady=8)
        self.entrada_usuario = ttk.Entry(tarjeta, width=30)
        self.entrada_usuario.grid(row=3, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(tarjeta, text="Contraseña:").grid(row=4, column=0, sticky="e", padx=8, pady=8)
        self.entrada_clave = ttk.Entry(tarjeta, width=30, show="*")
        self.entrada_clave.grid(row=4, column=1, sticky="ew", padx=8, pady=8)

        self.mensaje = ttk.Label(tarjeta, text="", anchor="center")
        self.mensaje.grid(row=5, column=0, columnspan=2, pady=8)
        ttk.Button(tarjeta, text="Ingresar", command=self.intentar_ingreso).grid(
            row=6, column=0, columnspan=2, pady=12, ipadx=30)
        ttk.Label(tarjeta, text="Usuarios y datos persistidos mediante archivos JSON").grid(
            row=7, column=0, columnspan=2, pady=(12, 0))
        self.entrada_usuario.focus_set()

    def intentar_ingreso(self) -> None:
        usuario = self.entrada_usuario.get().strip()
        clave = self.entrada_clave.get()
        if not usuario or not clave:
            self.mensaje.config(text="Complete el usuario y la contraseña.")
            return
        persona = self.servicio.validar_acceso(usuario, clave)
        if persona is None:
            self.mensaje.config(text="Usuario o contraseña incorrectos.")
            self.entrada_clave.delete(0, tk.END)
            return
        self.al_ingresar(persona)
