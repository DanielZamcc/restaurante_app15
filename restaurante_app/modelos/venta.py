from datetime import datetime


class Venta:
    """Representa una venta que relaciona un usuario con un producto."""

    def __init__(self, usuario: str, producto: str, fecha: str | None = None) -> None:
        self.usuario = str(usuario).strip()
        self.producto = str(producto).strip()
        self.fecha = str(fecha).strip() if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not self.usuario:
            raise ValueError("El usuario de la venta no puede estar vacío.")
        if not self.producto:
            raise ValueError("El producto de la venta no puede estar vacío.")
        if not self.fecha:
            raise ValueError("La fecha de la venta no puede estar vacía.")

    def mostrar_informacion(self) -> str:
        return f"{self.fecha} | Usuario: {self.usuario} | Producto: {self.producto}"

    def __str__(self) -> str:
        return self.mostrar_informacion()
