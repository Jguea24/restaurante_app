import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginView(tk.Frame):
    """Vista de autenticación de usuario con diseño estilizado y alto contraste visual."""
    
    def __init__(self, master, servicio, on_login_success):
        super().__init__(master, bg="#F1F5F9")
        self.master = master
        self.servicio = servicio
        self.on_login_success = on_login_success
        
        self.master.title("Restaurante App - Iniciar Sesión")
        self.master.geometry("420x520")
        self.master.resizable(False, False)
        self.master.configure(bg="#F1F5F9")
        
        self.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        # Tarjeta central con sombra simulada/borde sutil
        card = tk.Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=450)

        # 1. Logo institucional desde assets/
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
        logo_path = os.path.join(assets_dir, "logo.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path).resize((280, 70), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(img)
                lbl_logo = tk.Label(card, image=self.logo_tk, bg="#FFFFFF")
                lbl_logo.pack(pady=(20, 10))
            except Exception:
                lbl_alt = tk.Label(card, text="🍽️ RESTAURANTE APP", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0F172A")
                lbl_alt.pack(pady=(25, 10))
        else:
            lbl_alt = tk.Label(card, text="🍽️ RESTAURANTE APP", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0F172A")
            lbl_alt.pack(pady=(25, 10))

        # Título de bienvenida
        tk.Label(
            card,
            text="Control de Acceso",
            font=("Helvetica", 13, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        ).pack(pady=(0, 15))

        # Formulario
        form_frame = tk.Frame(card, bg="#FFFFFF")
        form_frame.pack(fill="x", padx=30)

        # Campo Usuario
        tk.Label(form_frame, text="Usuario:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(anchor="w")
        self.txt_usuario = tk.Entry(form_frame, font=("Helvetica", 11), bg="#F8FAFC", fg="#0F172A", relief="solid", bd=1)
        self.txt_usuario.pack(fill="x", pady=(4, 12), ipady=4)
        self.txt_usuario.focus()

        # Campo Contraseña
        tk.Label(form_frame, text="Contraseña:", font=("Helvetica", 9, "bold"), bg="#FFFFFF", fg="#334155").pack(anchor="w")
        self.txt_password = tk.Entry(form_frame, font=("Helvetica", 11), show="•", bg="#F8FAFC", fg="#0F172A", relief="solid", bd=1)
        self.txt_password.pack(fill="x", pady=(4, 20), ipady=4)
        self.txt_password.bind("<Return>", lambda event: self._intentar_login())

        # Botón Ingresar (Alto contraste: azul intenso con texto blanco)
        self.btn_ingresar = tk.Button(
            card,
            text="INGRESAR AL SISTEMA",
            font=("Helvetica", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            cursor="hand2",
            relief="flat",
            bd=0,
            command=self._intentar_login
        )
        self.btn_ingresar.pack(fill="x", padx=30, ipady=8, pady=(0, 10))

        # Nota de credenciales de prueba
        lbl_hint = tk.Label(
            card,
            text="Demo: admin / 123  |  mesero1 / 123",
            font=("Helvetica", 8, "italic"),
            bg="#FFFFFF",
            fg="#64748B"
        )
        lbl_hint.pack(side="bottom", pady=12)

    def _intentar_login(self):
        username = self.txt_usuario.get()
        password = self.txt_password.get()

        if not username or not password:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña.")
            return

        usuario = self.servicio.validar_usuario(username, password)
        if usuario:
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")