import os
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """Servicio central que gestiona la lógica de negocio y coordina con persistencia."""
    ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")
    ROLES_COMPATIBLES = ROLES_VALIDOS + ("Mesero",)
    
    def __init__(self, ruta_base: str = None):
        if ruta_base is None:
            # Localizar carpeta datos relativa al script
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_base = os.path.join(base_dir, "datos")
        
        self.ruta_usuarios = os.path.join(ruta_base, "usuarios.json")
        self.ruta_productos = os.path.join(ruta_base, "productos.json")
        self.ruta_ventas = os.path.join(ruta_base, "ventas.json")

    # --- Métodos de Usuarios ---
    def obtener_usuarios(self) -> list:
        datos = ArchivoServicio.leer_json(self.ruta_usuarios)
        return [Usuario.from_dict(item) for item in datos]

    def validar_usuario(self, username: str, password: str):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.username == username.strip() and u.password == password.strip():
                return u
        return None

    def es_administrador(self, usuario: Usuario) -> bool:
        return usuario is not None and usuario.rol == "Administrador"

    def buscar_usuario_por_id(self, id_usuario: int):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.id_usuario == id_usuario:
                return u
        return None

    def buscar_usuario_por_username(self, username: str):
        username_limpio = username.strip().lower()
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.username.strip().lower() == username_limpio:
                return u
        return None

    def registrar_usuario(self, id_usuario: int, username: str, password: str, rol: str) -> tuple:
        ok, mensaje = self._validar_datos_usuario(id_usuario, username, password, rol)
        if not ok:
            return False, mensaje

        usuarios = self.obtener_usuarios()
        if any(u.id_usuario == id_usuario for u in usuarios):
            return False, f"Ya existe un usuario con el ID {id_usuario}."
        if any(u.username.strip().lower() == username.strip().lower() for u in usuarios):
            return False, f"Ya existe un usuario con el nombre '{username.strip()}'."

        usuarios.append(Usuario(id_usuario, username.strip(), password.strip(), rol.strip()))
        return self._guardar_usuarios(usuarios, "Usuario registrado correctamente.")

    def actualizar_usuario(self, id_usuario: int, username: str, password: str, rol: str) -> tuple:
        ok, mensaje = self._validar_datos_usuario(id_usuario, username, password, rol)
        if not ok:
            return False, mensaje

        usuarios = self.obtener_usuarios()
        encontrado = False
        username_limpio = username.strip().lower()

        for u in usuarios:
            if u.id_usuario != id_usuario and u.username.strip().lower() == username_limpio:
                return False, f"Ya existe otro usuario con el nombre '{username.strip()}'."

        for indice, usuario in enumerate(usuarios):
            if usuario.id_usuario == id_usuario:
                usuarios[indice] = Usuario(id_usuario, username.strip(), password.strip(), rol.strip())
                encontrado = True
                break

        if not encontrado:
            return False, f"No se encontró el usuario con ID {id_usuario}."

        return self._guardar_usuarios(usuarios, "Usuario actualizado correctamente.")

    def eliminar_usuario(self, id_usuario: int) -> tuple:
        usuarios = self.obtener_usuarios()
        inicial = len(usuarios)
        usuarios = [u for u in usuarios if u.id_usuario != id_usuario]

        if len(usuarios) == inicial:
            return False, f"No se encontró el usuario con ID {id_usuario}."

        return self._guardar_usuarios(usuarios, "Usuario eliminado correctamente.")

    def _validar_datos_usuario(self, id_usuario: int, username: str, password: str, rol: str) -> tuple:
        if id_usuario <= 0:
            return False, "El ID del usuario debe ser un número mayor a cero."
        if not username.strip():
            return False, "El nombre de usuario es obligatorio."
        if not password.strip():
            return False, "La contraseña es obligatoria."
        if rol.strip() not in self.ROLES_VALIDOS:
            return False, "Debe seleccionar un rol válido: Administrador, Empleado o Cliente."
        return True, ""

    def _guardar_usuarios(self, usuarios: list, mensaje_exito: str) -> tuple:
        datos = [u.to_dict() for u in usuarios]
        if ArchivoServicio.guardar_json(self.ruta_usuarios, datos):
            return True, mensaje_exito
        return False, "Error al guardar los cambios de usuarios en el archivo JSON."

    # --- Métodos de Productos ---
    def obtener_productos(self) -> list:
        datos = ArchivoServicio.leer_json(self.ruta_productos)
        return [Producto.from_dict(item) for item in datos]

    def buscar_producto_por_id(self, id_producto: int):
        productos = self.obtener_productos()
        for p in productos:
            if p.id_producto == id_producto:
                return p
        return None

    def registrar_producto(self, id_producto: int, nombre: str, categoria: str, precio: float) -> tuple:
        if not nombre.strip():
            return False, "El nombre del producto no puede estar vacío."
        if precio <= 0:
            return False, "El precio debe ser mayor a cero."
        
        productos = self.obtener_productos()
        for p in productos:
            if p.id_producto == id_producto:
                return False, f"Ya existe un producto con el ID {id_producto}."

        nuevo = Producto(id_producto, nombre.strip(), categoria.strip(), precio)
        productos.append(nuevo)
        datos = [p.to_dict() for p in productos]
        if ArchivoServicio.guardar_json(self.ruta_productos, datos):
            return True, "Producto registrado correctamente."
        return False, "Error al guardar el producto en el archivo."

    def actualizar_producto(self, id_producto: int, nombre: str, categoria: str, precio: float) -> tuple:
        if not nombre.strip():
            return False, "El nombre del producto no puede estar vacío."
        if precio <= 0:
            return False, "El precio debe ser mayor a cero."

        productos = self.obtener_productos()
        encontrado = False
        for i, p in enumerate(productos):
            if p.id_producto == id_producto:
                productos[i] = Producto(id_producto, nombre.strip(), categoria.strip(), precio)
                encontrado = True
                break

        if not encontrado:
            return False, f"No se encontró el producto con ID {id_producto}."

        datos = [p.to_dict() for p in productos]
        if ArchivoServicio.guardar_json(self.ruta_productos, datos):
            return True, "Producto actualizado correctamente."
        return False, "Error al guardar los cambios del producto."

    def eliminar_producto(self, id_producto: int) -> tuple:
        productos = self.obtener_productos()
        inicial = len(productos)
        productos = [p for p in productos if p.id_producto != id_producto]
        
        if len(productos) == inicial:
            return False, f"No se encontró el producto con ID {id_producto}."

        datos = [p.to_dict() for p in productos]
        if ArchivoServicio.guardar_json(self.ruta_productos, datos):
            return True, "Producto eliminado correctamente."
        return False, "Error al eliminar el producto en persistencia."

    # --- Nuevos Métodos de Ventas (Semana 15) ---
    def obtener_ventas(self) -> list:
        datos = ArchivoServicio.leer_json(self.ruta_ventas)
        return [Venta.from_dict(item) for item in datos]

    def registrar_venta(self, id_usuario: int, id_producto: int) -> tuple:
        """Valida entidades y registra una nueva venta en el sistema."""
        usuario = self.buscar_usuario_por_id(id_usuario)
        if not usuario:
            return False, "El usuario seleccionado no existe o es inválido."

        producto = self.buscar_producto_por_id(id_producto)
        if not producto:
            return False, "El producto seleccionado no existe o es inválido."

        ventas = self.obtener_ventas()
        nuevo_id = max([v.id_venta for v in ventas], default=0) + 1

        nueva_venta = Venta(
            id_venta=nuevo_id,
            id_usuario=usuario.id_usuario,
            nombre_usuario=usuario.username,
            id_producto=producto.id_producto,
            nombre_producto=producto.nombre,
            total=producto.precio
        )

        ventas.append(nueva_venta)
        datos = [v.to_dict() for v in ventas]
        if ArchivoServicio.guardar_json(self.ruta_ventas, datos):
            return True, f"Venta #{nuevo_id} registrada con éxito (${producto.precio:.2f})."
        return False, "Error al persistir la venta en el archivo JSON."
