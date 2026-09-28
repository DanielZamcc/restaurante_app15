from pathlib import Path
import tkinter as tk
from tkinter import ttk

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

BASE = Path(__file__).resolve().parent


class RestauranteApp:
    """Coordina la única ventana principal y las vistas."""

    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante App - Semana 15")
        self.ventana.geometry("1120x700")
        self.ventana.minsize(940, 620)

        estilo = ttk.Style()
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")

        archivo_servicio = ArchivoServicio(
            ruta_productos=BASE / "datos" / "productos.json",
            ruta_usuarios=BASE / "datos" / "usuarios.json",
            ruta_ventas=BASE / "datos" / "ventas.json",
        )
        self.servicio = RestauranteServicio(archivo_servicio)
        self.vista_actual = None
        self.mostrar_login()

    def _cambiar_vista(self, nueva_vista) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self._cambiar_vista(LoginView(self.ventana, self.servicio, al_ingresar=self.mostrar_principal))

    def mostrar_principal(self, usuario) -> None:
        self._cambiar_vista(MainView(self.ventana, self.servicio, usuario_actual=usuario,
                                     al_cerrar_sesion=self.mostrar_login))

    def ejecutar(self) -> None:
        self.ventana.mainloop()


if __name__ == "__main__":
    RestauranteApp().ejecutar()
