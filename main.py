import os
import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class AppRestaurante:
    """Clase controladora principal de la aplicación."""
    def __init__(self, root):
        self.root = root
        self.servicio = RestauranteServicio()
        self.vista_actual = None
        
        # Asignar ícono institucional si está disponible
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "icono.png")
        if os.path.exists(icon_path):
            try:
                img_ico = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, img_ico)
            except Exception:
                pass
        
        self.mostrar_login()

    def limpiar_vista_actual(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def mostrar_login(self):
        self.limpiar_vista_actual()
        self.vista_actual = LoginView(
            master=self.root,
            servicio=self.servicio,
            on_login_success=self.iniciar_sesion_exitosa
        )

    def iniciar_sesion_exitosa(self, usuario):
        self.limpiar_vista_actual()
        self.vista_actual = MainView(
            master=self.root,
            usuario_actual=usuario,
            servicio=self.servicio,
            on_logout=self.mostrar_login
        )

def main():
    root = tk.Tk()
    app = AppRestaurante(root)
    root.mainloop()

if __name__ == "__main__":
    main()
