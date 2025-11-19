import customtkinter as ctk
import tkinter
from tkinter import filedialog
from pathlib import Path


class MainView:
    def __init__(self, master):
        self.master = master

        # Variables para búsqueda y filtro
        self.busqueda_var = ctk.StringVar()
        self.filtro_genero_var = ctk.StringVar(value="Todos")

        # Crear menú
        self.menubar = tkinter.Menu(master)
        master.config(menu=self.menubar)

        self.menu_archivo = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)

        # Layout principal
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=2)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)

        # --- PANEL IZQUIERDO ---
        self.frame_izquierdo = ctk.CTkFrame(master)
        self.frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.titulo_lista = ctk.CTkLabel(
            self.frame_izquierdo,
            text="Lista de Usuarios",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.titulo_lista.pack(pady=10)

        # Campo de búsqueda
        self.busqueda_entry = ctk.CTkEntry(
            self.frame_izquierdo,
            placeholder_text="Buscar por nombre...",
            textvariable=self.busqueda_var,
            width=250
        )
        self.busqueda_entry.pack(pady=5, padx=10, fill="x")

        # Filtro por género
        self.filtro_genero = ctk.CTkOptionMenu(
            self.frame_izquierdo,
            values=["Todos", "Masculino", "Femenino", "Otro"],
            variable=self.filtro_genero_var,
            width=250
        )
        self.filtro_genero.pack(pady=5, padx=10, fill="x")

        # Botón añadir
        self.btn_añadir = ctk.CTkButton(
            self.frame_izquierdo,
            text="+ Añadir Usuario",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_añadir.pack(pady=5, padx=10, fill="x")

        # Lista scrollable
        self.lista_usuarios_scrollable = ctk.CTkScrollableFrame(
            self.frame_izquierdo,
            width=200,
            height=300
        )
        self.lista_usuarios_scrollable.pack(padx=10, pady=10, fill="both", expand=True)

        # --- PANEL DERECHO ---
        self.frame_derecho = ctk.CTkFrame(master)
        self.frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.titulo_detalles = ctk.CTkLabel(
            self.frame_derecho,
            text="Detalles del Usuario",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.titulo_detalles.pack(pady=10)

        self.avatar_label = ctk.CTkLabel(
            self.frame_derecho,
            text="",
            width=150,
            height=150
        )
        self.avatar_label.pack(pady=10)

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

        # Botones de acción
        frame_botones = ctk.CTkFrame(self.frame_derecho, fg_color="transparent")
        frame_botones.pack(pady=20)

        self.btn_editar = ctk.CTkButton(
            frame_botones,
            text="✏️ Editar",
            width=120,
            state="disabled"
        )
        self.btn_editar.pack(side="left", padx=5)

        self.btn_eliminar = ctk.CTkButton(
            frame_botones,
            text="🗑️ Eliminar",
            width=120,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.btn_eliminar.pack(side="left", padx=5)

        # --- BARRA DE ESTADO ---
        self.barra_estado = ctk.CTkLabel(
            master,
            text="Listo",
            font=ctk.CTkFont(size=11),
            anchor="w",
            fg_color=("gray85", "gray25"),
            height=25
        )
        self.barra_estado.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

    def actualizar_lista_usuarios(self, usuarios, on_seleccionar_callback, on_doble_clic_callback=None):
        for widget in self.lista_usuarios_scrollable.winfo_children():
            widget.destroy()

        for i, usuario in enumerate(usuarios):
            btn = ctk.CTkButton(
                self.lista_usuarios_scrollable,
                text=usuario.nombre,
                command=lambda idx=i: on_seleccionar_callback(idx)
            )

            if on_doble_clic_callback:
                btn.bind("<Double-Button-1>", lambda e, idx=i: on_doble_clic_callback(idx))

            btn.pack(fill="x", padx=5, pady=2)

    def mostrar_detalles_usuario(self, usuario, avatar_image=None):
        if usuario:
            self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
            self.label_edad.configure(text=f"Edad: {usuario.edad}")
            self.label_genero.configure(text=f"Género: {usuario.genero}")

            if avatar_image:
                self.avatar_label.configure(image=avatar_image)
            else:
                self.avatar_label.configure(image="")

            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
        else:
            self.label_nombre.configure(text="Nombre: -")
            self.label_edad.configure(text="Edad: -")
            self.label_genero.configure(text="Género: -")
            self.avatar_label.configure(image="")
            self.btn_editar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")

    def actualizar_barra_estado(self, mensaje):
        self.barra_estado.configure(text=mensaje)


class AddUserView:
    def __init__(self, master, usuario_existente=None):
        self.window = ctk.CTkToplevel(master)

        if usuario_existente:
            self.window.title("Editar Usuario")
        else:
            self.window.title("Añadir Nuevo Usuario")

        self.window.geometry("350x450")
        self.window.grab_set()

        self.avatar_path = usuario_existente.avatar if usuario_existente else None

        titulo = ctk.CTkLabel(
            self.window,
            text="Editar Usuario" if usuario_existente else "Nuevo Usuario",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.pack(pady=15)

        # Campo Nombre
        ctk.CTkLabel(self.window, text="Nombre:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(
            self.window,
            placeholder_text="Introduce el nombre",
            width=280
        )
        self.nombre_entry.pack(pady=5)
        if usuario_existente:
            self.nombre_entry.insert(0, usuario_existente.nombre)

        # Campo Edad
        ctk.CTkLabel(self.window, text="Edad:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        self.edad_entry = ctk.CTkEntry(
            self.window,
            placeholder_text="Introduce la edad",
            width=280
        )
        self.edad_entry.pack(pady=5)
        if usuario_existente:
            self.edad_entry.insert(0, str(usuario_existente.edad))

        # Campo Género
        ctk.CTkLabel(self.window, text="Género:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))
        valor_inicial = usuario_existente.genero if usuario_existente else "Masculino"
        self.genero_var = ctk.StringVar(value=valor_inicial)
        self.genero_menu = ctk.CTkOptionMenu(
            self.window,
            values=["Masculino", "Femenino", "Otro"],
            variable=self.genero_var,
            width=280
        )
        self.genero_menu.pack(pady=5)

        # Avatar
        ctk.CTkLabel(self.window, text="Avatar:", font=ctk.CTkFont(size=13)).pack(pady=(10, 0))

        self.avatar_button = ctk.CTkButton(
            self.window,
            text="Seleccionar Imagen",
            command=self.seleccionar_avatar,
            width=280
        )
        self.avatar_button.pack(pady=5)

        texto_avatar = "No se ha seleccionado imagen"
        if usuario_existente and usuario_existente.avatar:
            texto_avatar = f"Actual: {Path(usuario_existente.avatar).name}"

        self.avatar_label = ctk.CTkLabel(
            self.window,
            text=texto_avatar,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.avatar_label.pack(pady=5)

        # Botones
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
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen de avatar",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.avatar_path = ruta
            nombre_archivo = Path(ruta).name
            self.avatar_label.configure(
                text=f"Seleccionado: {nombre_archivo}",
                text_color="green"
            )

    def get_data(self):
        return {
            "nombre": self.nombre_entry.get().strip(),
            "edad": self.edad_entry.get().strip(),
            "genero": self.genero_var.get(),
            "avatar": self.avatar_path
        }