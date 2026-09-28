class Usuario:
    """Representa un usuario utilizado en la simulación de acceso."""

    def __init__(self, usuario: str, clave: str, nombre: str, correo: str) -> None:
        self.usuario = str(usuario).strip()
        self.clave = str(clave)
        self.nombre = str(nombre).strip()
        self.correo = str(correo).strip()

        if not self.usuario:
            raise ValueError("El usuario no puede estar vacío.")
        if not self.clave:
            raise ValueError("La contraseña no puede estar vacía.")
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")

    def mostrar_informacion(self) -> str:
        return f"{self.usuario} - {self.nombre} | {self.correo}"

    def __str__(self) -> str:
        return self.mostrar_informacion()
