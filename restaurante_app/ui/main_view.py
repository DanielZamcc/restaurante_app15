import tkinter as tk
from tkinter import messagebox, ttk

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """Interfaz principal: navegación, usuarios, productos y ventas."""

    def __init__(self, parent: tk.Misc, servicio: RestauranteServicio,
                 usuario_actual: Usuario, al_cerrar_sesion) -> None:
        super().__init__(parent, padding=14)
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        encabezado.columnconfigure(1, weight=1)
        ttk.Label(encabezado, text="Restaurante App", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, rowspan=2, sticky="w", padx=(0, 14))
        ttk.Label(encabezado, text="Semana 15 · Gestión de ventas y eventos",
                  font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")
        ttk.Label(encabezado, text=f"Usuario: {usuario_actual.nombre}").grid(row=1, column=1, sticky="w")

        menu = ttk.LabelFrame(self, text="Navegación", padding=10)
        menu.grid(row=1, column=0, sticky="ns", padx=(0, 12))
        for texto, comando in (("Inicio", self.mostrar_resumen), ("Productos", self.mostrar_productos),
                               ("Usuarios", self.mostrar_usuarios), ("Ventas", self.mostrar_ventas)):
            ttk.Button(menu, text=texto, command=comando, width=18).pack(fill="x", pady=4)
        ttk.Separator(menu).pack(fill="x", pady=10)
        ttk.Button(menu, text="Cerrar sesión", command=self.al_cerrar_sesion, width=18).pack(fill="x", pady=4)

        self.contenido = ttk.Frame(self)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(1, weight=1)
        self.mostrar_resumen()

    def _limpiar_contenido(self) -> None:
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_resumen(self) -> None:
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Resumen del sistema", font=("Segoe UI", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 12))
        resumen = ttk.LabelFrame(self.contenido, text="Información", padding=18)
        resumen.grid(row=1, column=0, sticky="nw")
        ttk.Label(resumen, text=(f"Productos registrados: {self.servicio.cantidad_productos()}\n"
            f"Usuarios registrados: {self.servicio.cantidad_usuarios()}\n"
            f"Ventas registradas: {self.servicio.cantidad_ventas()}\n\n"
            "Seleccione una sección del menú para trabajar con el sistema."), justify="left").pack()

    def mostrar_usuarios(self) -> None:
        self._limpiar_contenido()
        ttk.Label(self.contenido, text="Consulta de usuarios", font=("Segoe UI", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8))
        marco = ttk.LabelFrame(self.contenido, text="Usuarios registrados", padding=8)
        marco.grid(row=1, column=0, sticky="nsew")
        marco.columnconfigure(0, weight=1); marco.rowconfigure(0, weight=1)
        columnas = ("usuario", "nombre", "correo")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for columna, titulo, ancho in (("usuario", "Usuario", 130), ("nombre", "Nombre", 220), ("correo", "Correo", 280)):
            tabla.heading(columna, text=titulo); tabla.column(columna, width=ancho, anchor="center")
        scroll = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview); tabla.configure(yscrollcommand=scroll.set)
        tabla.grid(row=0, column=0, sticky="nsew"); scroll.grid(row=0, column=1, sticky="ns")
        for usuario in self.servicio.listar_usuarios():
            tabla.insert("", tk.END, values=(usuario.usuario, usuario.nombre, usuario.correo))

    def mostrar_productos(self) -> None:
        self._limpiar_contenido()
        self.contenido.rowconfigure(1, weight=0); self.contenido.rowconfigure(2, weight=1)
        ttk.Label(self.contenido, text="Gestión de productos", font=("Segoe UI", 15, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8))
        formulario = ttk.LabelFrame(self.contenido, text="Formulario de producto", padding=10)
        formulario.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        for columna in range(4): formulario.columnconfigure(columna, weight=1)
        self.codigo_var = tk.StringVar(); self.nombre_var = tk.StringVar(); self.precio_var = tk.StringVar()
        self.categoria_var = tk.StringVar(); self.stock_var = tk.StringVar()
        for col, label, var in ((0,"Código:",self.codigo_var),(1,"Nombre:",self.nombre_var),(2,"Precio:",self.precio_var)):
            ttk.Label(formulario, text=label).grid(row=0, column=col, sticky="w")
            ttk.Entry(formulario, textvariable=var).grid(row=1, column=col, sticky="ew", padx=8, pady=(3,8))
        ttk.Label(formulario, text="Categoría:").grid(row=0, column=3, sticky="w")
        ttk.Combobox(formulario, textvariable=self.categoria_var,
                     values=("Plato fuerte","Bebida","Postre","Entrada"), state="normal").grid(
            row=1, column=3, sticky="ew", padx=8, pady=(3,8))
        ttk.Label(formulario, text="Stock:").grid(row=2, column=0, sticky="w")
        ttk.Entry(formulario, textvariable=self.stock_var).grid(row=3, column=0, sticky="ew", padx=8)
        botones = ttk.Frame(formulario); botones.grid(row=3, column=1, columnspan=3, sticky="e")
        for texto, comando in (("Registrar",self.registrar_producto),("Cargar / Consultar",self.cargar_producto),
                               ("Actualizar",self.actualizar_producto),("Eliminar",self.eliminar_producto),("Limpiar",self.limpiar_formulario)):
            ttk.Button(botones, text=texto, command=comando).pack(side="left", padx=3)
        tabla_frame = ttk.LabelFrame(self.contenido, text="Productos registrados", padding=8)
        tabla_frame.grid(row=2, column=0, sticky="nsew"); tabla_frame.columnconfigure(0, weight=1); tabla_frame.rowconfigure(0, weight=1)
        columnas=("codigo","nombre","precio","categoria","stock")
        self.tabla_productos=ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)
        for columna,titulo,ancho in (("codigo","Código",80),("nombre","Nombre",180),("precio","Precio",90),("categoria","Categoría",130),("stock","Stock",70)):
            self.tabla_productos.heading(columna,text=titulo); self.tabla_productos.column(columna,width=ancho,anchor="center")
        scroll=ttk.Scrollbar(tabla_frame,orient="vertical",command=self.tabla_productos.yview); self.tabla_productos.configure(yscrollcommand=scroll.set)
        self.tabla_productos.grid(row=0,column=0,sticky="nsew"); scroll.grid(row=0,column=1,sticky="ns")
        self.actualizar_tabla_productos()

    def _datos_formulario(self):
        return (self.codigo_var.get(), self.nombre_var.get(), self.precio_var.get(), self.categoria_var.get(), self.stock_var.get())

    def actualizar_tabla_productos(self) -> None:
        if not hasattr(self, "tabla_productos"): return
        for item in self.tabla_productos.get_children(): self.tabla_productos.delete(item)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert("", tk.END, values=(producto.codigo, producto.nombre, f"${producto.precio:.2f}", producto.categoria, producto.stock))

    def registrar_producto(self) -> None:
        try: self.servicio.registrar_producto(*self._datos_formulario())
        except (ValueError,OSError) as error: messagebox.showerror("No se pudo registrar", str(error)); return
        messagebox.showinfo("Producto registrado", "El producto fue guardado correctamente."); self.actualizar_tabla_productos(); self.limpiar_formulario()

    def cargar_producto(self) -> None:
        producto=self.servicio.buscar_producto(self.codigo_var.get())
        if producto is None: messagebox.showwarning("Producto no encontrado","Ingrese un código existente."); return
        self.nombre_var.set(producto.nombre); self.precio_var.set(str(producto.precio)); self.categoria_var.set(producto.categoria); self.stock_var.set(str(producto.stock))

    def actualizar_producto(self) -> None:
        try: self.servicio.actualizar_producto(*self._datos_formulario())
        except (ValueError,OSError) as error: messagebox.showerror("No se pudo actualizar",str(error)); return
        messagebox.showinfo("Producto actualizado","Los cambios fueron guardados."); self.actualizar_tabla_productos(); self.limpiar_formulario()

    def eliminar_producto(self) -> None:
        codigo=self.codigo_var.get().strip()
        if not codigo: messagebox.showwarning("Código requerido","Ingrese el código del producto."); return
        producto=self.servicio.buscar_producto(codigo)
        if producto is None: messagebox.showwarning("Producto no encontrado","No existe ese producto."); return
        if not messagebox.askyesno("Confirmar eliminación",f"¿Desea eliminar el producto '{producto.nombre}'?"): return
        try: self.servicio.eliminar_producto(codigo)
        except (ValueError,OSError) as error: messagebox.showerror("No se pudo eliminar",str(error)); return
        messagebox.showinfo("Producto eliminado","El producto fue eliminado."); self.actualizar_tabla_productos(); self.limpiar_formulario()

    def limpiar_formulario(self) -> None:
        for variable in (self.codigo_var,self.nombre_var,self.precio_var,self.categoria_var,self.stock_var): variable.set("")

    def mostrar_ventas(self) -> None:
        self._limpiar_contenido()
        self.contenido.rowconfigure(1, weight=0); self.contenido.rowconfigure(2, weight=1)
        ttk.Label(self.contenido, text="Gestión de ventas", font=("Segoe UI",15,"bold")).grid(row=0,column=0,sticky="w",pady=(0,8))
        formulario=ttk.LabelFrame(self.contenido,text="Registrar venta",padding=12); formulario.grid(row=1,column=0,sticky="ew",pady=(0,10))
        formulario.columnconfigure(0,weight=1); formulario.columnconfigure(1,weight=1); formulario.columnconfigure(2,weight=0)
        ttk.Label(formulario,text="Usuario:").grid(row=0,column=0,sticky="w")
        self.venta_usuario_var=tk.StringVar()
        usuarios=[f"{u.usuario} - {u.nombre}" for u in self.servicio.listar_usuarios()]
        self.venta_usuario_combo=ttk.Combobox(formulario,textvariable=self.venta_usuario_var,values=usuarios,state="readonly")
        self.venta_usuario_combo.grid(row=1,column=0,sticky="ew",padx=(0,10),pady=(3,8))
        ttk.Label(formulario,text="Producto:").grid(row=0,column=1,sticky="w")
        self.venta_producto_var=tk.StringVar()
        self.venta_producto_combo=ttk.Combobox(formulario,textvariable=self.venta_producto_var,values=self._opciones_productos(),state="readonly")
        self.venta_producto_combo.grid(row=1,column=1,sticky="ew",padx=(0,10),pady=(3,8))
        ttk.Button(formulario,text="Registrar venta",command=self.registrar_venta).grid(row=1,column=2,padx=4,pady=(3,8))
        ttk.Label(formulario,text="El botón usa command=registrar_venta y el callback delega la operación a RestauranteServicio.").grid(
            row=2,column=0,columnspan=3,sticky="w",pady=(3,0))
        tabla_frame=ttk.LabelFrame(self.contenido,text="Ventas registradas",padding=8); tabla_frame.grid(row=2,column=0,sticky="nsew")
        tabla_frame.columnconfigure(0,weight=1); tabla_frame.rowconfigure(0,weight=1)
        columnas=("fecha","usuario","producto","nombre_producto")
        self.tabla_ventas=ttk.Treeview(tabla_frame,columns=columnas,show="headings")
        for col,titulo,ancho in (("fecha","Fecha",170),("usuario","Usuario",140),("producto","Código",100),("nombre_producto","Producto",240)):
            self.tabla_ventas.heading(col,text=titulo); self.tabla_ventas.column(col,width=ancho,anchor="center")
        scroll=ttk.Scrollbar(tabla_frame,orient="vertical",command=self.tabla_ventas.yview); self.tabla_ventas.configure(yscrollcommand=scroll.set)
        self.tabla_ventas.grid(row=0,column=0,sticky="nsew"); scroll.grid(row=0,column=1,sticky="ns")
        self.actualizar_tabla_ventas()

    def _opciones_productos(self):
        return [f"{p.codigo} - {p.nombre} (Stock: {p.stock})" for p in self.servicio.listar_productos() if p.stock > 0]

    @staticmethod
    def _codigo_desde_opcion(opcion: str) -> str:
        return opcion.split(" - ",1)[0].strip()

    def registrar_venta(self) -> None:
        usuario_opcion=self.venta_usuario_var.get().strip(); producto_opcion=self.venta_producto_var.get().strip()
        if not usuario_opcion or not producto_opcion:
            messagebox.showwarning("Datos requeridos","Seleccione un usuario y un producto."); return
        usuario=self._codigo_desde_opcion(usuario_opcion)
        producto=self._codigo_desde_opcion(producto_opcion)
        try: venta=self.servicio.registrar_venta(usuario,producto)
        except (ValueError,OSError) as error: messagebox.showerror("No se pudo registrar la venta",str(error)); return
        messagebox.showinfo("Venta registrada",f"Venta registrada correctamente.\nFecha: {venta.fecha}")
        self.venta_producto_combo["values"]=self._opciones_productos(); self.venta_producto_var.set("")
        self.actualizar_tabla_ventas()

    def actualizar_tabla_ventas(self) -> None:
        if not hasattr(self,"tabla_ventas"): return
        for item in self.tabla_ventas.get_children(): self.tabla_ventas.delete(item)
        for venta in self.servicio.listar_ventas():
            producto=self.servicio.buscar_producto(venta.producto)
            nombre=producto.nombre if producto else "Producto no disponible"
            self.tabla_ventas.insert("",tk.END,values=(venta.fecha,venta.usuario,venta.producto,nombre))
