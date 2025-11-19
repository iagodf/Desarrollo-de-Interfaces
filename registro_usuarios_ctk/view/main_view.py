import customtkinter as ctk


class MainView:
    """Ventana principal de la aplicación."""

    def __init__(self, master):
        """
        Crea la interfaz principal.

        Args:
            master: La ventana raíz de CTk
        """
        self.master = master

        # Configurar el layout principal con grid (2 columnas)
        master.grid_columnconfigure(0, weight=1)  # Columna izquierda (lista)
        master.grid_columnconfigure(1, weight=2)  # Columna derecha (detalles)
        master.grid_rowconfigure(0, weight=1)

        # --- PANEL IZQUIERDO: Lista de usuarios ---
        self.frame_izquierdo = ctk.CTkFrame(master)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Título de la lista
        self.titulo_lista = ctk.CTkLabel(
            self.frame_izquierdo,
            text="Lista de Usuarios",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.titulo_lista.pack(pady=10)

        # Frame scrollable para la lista de usuarios
        self.lista_usuarios_scrollable = ctk.CTkScrollableFrame(
            self.frame_izquierdo,
            width=200,
            height=400
        )
        self.lista_usuarios_scrollable.pack(padx=10, pady=10, fill="both", expand=True)

        # --- PANEL DERECHO: Detalles del usuario seleccionado ---
        self.frame_derecho = ctk.CTkFrame(master)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Título del panel de detalles
        self.titulo_detalles = ctk.CTkLabel(
            self.frame_derecho,
            text="Detalles del Usuario",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.titulo_detalles.pack(pady=10)

        # Etiquetas para mostrar los datos
        self.label_nombre = ctk.CTkLabel(
            self.frame_derecho,
            text="Nombre: -",
            font=ctk.CTkFont(size=14)
        )
        self.label_nombre.pack(pady=5, anchor="w", padx=20)

        self.label_edad = ctk.CTkLabel(
            self.frame_derecho,
            text="Edad: -",
            font=ctk.CTkFont(size=14)
        )
        self.label_edad.pack(pady=5, anchor="w", padx=20)

        self.label_genero = ctk.CTkLabel(
            self.frame_derecho,
            text="Género: -",
            font=ctk.CTkFont(size=14)
        )
        self.label_genero.pack(pady=5, anchor="w", padx=20)

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback):
        """
        Actualiza la lista de usuarios mostrada.

        Args:
            usuarios (list): Lista de objetos Usuario
            on_seleccionar_callback (function): Función a llamar cuando se seleccione un usuario
        """
        # Limpiar la lista actual
        for widget in self.lista_usuarios_scrollable.winfo_children():
            widget.destroy()

        # Crear un botón por cada usuario
        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                # Lambda captura el índice 'i' y lo pasa al callback
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario):
        """
        Actualiza el panel de detalles con los datos del usuario.

        Args:
            usuario (Usuario): El objeto usuario a mostrar
        """
        if usuario:
            self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
            self.label_edad.configure(text=f"Edad: {usuario.edad}")
            self.label_genero.configure(text=f"Género: {usuario.genero}")
        else:
            self.label_nombre.configure(text="Nombre: -")
            self.label_edad.configure(text="Edad: -")
            self.label_genero.configure(text="Género: -")