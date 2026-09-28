from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Contiene las reglas de negocio y coordina la persistencia."""

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self._archivo_servicio = archivo_servicio
        self._productos = self._crear_productos(self._archivo_servicio.cargar_productos())
        self._usuarios = self._crear_usuarios(self._archivo_servicio.cargar_usuarios())
        self._ventas = self._crear_ventas(self._archivo_servicio.cargar_ventas())

    @staticmethod
    def _crear_productos(datos: list[dict]) -> list[Producto]:
        productos = []
        for registro in datos:
            try:
                productos.append(Producto(codigo=registro["codigo"], nombre=registro["nombre"],
                    precio=registro["precio"], categoria=registro["categoria"],
                    stock=registro.get("stock", 0)))
            except (KeyError, TypeError, ValueError):
                continue
        return productos

    @staticmethod
    def _crear_usuarios(datos: list[dict]) -> list[Usuario]:
        usuarios = []
        for registro in datos:
            try:
                usuarios.append(Usuario(usuario=registro["usuario"], clave=registro["clave"],
                    nombre=registro["nombre"], correo=registro.get("correo", "")))
            except (KeyError, TypeError, ValueError):
                continue
        return usuarios

    @staticmethod
    def _crear_ventas(datos: list[dict]) -> list[Venta]:
        ventas = []
        for registro in datos:
            try:
                ventas.append(Venta(usuario=registro["usuario"], producto=registro["producto"],
                    fecha=registro["fecha"]))
            except (KeyError, TypeError, ValueError):
                continue
        return ventas

    def validar_acceso(self, usuario: str, clave: str) -> Usuario | None:
        usuario = usuario.strip()
        for persona in self._usuarios:
            if persona.usuario == usuario and persona.clave == clave:
                return persona
        return None

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def listar_ventas(self) -> list[Venta]:
        return list(self._ventas)

    def cantidad_productos(self) -> int:
        return len(self._productos)

    def cantidad_usuarios(self) -> int:
        return len(self._usuarios)

    def cantidad_ventas(self) -> int:
        return len(self._ventas)

    def buscar_usuario(self, usuario: str) -> Usuario | None:
        usuario = str(usuario).strip()
        for persona in self._usuarios:
            if persona.usuario == usuario:
                return persona
        return None

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = str(codigo).strip()
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    @staticmethod
    def _validar_datos_producto(codigo: str, nombre: str, precio: str | float,
                                categoria: str, stock: str | int) -> tuple[str, str, float, str, int]:
        codigo, nombre, categoria = str(codigo).strip(), str(nombre).strip(), str(categoria).strip()
        if not codigo or not nombre or not categoria:
            raise ValueError("Complete código, nombre y categoría.")
        try:
            precio_num = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser numérico.")
        if precio_num < 0:
            raise ValueError("El precio no puede ser negativo.")
        try:
            stock_num = int(stock)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un número entero.")
        if stock_num < 0:
            raise ValueError("El stock no puede ser negativo.")
        return codigo, nombre, precio_num, categoria, stock_num

    @staticmethod
    def _producto_a_dict(producto: Producto) -> dict:
        return {"codigo": producto.codigo, "nombre": producto.nombre,
                "precio": producto.precio, "categoria": producto.categoria, "stock": producto.stock}

    @staticmethod
    def _venta_a_dict(venta: Venta) -> dict:
        return {"usuario": venta.usuario, "producto": venta.producto, "fecha": venta.fecha}

    def _guardar_productos(self) -> None:
        if not self._archivo_servicio.guardar_productos([self._producto_a_dict(p) for p in self._productos]):
            raise OSError("No se pudo guardar productos.json.")

    def _guardar_ventas(self) -> None:
        if not self._archivo_servicio.guardar_ventas([self._venta_a_dict(v) for v in self._ventas]):
            raise OSError("No se pudo guardar ventas.json.")

    def registrar_producto(self, codigo: str, nombre: str, precio: str | float,
                           categoria: str, stock: str | int) -> Producto:
        datos = self._validar_datos_producto(codigo, nombre, precio, categoria, stock)
        if self.buscar_producto(datos[0]) is not None:
            raise ValueError("Ya existe un producto con ese código.")
        producto = Producto(*datos)
        self._productos.append(producto)
        try:
            self._guardar_productos()
        except Exception:
            self._productos.remove(producto)
            raise
        return producto

    def actualizar_producto(self, codigo: str, nombre: str, precio: str | float,
                            categoria: str, stock: str | int) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        datos = self._validar_datos_producto(codigo, nombre, precio, categoria, stock)
        producto.nombre, producto.precio, producto.categoria, producto.stock = datos[1], datos[2], datos[3], datos[4]
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> None:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese código.")
        self._productos.remove(producto)
        try:
            self._guardar_productos()
        except Exception:
            self._productos.append(producto)
            raise

    def registrar_venta(self, usuario: str, producto: str) -> Venta:
        persona = self.buscar_usuario(usuario)
        if persona is None:
            raise ValueError("El usuario seleccionado no existe.")
        articulo = self.buscar_producto(producto)
        if articulo is None:
            raise ValueError("El producto seleccionado no existe.")
        if articulo.stock <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        venta = Venta(persona.usuario, articulo.codigo)
        articulo.stock -= 1
        self._ventas.append(venta)
        try:
            self._guardar_productos()
            self._guardar_ventas()
        except Exception:
            articulo.stock += 1
            self._ventas.remove(venta)
            raise
        return venta
