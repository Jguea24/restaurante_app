Restaurante App - Semana 16

Sistema de gestión para restaurante desarrollado en Python con Programación Orientada a Objetos, Tkinter/ttk y persistencia en archivos JSON.

## Descripción

`restaurante_app` conserva las funcionalidades existentes de login, gestión de productos, registro de ventas, historial de ventas, cierre de sesión y carga de recursos visuales desde `assets/`. La evolución de Semana 16 agrega una verdadera Gestión de Usuarios para el rol Administrador, sin reemplazar la arquitectura modular del proyecto.

## Objetivo de la Semana 16

Demostrar la organización modular de un sistema orientado a objetos en Python aplicando manejo de eventos en Tkinter a la gestión administrativa de usuarios.

La implementación evidencia:

- Uso de `ttk.Treeview` para consultar usuarios registrados.
- Uso de `ttk.Combobox` para seleccionar roles.
- Eventos con `bind()`: `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>`.
- Botones con `command=` para ejecutar callbacks de CRUD.
- Separación entre interfaz, servicio, modelos y persistencia JSON.

## Arquitectura del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── logo.png
│   └── icono.png
├── main.py
└── README.md
```

## Gestión de Usuarios

La pestaña **Gestión de Usuarios** está disponible únicamente para usuarios con rol **Administrador**. Los roles no administrativos visualizan un mensaje de acceso restringido.

El formulario permite administrar:

- ID
- Nombre de usuario
- Contraseña
- Rol

Roles permitidos para nuevos registros y actualizaciones:

- Administrador
- Empleado
- Cliente

Compatibilidad: los datos existentes con rol `Mesero` no se eliminan. Si un usuario `Mesero` se selecciona para edición, el formulario lo trata como `Empleado` para permitir una migración coherente sin pérdida de datos.

## CRUD de Usuarios

El Administrador puede:

- Registrar usuarios.
- Consultar usuarios en un `Treeview`.
- Seleccionar un usuario y cargarlo en el formulario.
- Actualizar nombre, contraseña y rol.
- Eliminar usuarios con confirmación.
- Limpiar formulario y selección.

La contraseña nunca se muestra en el `Treeview`; solo aparece en el formulario al seleccionar un usuario para edición.

Reglas principales:

- ID obligatorio, numérico y no duplicado.
- Nombre de usuario obligatorio y no duplicado.
- Contraseña obligatoria.
- Rol obligatorio y válido.
- El Administrador autenticado no puede eliminar su propia cuenta desde esta pantalla.

## Manejo de Eventos

Eventos implementados con `bind()`:

- `<<TreeviewSelect>>`: al seleccionar una fila, recupera el ID, consulta el usuario en `RestauranteServicio` y carga el formulario.
- `<Return>`: ejecuta el registro reutilizando el mismo callback de registrar usuario.
- `<Escape>`: limpia los campos, limpia la selección del `Treeview` y restaura el estado inicial del formulario.
- `<<ComboboxSelected>>`: responde al cambio de rol y actualiza el estado visual del formulario.

Botones implementados con `command=`:

- Registrar
- Actualizar
- Eliminar
- Limpiar

Esto permite demostrar la diferencia entre eventos enlazados con `bind()` y acciones directas de botones con `command=`.

## RestauranteServicio

`RestauranteServicio` concentra la lógica de negocio y persistencia:

- Validación de usuarios.
- Búsqueda por ID y nombre de usuario.
- Registro, actualización y eliminación de usuarios.
- Validación de roles.
- Protección contra duplicados.
- Guardado en `datos/usuarios.json`.

La interfaz `ui/main_view.py` no escribe directamente archivos JSON; delega las operaciones al servicio.

## Persistencia

La persistencia continúa usando JSON:

- Usuarios: `datos/usuarios.json`
- Productos: `datos/productos.json`
- Ventas: `datos/ventas.json`

Los cambios realizados desde Gestión de Usuarios se guardan en `usuarios.json` y se recuperan al cerrar y volver a ejecutar la aplicación.

## Assets

La aplicación mantiene los recursos visuales en `assets/`, incluyendo el logotipo usado en login y vista principal.

## Ejecución

Requisitos:

- Python 3.10 o superior.
- Tkinter incluido con Python.
- Pillow para carga de imágenes.

Instalar Pillow si hace falta:

```bash
pip install Pillow
```

Ejecutar:

```bash
python main.py
```

Credenciales de prueba existentes:

- Administrador: `admin` / `123`
- Usuario existente: `mesero1` / `123`

