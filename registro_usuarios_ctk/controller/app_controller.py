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

        self.master = master

        # Configurar rutas del proyecto
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"

        # Cache de imágenes para evitar que se eliminen por el garbage collector
        self.avatar_images = {}

        # Crear el modelo (la lógica de negocio)
        self.gestor = GestorUsuarios()

        # Crear la vista (la interfaz gráfica)
        self.view = MainView(master)

        # Conectar el botón de añadir usuario
        self.view.btn_añadir.configure(command=self.abrir_ventana_añadir)

        # Poblar la lista inicial
        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        """Obtiene los usuarios del modelo y actualiza la vista."""
        usuarios = self.gestor.listar()
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice):

        usuario = self.gestor.obtener_por_indice(indice)

        # Cargar la imagen del avatar si existe
        avatar_image = None
        if usuario and usuario.avatar:
            avatar_image = self._cargar_imagen_avatar(usuario.avatar, indice)

        # Mostrar los detalles
        self.view.mostrar_detalles_usuario(usuario, avatar_image)

    def _cargar_imagen_avatar(self, ruta_avatar, indice):
        """
        Carga una imagen de avatar y la guarda en cache.

        Args:
            ruta_avatar (str): Ruta al archivo de imagen
            indice (int): Índice del usuario (para la cache)

        Returns:
            CTkImage: La imagen cargada o None si falla
        """
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

        # Conectar el botón guardar con la función de añadir
        add_view.guardar_button.configure(
            command=lambda: self.añadir_usuario(add_view)
        )

    def añadir_usuario(self, add_view):
        """
        Procesa los datos del formulario y añade el usuario.

        Args:
            add_view (AddUserView): La instancia de la ventana modal
        """
        # Obtener los datos del formulario
        datos = add_view.get_data()

        # Validar que el nombre no esté vacío
        if not datos["nombre"]:
            messagebox.showerror(
                "Error",
                "El nombre es obligatorio"
            )
            return

        # Validar y convertir la edad
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