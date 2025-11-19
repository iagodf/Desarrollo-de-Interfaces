from model import GestorUsuarios
from view import MainView


class AppController:
    """Controlador principal de la aplicación."""

    def __init__(self, master):
        """
        Inicializa el controlador, crea el modelo y la vista, y los conecta.

        Args:
            master: La ventana raíz de CTk
        """
        self.master = master

        # Crear el modelo (la lógica de negocio)
        self.gestor = GestorUsuarios()

        # Crear la vista (la interfaz gráfica)
        self.view = MainView(master)

        # Poblar la lista inicial
        self.refrescar_lista_usuarios()

    def refrescar_lista_usuarios(self):
        """
        Obtiene los usuarios del modelo y actualiza la vista.
        Este método es el puente entre el modelo y la vista.
        """
        # 1. Pedir los datos al modelo
        usuarios = self.gestor.listar()

        # 2. Pasarle los datos a la vista junto con el callback de selección
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice):
        """
        Callback que se ejecuta cuando el usuario hace clic en un nombre.

        Args:
            indice (int): La posición del usuario en la lista
        """
        # 1. Pedir al modelo el usuario completo
        usuario = self.gestor.obtener_por_indice(indice)

        # 2. Pedirle a la vista que muestre los detalles
        self.view.mostrar_detalles_usuario(usuario)