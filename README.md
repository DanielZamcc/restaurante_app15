# Restaurante App - Semana 15

## Asignatura
**Programación Orientada a Objetos**

## Actividad
**Semana 15 - Taller práctico: organización modular y manejo de eventos**

## Descripción

Esta versión continúa directamente el proyecto `restaurante_app` de la Semana 14. Se conserva el inicio de sesión, la consulta de usuarios y la gestión CRUD de productos, y se incorpora una nueva sección de **Ventas** para evidenciar el flujo de eventos trabajado en la Semana 15.

La operación relaciona un usuario existente con un producto existente. El botón **Registrar venta** utiliza `command=` para ejecutar un callback. El callback obtiene las selecciones de la interfaz y delega la operación a `RestauranteServicio`, que valida, registra la venta y conserva los datos en `datos/ventas.json`. Al registrar una venta se descuenta una unidad del stock del producto y se actualiza `productos.json`.

## Flujo de eventos

```text
Usuario
  ↓
Botón Registrar venta
  ↓
command=registrar_venta
  ↓
Callback registrar_venta()
  ↓
RestauranteServicio.registrar_venta()
  ↓
Validación + persistencia
  ↓
ventas.json / productos.json
  ↓
Actualización de Treeview + respuesta visual
```

El callback coordina la interacción, pero las validaciones y la persistencia permanecen en la capa de servicios. La interfaz no escribe directamente en los archivos JSON.

## Estructura

```text
Repositorio GitHub/
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   ├── assets/
│   │   ├── logo.png
│   │   └── icon.png
│   └── main.py
└── README.md
```

## Funciones principales

- Inicio de sesión mediante usuarios registrados en JSON.
- Consulta de usuarios.
- Registro, consulta, actualización y eliminación de productos.
- Sección de Ventas.
- Selección de usuario y producto mediante `ttk.Combobox`.
- Registro mediante botón con `command=` y callback.
- Validación de usuario, producto y stock en `RestauranteServicio`.
- Persistencia de ventas en `ventas.json`.
- Actualización del stock y persistencia en `productos.json`.
- Presentación de las ventas en `ttk.Treeview`.
- Recursos visuales obligatorios en `assets/`, incluyendo logo e ícono.

## Ejecución

Requiere Python 3.10 o superior.

Desde una terminal ubicada en la carpeta que contiene `restaurante_app`:

```bash
cd restaurante_app
python main.py
```

## Credenciales de prueba

```text
Usuario: admin
Contraseña: 1234
```

También:

```text
Usuario: invitado
Contraseña: 2026
```

## Comprobación de la Semana 15

1. Ejecutar `main.py` sin errores.
2. Iniciar sesión.
3. Comprobar las secciones Inicio, Usuarios y Productos.
4. Abrir **Ventas**.
5. Seleccionar un usuario existente.
6. Seleccionar un producto con stock.
7. Pulsar **Registrar venta**.
8. Verificar la respuesta visual y la actualización de la tabla.
9. Verificar que la venta se almacene en `ventas.json`.
10. Verificar que el stock se actualice en `productos.json`.
11. Cerrar y volver a ejecutar para comprobar que la venta se recupere correctamente.
12. Verificar que no existan referencias ajenas al dominio del restaurante.

## Alcance

No se implementan `bind()`, doble clic, eventos de teclado o mouse, `<<TreeviewSelect>>`, facturación, carrito de compras, inventario avanzado ni bases de datos, porque no forman parte del alcance solicitado para esta semana.
"# restaurante_app15" 
