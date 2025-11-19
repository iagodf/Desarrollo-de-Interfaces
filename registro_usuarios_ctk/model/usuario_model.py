class Usuario:
    """Representa un usuario con sus datos básicos."""

    def __init__(self, nombre, edad, genero, avatar=None):
        """
        Inicializa un usuario.

        Args:
            nombre (str): Nombre del usuario
            edad (int): Edad del usuario
            genero (str): Género del usuario
            avatar (str): Ruta al archivo de imagen del avatar (opcional)
        """
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar


class GestorUsuarios:
    """Gestiona la colección de usuarios y las operaciones sobre ellos."""

    def __init__(self):
        """Inicializa el gestor con una lista vacía de usuarios."""
        self._usuarios = []
        # Cargamos algunos datos de ejemplo para probar
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        """Crea algunos usuarios de prueba (método privado)."""
        self._usuarios.append(Usuario("Ana García", 28, "Femenino", None))
        self._usuarios.append(Usuario("Carlos López", 35, "Masculino", None))
        self._usuarios.append(Usuario("María Rodríguez", 42, "Femenino", None))

    def listar(self):
        """
        Devuelve la lista completa de usuarios.

        Returns:
            list: Lista de objetos Usuario
        """
        return self._usuarios

    def obtener_por_indice(self, indice):
        """
        Obtiene un usuario por su posición en la lista.

        Args:
            indice (int): Posición del usuario en la lista

        Returns:
            Usuario: El objeto usuario si existe, None si el índice es inválido
        """
        if 0 <= indice < len(self._usuarios):
            return self._usuarios[indice]
        return None