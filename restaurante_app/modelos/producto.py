class Producto:
    """Representa un producto disponible en el restaurante."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        categoria: str,
        stock: int = 0,
    ) -> None:
        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.categoria = str(categoria).strip()
        self.stock = int(stock)

        if not self.codigo:
            raise ValueError("El código del producto no puede estar vacío.")
        if not self.nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not self.categoria:
            raise ValueError("La categoría no puede estar vacía.")

    def mostrar_informacion(self) -> str:
        return (
            f"{self.codigo} - {self.nombre} | "
            f"${self.precio:.2f} | {self.categoria} | Stock: {self.stock}"
        )

    def __str__(self) -> str:
        return self.mostrar_informacion()
