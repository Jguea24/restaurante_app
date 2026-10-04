import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class MainView(tk.Frame):
    """Vista principal del restaurante con diseño mejorado, alto contraste y gestión de ventas."""
    
    def __init__(self, master, usuario_actual, servicio, on_logout):
        super().__init__(master, bg="#F1F5F9")
        self.master = master
        self.usuario_actual = usuario_actual
        self.servicio = servicio
        self.on_logout = on_logout

        self.master.title("Restaurante App - Sistema de Gestión")
        self.master.geometry("980x680")
        self.master.minsize(900, 620)
        self.master.configure(bg="#F1F5F9")

        self.pack(fill="both", expand=True)
        self._configurar_estilos()
        self._construir_encabezado()
        self._construir_cuerpo()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo para Notebook (pestañas con buen contraste)
        style.configure("TNotebook", background="#F1F5F9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[16, 8],
                        background="#E2E8F0", foreground="#334155")
        style.map("TNotebook.Tab",
                  background=[("selected", "#0F172A")],
                  foreground=[("selected", "#FFFFFF")])

        # Estilo para Treeview (tablas de datos nítidas)
        style.configure("Custom.Treeview",
                        background="#FFFFFF",
                        foreground="#0F172A",
                        rowheight=26,
                        fieldbackground="#FFFFFF",
                        font=("Helvetica", 9))
        style.configure("Custom.Treeview.Heading",
                        background="#1E293B",
                        foreground="#FFFFFF",
                        font=("Helvetica", 9, "bold"),
                        relief="flat")
        style.map("Custom.Treeview.Heading",
                  background=[("active", "#334155")],
                  foreground=[("active", "#FFFFFF")])
        style.map("Custom.Treeview",
                  background=[("selected", "#2563EB")],
                  foreground=[("selected", "#FFFFFF")])

    def _construir_encabezado(self):
        header = tk.Frame(self, bg="#0F172A", height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Cargar logo de assets/
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        logo_path = os.path.join(assets_dir, "logo.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path).resize((200, 50), Image.Resampling.LANCZOS)
                self.logo_header = ImageTk.PhotoImage(img)
                lbl_logo = tk.Label(header, image=self.logo_header, bg="#0F172A")
                lbl_logo.pack(side="left", padx=15, pady=10)
            except Exception:
                tk.Label(header, text="🍽️ RESTAURANTE APP", font=("Helvetica", 14, "bold"),
                         bg="#0F172A", fg="#FFFFFF").pack(side="left", padx=20)
        else:
            tk.Label(header, text="🍽️ RESTAURANTE APP", font=("Helvetica", 14, "bold"),
                     bg="#0F172A", fg="#FFFFFF").pack(side="left", padx=20)

        # Información de sesión
        user_info = tk.Frame(header, bg="#0F172A")
        user_info.pack(side="right", padx=20, pady=10)

        tk.Label(user_info, text=f"Usuario: {self.usuario_actual.username} ({self.usuario_actual.rol})",
                 font=("Helvetica", 10, "bold"), bg="#0F172A", fg="#F8FAFC").pack(side="left", padx=15)

        btn_salir = tk.Button(user_info, text="Cerrar Sesión", font=("Helvetica", 9, "bold"),
                              bg="#DC2626", fg="#FFFFFF", activebackground="#B91C1C", activeforeground="#FFFFFF",
                              bd=0, relief="flat", cursor="hand2", padx=12, pady=5, command=self.on_logout)
        btn_salir.pack(side="left")

    def _construir_cuerpo(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        # Pestañas del sistema
        self.tab_ventas = tk.Frame(self.notebook, bg="#F8FAFC")
        self.tab_productos = tk.Frame(self.notebook, bg="#F8FAFC")
        self.tab_usuarios = tk.Frame(self.notebook, bg="#F8FAFC")

        self.notebook.add(self.tab_ventas, text=" Registro de Ventas ")
        self.notebook.add(self.tab_productos, text=" Gestión de Productos ")
        self.notebook.add(self.tab_usuarios, text=" Gestión de Usuarios ")

        # Construcción de cada vista interna
        self._construir_seccion_ventas()
        self._construir_seccion_productos()
        self._construir_seccion_usuarios()

    # =========================================================================
    # SECCIÓN 1: VENTAS (SEMANA 15 - MANEJO DE EVENTOS)
    # =========================================================================
    def _construir_seccion_ventas(self):
        # Panel superior de registro
        panel_registro = tk.LabelFrame(self.tab_ventas, text=" Registrar Nueva Venta ",
                                       font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#0F172A", bd=1, padx=15, pady=15)
        panel_registro.pack(fill="x", padx=15, pady=(15, 10))

        campos = tk.Frame(panel_registro, bg="#FFFFFF")
        campos.pack(fill="x")

        # Selector de Usuario
        tk.Label(campos, text="Atendido por (Usuario):", font=("Helvetica", 9, "bold"),
                 bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.cbo_usuario = ttk.Combobox(campos, state="readonly", font=("Helvetica", 10), width=28)
        self.cbo_usuario.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Selector de Producto
        tk.Label(campos, text="Producto seleccionado:", font=("Helvetica", 9, "bold"),
                 bg="#FFFFFF", fg="#334155").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.cbo_producto = ttk.Combobox(campos, state="readonly", font=("Helvetica", 10), width=40)
        self.cbo_producto.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")

        # BOTÓN CON EVENTO COMMAND ASOCIADO DIRECTAMENTE AL CALLBACK (Rúbrica)
        self.btn_registrar_venta = tk.Button(
            campos,
            text="➕ REGISTRAR VENTA",
            font=("Helvetica", 10, "bold"),
            bg="#059669",
            fg="#FFFFFF",
            activebackground="#047857",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=6,
            command=self._registrar_venta  # command=callback sin paréntesis
        )
        self.btn_registrar_venta.grid(row=1, column=2, padx=15, pady=(0, 10), sticky="e")

        # Panel inferior: Historial de Ventas (Treeview)
        panel_tabla = tk.LabelFrame(self.tab_ventas, text=" Historial de Ventas Registradas ",
                                     font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#0F172A", bd=1, padx=10, pady=10)
        panel_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columnas = ("id", "fecha", "usuario", "producto", "total")
        self.tabla_ventas = ttk.Treeview(panel_tabla, columns=columnas, show="headings", style="Custom.Treeview")
        self.tabla_ventas.heading("id", text="N° Venta")
        self.tabla_ventas.heading("fecha", text="Fecha y Hora")
        self.tabla_ventas.heading("usuario", text="Vendedor / Mesero")
        self.tabla_ventas.heading("producto", text="Producto Consumido")
        self.tabla_ventas.heading("total", text="Total ($)")

        self.tabla_ventas.column("id", width=80, anchor="center")
        self.tabla_ventas.column("fecha", width=160, anchor="center")
        self.tabla_ventas.column("usuario", width=160, anchor="w")
        self.tabla_ventas.column("producto", width=260, anchor="w")
        self.tabla_ventas.column("total", width=100, anchor="e")

        scroll_v = ttk.Scrollbar(panel_tabla, orient="vertical", command=self.tabla_ventas.yview)
        self.tabla_ventas.configure(yscrollcommand=scroll_v.set)

        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll_v.pack(side="right", fill="y")

        # Inicializar datos en la vista de ventas
        self._cargar_combos_ventas()
        self._cargar_tabla_ventas()

    def _cargar_combos_ventas(self):
        # Poblar combobox de usuarios
        usuarios = self.servicio.obtener_usuarios()
        self.usuarios_map = {f"{u.id_usuario} - {u.username} ({u.rol})": u.id_usuario for u in usuarios}
        self.cbo_usuario["values"] = list(self.usuarios_map.keys())
        # Preseleccionar el usuario logueado
        for texto, id_u in self.usuarios_map.items():
            if id_u == self.usuario_actual.id_usuario:
                self.cbo_usuario.set(texto)
                break

        # Poblar combobox de productos
        productos = self.servicio.obtener_productos()
        self.productos_map = {f"{p.id_producto} - {p.nombre} (${p.precio:.2f})": p.id_producto for p in productos}
        self.cbo_producto["values"] = list(self.productos_map.keys())
        if self.cbo_producto["values"]:
            self.cbo_producto.current(0)

    def _cargar_tabla_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        ventas = self.servicio.obtener_ventas()
        for v in ventas:
            self.tabla_ventas.insert("", "end", values=(
                f"#{v.id_venta}",
                v.fecha,
                v.nombre_usuario,
                v.nombre_producto,
                f"${v.total:.2f}"
            ))

    def _registrar_venta(self):
        """Callback de evento para registrar la venta delegando al servicio."""
        usuario_txt = self.cbo_usuario.get()
        producto_txt = self.cbo_producto.get()

        if not usuario_txt or not producto_txt:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario y un producto.")
            return

        id_usuario = self.usuarios_map.get(usuario_txt)
        id_producto = self.productos_map.get(producto_txt)

        # Delegación exclusiva a RestauranteServicio
        exito, mensaje = self.servicio.registrar_venta(id_usuario, id_producto)

        if exito:
            self._cargar_tabla_ventas()
            messagebox.showinfo("Venta Exitosa", mensaje)
        else:
            messagebox.showerror("Error al Registrar", mensaje)

    # =========================================================================
    # SECCIÓN 2: PRODUCTOS (Mantenida y Estilizada)
    # =========================================================================
    def _construir_seccion_productos(self):
        # Formulario
        f_form = tk.LabelFrame(self.tab_productos, text=" Formulario de Producto ",
                               font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#0F172A", bd=1, padx=15, pady=10)
        f_form.pack(fill="x", padx=15, pady=(15, 10))

        tk.Label(f_form, text="ID Producto:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.txt_prod_id = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=12)
        self.txt_prod_id.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        tk.Label(f_form, text="Nombre:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.txt_prod_nom = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=28)
        self.txt_prod_nom.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        tk.Label(f_form, text="Categoría:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.txt_prod_cat = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=16)
        self.txt_prod_cat.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        tk.Label(f_form, text="Precio ($):", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.txt_prod_pre = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=16)
        self.txt_prod_pre.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        # Botonera de productos con colores diferenciados
        f_btns = tk.Frame(f_form, bg="#FFFFFF")
        f_btns.grid(row=2, column=0, columnspan=4, pady=10, sticky="w")

        tk.Button(f_btns, text="Registrar", font=("Helvetica", 9, "bold"), bg="#2563EB", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._prod_registrar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Actualizar", font=("Helvetica", 9, "bold"), bg="#D97706", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._prod_actualizar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Eliminar", font=("Helvetica", 9, "bold"), bg="#DC2626", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._prod_eliminar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Limpiar", font=("Helvetica", 9, "bold"), bg="#475569", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._prod_limpiar).pack(side="left", padx=4)

        # Tabla de Productos
        f_tabla = tk.LabelFrame(self.tab_productos, text=" Catálogo de Productos ",
                                font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#0F172A", bd=1, padx=10, pady=10)
        f_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.tabla_productos = ttk.Treeview(f_tabla, columns=("id", "nom", "cat", "pre"), show="headings", style="Custom.Treeview")
        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nom", text="Nombre")
        self.tabla_productos.heading("cat", text="Categoría")
        self.tabla_productos.heading("pre", text="Precio ($)")

        self.tabla_productos.column("id", width=60, anchor="center")
        self.tabla_productos.column("nom", width=250, anchor="w")
        self.tabla_productos.column("cat", width=160, anchor="w")
        self.tabla_productos.column("pre", width=100, anchor="e")

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        self.tabla_productos.bind("<Double-1>", self._prod_seleccionar_fila)
        self._cargar_tabla_productos()

    def _cargar_tabla_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for p in self.servicio.obtener_productos():
            self.tabla_productos.insert("", "end", values=(p.id_producto, p.nombre, p.categoria, f"${p.precio:.2f}"))

    def _prod_seleccionar_fila(self, event):
        item = self.tabla_productos.focus()
        if item:
            val = self.tabla_productos.item(item, "values")
            self.txt_prod_id.delete(0, tk.END)
            self.txt_prod_id.insert(0, val[0])
            self.txt_prod_nom.delete(0, tk.END)
            self.txt_prod_nom.insert(0, val[1])
            self.txt_prod_cat.delete(0, tk.END)
            self.txt_prod_cat.insert(0, val[2])
            self.txt_prod_pre.delete(0, tk.END)
            self.txt_prod_pre.insert(0, val[3].replace("$", ""))

    def _prod_limpiar(self):
        self.txt_prod_id.delete(0, tk.END)
        self.txt_prod_nom.delete(0, tk.END)
        self.txt_prod_cat.delete(0, tk.END)
        self.txt_prod_pre.delete(0, tk.END)

    def _prod_registrar(self):
        try:
            id_p = int(self.txt_prod_id.get().strip())
            nom = self.txt_prod_nom.get().strip()
            cat = self.txt_prod_cat.get().strip()
            pre = float(self.txt_prod_pre.get().strip())
        except ValueError:
            messagebox.showwarning("Datos Inválidos", "Revise el ID y precio ingresados.")
            return

        ok, msg = self.servicio.registrar_producto(id_p, nom, cat, pre)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_tabla_productos()
            self._cargar_combos_ventas()
            self._prod_limpiar()
        else:
            messagebox.showerror("Error", msg)

    def _prod_actualizar(self):
        try:
            id_p = int(self.txt_prod_id.get().strip())
            nom = self.txt_prod_nom.get().strip()
            cat = self.txt_prod_cat.get().strip()
            pre = float(self.txt_prod_pre.get().strip())
        except ValueError:
            messagebox.showwarning("Datos Inválidos", "Revise los campos del formulario.")
            return

        ok, msg = self.servicio.actualizar_producto(id_p, nom, cat, pre)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_tabla_productos()
            self._cargar_combos_ventas()
            self._prod_limpiar()
        else:
            messagebox.showerror("Error", msg)

    def _prod_eliminar(self):
        try:
            id_p = int(self.txt_prod_id.get().strip())
        except ValueError:
            messagebox.showwarning("Atención", "Ingrese el ID del producto a eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el producto #{id_p}?"):
            ok, msg = self.servicio.eliminar_producto(id_p)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self._cargar_tabla_productos()
                self._cargar_combos_ventas()
                self._prod_limpiar()
            else:
                messagebox.showerror("Error", msg)

    # =========================================================================
    # SECCIÓN 3: USUARIOS (CRUD con eventos - Semana 16)
    # =========================================================================
    def _construir_seccion_usuarios(self):
        if not self.servicio.es_administrador(self.usuario_actual):
            panel_restringido = tk.LabelFrame(
                self.tab_usuarios,
                text=" Gestión de Usuarios ",
                font=("Helvetica", 10, "bold"),
                bg="#FFFFFF",
                fg="#0F172A",
                bd=1,
                padx=20,
                pady=20
            )
            panel_restringido.pack(fill="both", expand=True, padx=15, pady=15)

            tk.Label(
                panel_restringido,
                text="Acceso restringido",
                font=("Helvetica", 14, "bold"),
                bg="#FFFFFF",
                fg="#DC2626"
            ).pack(pady=(80, 8))
            tk.Label(
                panel_restringido,
                text="La administración de usuarios está disponible únicamente para el rol Administrador.",
                font=("Helvetica", 10),
                bg="#FFFFFF",
                fg="#334155"
            ).pack()
            return

        self.roles_usuario = list(self.servicio.ROLES_VALIDOS)
        self.usuario_seleccionado_id = None

        f_form = tk.LabelFrame(
            self.tab_usuarios,
            text=" Gestión de Usuarios ",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#0F172A",
            bd=1,
            padx=15,
            pady=10
        )
        f_form.pack(fill="x", padx=15, pady=(15, 10))

        tk.Label(f_form, text="ID:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.txt_usuario_id = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=12)
        self.txt_usuario_id.grid(row=1, column=0, sticky="w", padx=5, pady=(0, 8))

        tk.Label(f_form, text="Nombre de Usuario:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.txt_usuario_nombre = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=26)
        self.txt_usuario_nombre.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 8))

        tk.Label(f_form, text="Contraseña:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.txt_usuario_password = tk.Entry(f_form, font=("Helvetica", 10), bg="#F8FAFC", relief="solid", bd=1, width=22, show="*")
        self.txt_usuario_password.grid(row=1, column=2, sticky="w", padx=5, pady=(0, 8))

        tk.Label(f_form, text="Rol:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=3, sticky="w", padx=5, pady=4)
        self.cbo_usuario_rol = ttk.Combobox(f_form, state="readonly", font=("Helvetica", 10), width=18, values=self.roles_usuario)
        self.cbo_usuario_rol.grid(row=1, column=3, sticky="w", padx=5, pady=(0, 8))
        self.cbo_usuario_rol.bind("<<ComboboxSelected>>", self._usuario_rol_seleccionado)

        self.txt_usuario_id.bind("<Return>", self._usuario_on_return)
        self.txt_usuario_nombre.bind("<Return>", self._usuario_on_return)
        self.txt_usuario_password.bind("<Return>", self._usuario_on_return)
        self.cbo_usuario_rol.bind("<Return>", self._usuario_on_return)

        self.txt_usuario_id.bind("<Escape>", self._usuario_on_escape)
        self.txt_usuario_nombre.bind("<Escape>", self._usuario_on_escape)
        self.txt_usuario_password.bind("<Escape>", self._usuario_on_escape)
        self.cbo_usuario_rol.bind("<Escape>", self._usuario_on_escape)

        f_btns = tk.Frame(f_form, bg="#FFFFFF")
        f_btns.grid(row=2, column=0, columnspan=4, pady=8, sticky="w")

        tk.Button(f_btns, text="Registrar", font=("Helvetica", 9, "bold"), bg="#2563EB", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._usuario_registrar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Actualizar", font=("Helvetica", 9, "bold"), bg="#D97706", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._usuario_actualizar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Eliminar", font=("Helvetica", 9, "bold"), bg="#DC2626", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._usuario_eliminar).pack(side="left", padx=4)
        tk.Button(f_btns, text="Limpiar", font=("Helvetica", 9, "bold"), bg="#475569", fg="#FFFFFF",
                  relief="flat", cursor="hand2", padx=10, pady=4, command=self._usuario_limpiar).pack(side="left", padx=4)

        self.lbl_usuario_estado = tk.Label(
            f_form,
            text="",
            font=("Helvetica", 9, "italic"),
            bg="#FFFFFF",
            fg="#64748B"
        )
        self.lbl_usuario_estado.grid(row=3, column=0, columnspan=4, sticky="w", padx=5)

        f_usuarios = tk.LabelFrame(self.tab_usuarios, text=" Usuarios Registrados ",
                                   font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#0F172A", bd=1, padx=10, pady=10)
        f_usuarios.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columnas = ("id", "username", "rol")
        self.tabla_usuarios = ttk.Treeview(f_usuarios, columns=columnas, show="headings", style="Custom.Treeview")
        self.tabla_usuarios.heading("id", text="ID")
        self.tabla_usuarios.heading("username", text="Nombre de Usuario")
        self.tabla_usuarios.heading("rol", text="Rol asignado")

        self.tabla_usuarios.column("id", width=80, anchor="center")
        self.tabla_usuarios.column("username", width=220, anchor="w")
        self.tabla_usuarios.column("rol", width=200, anchor="center")

        scroll_v = ttk.Scrollbar(f_usuarios, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scroll_v.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scroll_v.pack(side="right", fill="y")
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self._usuario_seleccionar_fila)

        self._cargar_tabla_usuarios()

    def _cargar_tabla_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for u in self.servicio.obtener_usuarios():
            self.tabla_usuarios.insert("", "end", iid=str(u.id_usuario), values=(u.id_usuario, u.username, u.rol))

    def _obtener_datos_form_usuario(self):
        try:
            id_usuario = int(self.txt_usuario_id.get().strip())
        except ValueError:
            messagebox.showwarning("Datos Inválidos", "El ID del usuario debe ser numérico.")
            return None

        return (
            id_usuario,
            self.txt_usuario_nombre.get().strip(),
            self.txt_usuario_password.get().strip(),
            self.cbo_usuario_rol.get().strip()
        )

    def _usuario_registrar(self):
        datos = self._obtener_datos_form_usuario()
        if datos is None:
            return

        ok, msg = self.servicio.registrar_usuario(*datos)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_tabla_usuarios()
            self._cargar_combos_ventas()
            self._usuario_limpiar()
        else:
            messagebox.showerror("Error", msg)

    def _usuario_actualizar(self):
        datos = self._obtener_datos_form_usuario()
        if datos is None:
            return

        ok, msg = self.servicio.actualizar_usuario(*datos)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_tabla_usuarios()
            self._cargar_combos_ventas()
            self._usuario_limpiar()
        else:
            messagebox.showerror("Error", msg)

    def _usuario_eliminar(self):
        datos = self._obtener_datos_form_usuario()
        if datos is None:
            return

        id_usuario = datos[0]
        usuario = self.servicio.buscar_usuario_por_id(id_usuario)
        if usuario is None:
            messagebox.showwarning("Atención", f"No se encontró el usuario con ID {id_usuario}.")
            return

        if id_usuario == self.usuario_actual.id_usuario:
            messagebox.showwarning(
                "Operación no permitida",
                "No puede eliminar su propia cuenta desde esta pantalla."
            )
            return

        if not messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar el usuario '{usuario.username}'?"):
            return

        ok, msg = self.servicio.eliminar_usuario(id_usuario)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_tabla_usuarios()
            self._cargar_combos_ventas()
            self._usuario_limpiar()
        else:
            messagebox.showerror("Error", msg)

    def _usuario_limpiar(self):
        self.usuario_seleccionado_id = None
        self.txt_usuario_id.config(state="normal")
        self.txt_usuario_id.delete(0, tk.END)
        self.txt_usuario_nombre.delete(0, tk.END)
        self.txt_usuario_password.delete(0, tk.END)
        self.cbo_usuario_rol.set("")
        self.lbl_usuario_estado.config(text="")

        for item in self.tabla_usuarios.selection():
            self.tabla_usuarios.selection_remove(item)
        self.txt_usuario_id.focus_set()

    def _usuario_seleccionar_fila(self, event):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        try:
            id_usuario = int(seleccion[0])
        except ValueError:
            valores = self.tabla_usuarios.item(seleccion[0], "values")
            id_usuario = int(valores[0])

        usuario = self.servicio.buscar_usuario_por_id(id_usuario)
        if usuario is None:
            messagebox.showwarning("Atención", "El usuario seleccionado ya no existe.")
            self._usuario_limpiar()
            return

        self.usuario_seleccionado_id = usuario.id_usuario
        self.txt_usuario_id.config(state="normal")
        self.txt_usuario_id.delete(0, tk.END)
        self.txt_usuario_id.insert(0, str(usuario.id_usuario))
        self.txt_usuario_nombre.delete(0, tk.END)
        self.txt_usuario_nombre.insert(0, usuario.username)
        self.txt_usuario_password.delete(0, tk.END)
        self.txt_usuario_password.insert(0, usuario.password)

        rol_form = "Empleado" if usuario.rol == "Mesero" else usuario.rol
        self.cbo_usuario_rol.set(rol_form if rol_form in self.roles_usuario else "")
        self.lbl_usuario_estado.config(text=f"Usuario seleccionado: {usuario.username}")

    def _usuario_on_return(self, event):
        self._usuario_registrar()

    def _usuario_on_escape(self, event):
        self._usuario_limpiar()

    def _usuario_rol_seleccionado(self, event):
        rol = self.cbo_usuario_rol.get()
        self.lbl_usuario_estado.config(text=f"Rol seleccionado: {rol}")
