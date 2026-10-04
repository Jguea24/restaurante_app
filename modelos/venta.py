from datetime import datetime

class Venta:
    """Modelo que representa una transacción de venta en el restaurante.
    Relaciona un usuario (mesero/vendedor), un producto y la fecha de la operación.
    """
    def __init__(self, id_venta: int, id_usuario: int, nombre_usuario: str, 
                 id_producto: int, nombre_producto: str, total: float, fecha: str = None):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.total = float(total)
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id_venta": self.id_venta,
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "total": self.total,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_venta=int(data.get("id_venta", 0)),
            id_usuario=int(data.get("id_usuario", 0)),
            nombre_usuario=str(data.get("nombre_usuario", "")),
            id_producto=int(data.get("id_producto", 0)),
            nombre_producto=str(data.get("nombre_producto", "")),
            total=float(data.get("total", 0.0)),
            fecha=str(data.get("fecha", ""))
        )