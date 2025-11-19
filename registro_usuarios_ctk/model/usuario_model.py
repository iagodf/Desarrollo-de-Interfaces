import csv
from pathlib import Path


class Usuario:
    """Representa un usuario con sus datos básicos."""

    def __init__(self, nombre, edad, genero, avatar=None):

        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar


class GestorUsuarios:
    """Gestiona la colección de usuarios y las operaciones sobre ellos."""

    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        """Crea algunos usuarios de prueba (método privado)."""
        self._usuarios.append(Usuario("Ana García", 28, "Femenino", None))
        self._usuarios.append(Usuario("Carlos López", 35, "Masculino", None))
        self._usuarios.append(Usuario("María Rodríguez", 42, "Femenino", None))

    def listar(self):
        """Devuelve la lista completa de usuarios."""
        return self._usuarios

    def obtener_por_indice(self, indice):
        """Obtiene un usuario por su posición en la lista."""
        if 0 <= indice < len(self._usuarios):
            return self._usuarios[indice]
        return None

    def añadir(self, usuario):
        """
        Añade un nuevo usuario a la lista.

        Args:
            usuario (Usuario): El objeto usuario a añadir
        """
        self._usuarios.append(usuario)

    def guardar_csv(self, ruta_archivo):
        """
        Guarda todos los usuarios en un archivo CSV.

        Args:
            ruta_archivo (str o Path): Ruta donde guardar el archivo CSV

        Raises:
            Exception: Si hay algún error al escribir el archivo
        """
        try:
            ruta = Path(ruta_archivo)

            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)

                # Escribir la cabecera
                escritor.writerow(['Nombre', 'Edad', 'Genero', 'Avatar'])

                # Escribir los datos de cada usuario
                for usuario in self._usuarios:
                    escritor.writerow([
                        usuario.nombre,
                        usuario.edad,
                        usuario.genero,
                        usuario.avatar if usuario.avatar else ''
                    ])
        except Exception as e:
            raise Exception(f"Error al guardar el archivo CSV: {str(e)}")

    def cargar_csv(self, ruta_archivo):
        """
        Carga usuarios desde un archivo CSV.

        Args:
            ruta_archivo (str o Path): Ruta del archivo CSV a cargar

        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay algún error al leer el archivo
        """
        try:
            ruta = Path(ruta_archivo)

            if not ruta.exists():
                raise FileNotFoundError(f"El archivo {ruta} no existe")

            # Limpiar la lista actual
            self._usuarios.clear()

            with open(ruta, 'r', encoding='utf-8') as f:
                lector = csv.reader(f)

                # Saltar la cabecera
                next(lector)

                # Leer cada fila y crear usuarios
                for fila in lector:
                    try:
                        # Validar que la fila tenga al menos 3 campos
                        if len(fila) >= 3:
                            nombre = fila[0]
                            edad = int(fila[1])
                            genero = fila[2]
                            avatar = fila[3] if len(fila) > 3 and fila[3] else None

                            usuario = Usuario(nombre, edad, genero, avatar)
                            self._usuarios.append(usuario)
                    except (ValueError, IndexError) as e:
                        # Si una fila está corrupta, la saltamos y continuamos
                        print(f"Advertencia: Fila ignorada por error: {fila}. Error: {e}")
                        continue

        except FileNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error al cargar el archivo CSV: {str(e)}")