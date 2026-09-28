import json
from pathlib import Path


class ArchivoServicio:
    """Gestiona la lectura y escritura de los archivos JSON."""

    def __init__(self, ruta_productos: str | Path, ruta_usuarios: str | Path,
                 ruta_ventas: str | Path) -> None:
        self.ruta_productos = Path(ruta_productos)
        self.ruta_usuarios = Path(ruta_usuarios)
        self.ruta_ventas = Path(ruta_ventas)

    @staticmethod
    def _leer_json(ruta: Path) -> list[dict]:
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if not isinstance(datos, list):
                raise ValueError(f"{ruta.name} debe contener una lista JSON.")
            return datos
        except FileNotFoundError:
            print(f"No se encontró el archivo {ruta.name}.")
        except json.JSONDecodeError:
            print(f"El archivo {ruta.name} no contiene un JSON válido.")
        except (PermissionError, OSError, ValueError) as error:
            print(f"No fue posible leer {ruta.name}: {error}")
        return []

    @staticmethod
    def _escribir_json(ruta: Path, datos: list[dict]) -> bool:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            with ruta.open("w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            return True
        except (PermissionError, OSError) as error:
            print(f"No fue posible guardar {ruta.name}: {error}")
            return False

    def cargar_productos(self) -> list[dict]:
        return self._leer_json(self.ruta_productos)

    def cargar_usuarios(self) -> list[dict]:
        return self._leer_json(self.ruta_usuarios)

    def cargar_ventas(self) -> list[dict]:
        return self._leer_json(self.ruta_ventas)

    def guardar_productos(self, datos: list[dict]) -> bool:
        return self._escribir_json(self.ruta_productos, datos)

    def guardar_ventas(self, datos: list[dict]) -> bool:
        return self._escribir_json(self.ruta_ventas, datos)
