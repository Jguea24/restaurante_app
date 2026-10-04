import os
import json

class ArchivoServicio:
    """Clase utilitaria para persistencia en archivos JSON."""
    
    @staticmethod
    def leer_json(ruta: str) -> list:
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def guardar_json(ruta: str, datos: list) -> bool:
        try:
            carpeta = os.path.dirname(ruta)
            if carpeta:
                os.makedirs(carpeta, exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False