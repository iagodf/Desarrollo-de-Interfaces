# view/main_view.py
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path


class MainView:
    """Ventana principal de la aplicación."""

    def __init__(self, master):
        self.master = master

        # Configurar el layout principal con grid (2 columnas)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=2)
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

        # Botón para añadir usuario
        self.btn_añadir = ctk.CTkButton(
            self.frame_izquierdo,
            text="+ Añadir Usuario",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_añadir.pack(pady=5, padx=10, fill="x")

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

        # Label para el avatar
        self.avatar_label = ctk.CTkLabel(
            self.frame_derecho,
            text="",  # Sin texto, solo imagen
            width=150,
            height=150
        )
        self.avatar_label.pack(pady=10)

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
        """Actualiza la lista de usuarios mostrada."""
        # Limpiar la lista actual
        for widget in self.lista_usuarios_scrollable.winfo_children():
            widget.destroy()

        # Crear un botón por cada usuario
        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                command=lambda idx=i: on_seleccionar_callback(idx)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario, avatar_image=None):
        """
        Actualiza el panel de detalles con los datos del usuario.

        Args:
            usuario (Usuario): El objeto usuario a mostrar
            avatar_image (CTkImage): La imagen del avatar (opcional)
        """
        if usuario:
            self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
            self.label_edad.configure(text=f"Edad: {usuario.edad}")
            self.label_genero.configure(text=f"Género: {usuario.genero}")

            # Mostrar el avatar si existe
            if avatar_image:
                self.avatar_label.configure(image=avatar_image)
            else:
                self.avatar_label.configure(image="")
        else:
            self.label_nombre.configure(text="Nombre: -")
            self.label_edad.configure(text="Edad: -")
            self.label_genero.configure(text="Género: -")
            self.avatar_label.configure(image="")


class AddUserView:
    """Ventana modal para añadir un nuevo usuario."""

    def __init__(self, master):
        """
        Crea la ventana modal de añadir usuario.

        Args:
            master: La ventana padre
        """
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario")
        self.window.geometry("350x450")
        self.window.grab_set()  # Hace la ventana modal

        # Variable para guardar la ruta del avatar seleccionado
        self.avatar_path = None

        # --- Título ---
        titulo = ctk.CTkLabel(
            self.window,
            text="Nuevo Usuario",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.pack(pady=15)

        # --- Campo Nombre ---
        ctk.CTkLabel(self.window, text="Nombre:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(
            self.window,
            placeholder_text="Introduce el nombre",
            width=280
        )
        self.nombre_entry.pack(pady=5)

        # --- Campo Edad ---
        ctk.CTkLabel(self.window, text="Edad:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        self.edad_entry = ctk.CTkEntry(
            self.window,
            placeholder_text="Introduce la edad",
            width=280
        )
        self.edad_entry.pack(pady=5)

        # --- Campo Género ---
        ctk.CTkLabel(self.window, text="Género:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        self.genero_var = ctk.StringVar(value="Masculino")
        self.genero_menu = ctk.CTkOptionMenu(
            self.window,
            values=["Masculino", "Femenino", "Otro"],
            variable=self.genero_var,
            width=280
        )
        self.genero_menu.pack(pady=5)

        # --- Selección de Avatar ---
        ctk.CTkLabel(self.window, text="Avatar:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))

        self.avatar_button = ctk.CTkButton(
            self.window,
            text="Seleccionar Imagen",
            command=self.seleccionar_avatar,
            width=280
        )
        self.avatar_button.pack(pady=5)

        self.avatar_label = ctk.CTkLabel(
            self.window,
            text="No se ha seleccionado imagen",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.avatar_label.pack(pady=5)

        # --- Botones de acción ---
        frame_botones = ctk.CTkFrame(self.window, fg_color="transparent")
        frame_botones.pack(pady=20)

        self.guardar_button = ctk.CTkButton(
            frame_botones,
            text="Guardar",
            width=130,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.guardar_button.pack(side="left", padx=5)

        cancelar_button = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            width=130,
            command=self.window.destroy,
            fg_color="gray",
            hover_color="darkgray"
        )
        cancelar_button.pack(side="left", padx=5)

    def seleccionar_avatar(self):
        """Abre un diálogo para seleccionar la imagen del avatar."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen de avatar",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.avatar_path = ruta
            # Mostrar solo el nombre del archivo
            nombre_archivo = Path(ruta).name
            self.avatar_label.configure(
                text=f"Seleccionado: {nombre_archivo}",
                text_color="green"
            )

    def get_data(self):
        """
        Recoge y devuelve los datos del formulario.

        Returns:
            dict: Diccionario con los datos del formulario
        """
        return {
            "nombre": self.nombre_entry.get().strip(),
            "edad": self.edad_entry.get().strip(),
            "genero": self.genero_var.get(),
            "avatar": self.avatar_path
        }