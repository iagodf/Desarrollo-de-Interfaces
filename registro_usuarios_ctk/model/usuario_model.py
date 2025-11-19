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
    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        self._usuarios.append(Usuario("Ana García", 28, "Femenino", None))
        self._usuarios.append(Usuario("Carlos López", 35, "Masculino", None))
        self._usuarios.append(Usuario("María Rodríguez", 42, "Femenino", None))

    def listar(self):
        return self._usuarios

    def obtener_por_indice(self, indice):
        if 0 <= indice < len(self._usuarios):
            return self._usuarios[indice]
        return None

    def añadir(self, usuario):
        self._usuarios.append(usuario)

    def actualizar(self, indice, usuario):
        if 0 <= indice < len(self._usuarios):
            self._usuarios[indice] = usuario
            return True
        return False

    def eliminar(self, indice):
        if 0 <= indice < len(self._usuarios):
            self._usuarios.pop(indice)
            return True
        return False

    def buscar_y_filtrar(self, texto_busqueda="", filtro_genero="Todos"):
        resultados = []

        for usuario in self._usuarios:
            # Filtrar por texto (nombre)
            if texto_busqueda and texto_busqueda.lower() not in usuario.nombre.lower():
                continue

            # Filtrar por género
            if filtro_genero != "Todos" and usuario.genero != filtro_genero:
                continue

            resultados.append(usuario)

        return resultados

    def contar_por_genero(self):
        conteo = {"Masculino": 0, "Femenino": 0, "Otro": 0}
        for usuario in self._usuarios:
            if usuario.genero in conteo:
                conteo[usuario.genero] += 1
        return conteo

    def guardar_csv(self, ruta_archivo):
        try:
            ruta = Path(ruta_archivo)

            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow(['Nombre', 'Edad', 'Genero', 'Avatar'])

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
        try:
            ruta = Path(ruta_archivo)

            if not ruta.exists():
                raise FileNotFoundError(f"El archivo {ruta} no existe")

            self._usuarios.clear()

            with open(ruta, 'r', encoding='utf-8') as f:
                lector = csv.reader(f)
                next(lector)

                for fila in lector:
                    try:
                        if len(fila) >= 3:
                            nombre = fila[0]
                            edad = int(fila[1])
                            genero = fila[2]
                            avatar = fila[3] if len(fila) > 3 and fila[3] else None

                            usuario = Usuario(nombre, edad, genero, avatar)
                            self._usuarios.append(usuario)
                    except (ValueError, IndexError) as e:
                        print(f"Advertencia: Fila ignorada por error: {fila}. Error: {e}")
                        continue

        except FileNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error al cargar el archivo CSV: {str(e)}")