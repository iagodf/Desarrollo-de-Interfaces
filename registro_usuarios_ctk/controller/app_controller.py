# controller/app_controller.py
from pathlib import Path
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk

from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView, AddUserView


class AppController:
    """Controlador principal de la aplicación."""

    def __init__(self, master):
        """Inicializa el controlador, crea el modelo y la vista, y los conecta."""
        self.master = master

        # Configurar rutas del proyecto
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.CSV_FILE = self.BASE_DIR / "usuarios.csv"

        # Cache de imágenes para evitar que se eliminen por el garbage collector
        self.avatar_images = {}

        # Crear el modelo (la lógica de negocio)
        self.gestor = GestorUsuarios()

        # Crear la vista (la interfaz gráfica)
        self.view = MainView(master)

        # Conectar el botón de añadir usuario
        self.view.btn_añadir.configure(command=self.abrir_ventana_añadir)

        # Conectar las opciones del menú
        self.view.menu_archivo.add_command(
            label="Guardar",
            command=self.guardar_usuarios
        )
        self.view.menu_archivo.add_command(
            label="Cargar",
            command=self.cargar_usuarios
        )
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(
            label="Salir",
            command=master.quit
        )

        # Intentar cargar datos existentes al iniciar
        self.cargar_usuarios()

        # Si no había datos, mostrar la lista de ejemplo
        if not self.gestor.listar():
            self.gestor._cargar_datos_de_ejemplo()

        # Poblar la lista inicial
        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        """Obtiene los usuarios del modelo y actualiza la vista."""
        usuarios = self.gestor.listar()
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice):
        """Callback que se ejecuta cuando el usuario hace clic en un nombre."""
        usuario = self.gestor.obtener_por_indice(indice)

        # Cargar la imagen del avatar si existe
        avatar_image = None
        if usuario and usuario.avatar:
            avatar_image = self._cargar_imagen_avatar(usuario.avatar, indice)

        # Mostrar los detalles
        self.view.mostrar_detalles_usuario(usuario, avatar_image)

    def _cargar_imagen_avatar(self, ruta_avatar, indice):
        """Carga una imagen de avatar y la guarda en cache."""
        try:
            ruta = Path(ruta_avatar)

            # Si no es ruta absoluta, buscar en assets
            if not ruta.is_absolute():
                ruta = self.ASSETS_PATH / ruta_avatar

            if ruta.exists():
                # Cargar y guardar en cache
                img = Image.open(ruta)
                ctk_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(150, 150)
                )
                self.avatar_images[indice] = ctk_image
                return ctk_image
        except Exception as e:
            print(f"Error al cargar avatar: {e}")

        return None

    def abrir_ventana_añadir(self):
        """Abre la ventana modal para añadir un nuevo usuario."""
        add_view = AddUserView(self.master)
        add_view.guardar_button.configure(
            command=lambda: self.añadir_usuario(add_view)
        )

    def añadir_usuario(self, add_view):
        """Procesa los datos del formulario y añade el usuario."""
        datos = add_view.get_data()

        # Validar nombre
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        # Validar edad
        try:
            edad = int(datos["edad"])
            if edad <= 0 or edad > 150:
                raise ValueError("Edad fuera de rango")
        except ValueError:
            messagebox.showerror(
                "Error",
                "La edad debe ser un número válido entre 1 y 150"
            )
            return

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombre=datos["nombre"],
            edad=edad,
            genero=datos["genero"],
            avatar=datos["avatar"]
        )

        # Añadir al modelo
        self.gestor.añadir(nuevo_usuario)

        # Refrescar la lista
        self.refrescar_lista_usuarios()

        # Cerrar la ventana modal
        add_view.window.destroy()

        # Mensaje de confirmación
        messagebox.showinfo(
            "Éxito",
            f"Usuario '{datos['nombre']}' añadido correctamente"
        )

    def guardar_usuarios(self):
        """Guarda la lista de usuarios en un archivo CSV."""
        try:
            self.gestor.guardar_csv(self.CSV_FILE)
            messagebox.showinfo(
                "Éxito",
                f"Usuarios guardados correctamente en:\n{self.CSV_FILE.name}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudieron guardar los usuarios:\n{str(e)}"
            )

    def cargar_usuarios(self):
        """Carga la lista de usuarios desde un archivo CSV."""
        try:
            self.gestor.cargar_csv(self.CSV_FILE)
            self.refrescar_lista_usuarios()
            messagebox.showinfo(
                "Éxito",
                f"Usuarios cargados correctamente desde:\n{self.CSV_FILE.name}"
            )
        except FileNotFoundError:
            # No mostrar error si es la primera vez (no existe el archivo)
            print(f"Archivo {self.CSV_FILE.name} no encontrado. Se usarán datos de ejemplo.")
        except Exception as e:
            messagebox.showerror(
                "Error al cargar",
                f"No se pudieron cargar los usuarios:\n{str(e)}"
            )