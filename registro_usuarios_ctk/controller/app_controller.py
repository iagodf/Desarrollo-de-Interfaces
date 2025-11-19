
from pathlib import Path
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk
import threading
import time

from model.usuario_model import Usuario, GestorUsuarios
from view.main_view import MainView, AddUserView


class AppController:
    def __init__(self, master):
        self.master = master

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.CSV_FILE = self.BASE_DIR / "usuarios.csv"

        self.avatar_images = {}
        self.usuario_seleccionado_idx = None
        self.auto_guardado_activo = False
        self.hilo_auto_guardado = None

        self.gestor = GestorUsuarios()
        self.view = MainView(master)

        # Conectar botones
        self.view.btn_añadir.configure(command=self.abrir_ventana_añadir)
        self.view.btn_editar.configure(command=self.editar_usuario)
        self.view.btn_eliminar.configure(command=self.eliminar_usuario)

        # Conectar búsqueda y filtro
        self.view.busqueda_var.trace_add("write", lambda *args: self.aplicar_filtros())
        self.view.filtro_genero_var.trace_add("write", lambda *args: self.aplicar_filtros())

        # Menú
        self.view.menu_archivo.add_command(label="Guardar", command=self.guardar_usuarios)
        self.view.menu_archivo.add_command(label="Cargar", command=self.cargar_usuarios)
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(
            label="Activar Auto-guardado",
            command=self.toggle_auto_guardado
        )
        self.view.menu_archivo.add_separator()
        self.view.menu_archivo.add_command(label="Salir", command=self.salir)

        self.cargar_usuarios()

        if not self.gestor.listar():
            self.gestor._cargar_datos_de_ejemplo()

        self.refrescar_lista_usuarios()
        self.actualizar_estadisticas()

    def aplicar_filtros(self):
        texto_busqueda = self.view.busqueda_var.get()
        filtro_genero = self.view.filtro_genero_var.get()

        usuarios_filtrados = self.gestor.buscar_y_filtrar(texto_busqueda, filtro_genero)

        self.view.actualizar_lista_usuarios(
            usuarios_filtrados,
            self.seleccionar_usuario,
            self.editar_usuario_doble_clic
        )

        self.view.actualizar_barra_estado(
            f"Mostrando {len(usuarios_filtrados)} de {len(self.gestor.listar())} usuarios"
        )

    def refrescar_lista_usuarios(self):
        self.aplicar_filtros()

    def seleccionar_usuario(self, indice):
        # Obtener el usuario del conjunto FILTRADO
        texto_busqueda = self.view.busqueda_var.get()
        filtro_genero = self.view.filtro_genero_var.get()
        usuarios_filtrados = self.gestor.buscar_y_filtrar(texto_busqueda, filtro_genero)

        if indice < len(usuarios_filtrados):
            usuario = usuarios_filtrados[indice]
            # Buscar el índice real en la lista completa
            self.usuario_seleccionado_idx = self.gestor.listar().index(usuario)

            avatar_image = None
            if usuario.avatar:
                avatar_image = self._cargar_imagen_avatar(usuario.avatar, self.usuario_seleccionado_idx)

            self.view.mostrar_detalles_usuario(usuario, avatar_image)

    def editar_usuario_doble_clic(self, indice):
        self.seleccionar_usuario(indice)
        self.editar_usuario()

    def editar_usuario(self):
        if self.usuario_seleccionado_idx is None:
            return

        usuario_actual = self.gestor.obtener_por_indice(self.usuario_seleccionado_idx)

        edit_view = AddUserView(self.master, usuario_actual)
        edit_view.guardar_button.configure(
            command=lambda: self.guardar_edicion(edit_view)
        )

    def guardar_edicion(self, edit_view):
        datos = edit_view.get_data()

        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            edad = int(datos["edad"])
            if edad <= 0 or edad > 150:
                raise ValueError("Edad fuera de rango")
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número válido entre 1 y 150")
            return

        usuario_actualizado = Usuario(
            nombre=datos["nombre"],
            edad=edad,
            genero=datos["genero"],
            avatar=datos["avatar"]
        )

        self.gestor.actualizar(self.usuario_seleccionado_idx, usuario_actualizado)
        self.refrescar_lista_usuarios()
        self.actualizar_estadisticas()

        edit_view.window.destroy()

        messagebox.showinfo("Éxito", f"Usuario '{datos['nombre']}' actualizado correctamente")

    def eliminar_usuario(self):
        if self.usuario_seleccionado_idx is None:
            return

        usuario = self.gestor.obtener_por_indice(self.usuario_seleccionado_idx)

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar a '{usuario.nombre}'?"
        )

        if confirmar:
            self.gestor.eliminar(self.usuario_seleccionado_idx)
            self.usuario_seleccionado_idx = None
            self.view.mostrar_detalles_usuario(None)
            self.refrescar_lista_usuarios()
            self.actualizar_estadisticas()

            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")

    def actualizar_estadisticas(self):
        total = len(self.gestor.listar())
        conteo = self.gestor.contar_por_genero()

        mensaje = f"Total: {total} | M: {conteo['Masculino']} | F: {conteo['Femenino']} | Otro: {conteo['Otro']}"
        self.view.actualizar_barra_estado(mensaje)

    def _cargar_imagen_avatar(self, ruta_avatar, indice):
        try:
            ruta = Path(ruta_avatar)

            if not ruta.is_absolute():
                ruta = self.ASSETS_PATH / ruta_avatar

            if ruta.exists():
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
        add_view = AddUserView(self.master)
        add_view.guardar_button.configure(
            command=lambda: self.añadir_usuario(add_view)
        )

    def añadir_usuario(self, add_view):
        datos = add_view.get_data()

        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            edad = int(datos["edad"])
            if edad <= 0 or edad > 150:
                raise ValueError("Edad fuera de rango")
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número válido entre 1 y 150")
            return

        nuevo_usuario = Usuario(
            nombre=datos["nombre"],
            edad=edad,
            genero=datos["genero"],
            avatar=datos["avatar"]
        )

        self.gestor.añadir(nuevo_usuario)
        self.refrescar_lista_usuarios()
        self.actualizar_estadisticas()

        add_view.window.destroy()

        messagebox.showinfo("Éxito", f"Usuario '{datos['nombre']}' añadido correctamente")

    def guardar_usuarios(self):
        try:
            self.gestor.guardar_csv(self.CSV_FILE)
            self.view.actualizar_barra_estado(f"✓ Guardado en {self.CSV_FILE.name}")
            messagebox.showinfo("Éxito", f"Usuarios guardados correctamente")
        except Exception as e:
            self.view.actualizar_barra_estado("✗ Error al guardar")
            messagebox.showerror("Error al guardar", f"No se pudieron guardar los usuarios:\n{str(e)}")

    def cargar_usuarios(self):
        try:
            self.gestor.cargar_csv(self.CSV_FILE)
            self.refrescar_lista_usuarios()
            self.actualizar_estadisticas()
            self.view.actualizar_barra_estado(f"✓ Cargado desde {self.CSV_FILE.name}")
        except FileNotFoundError:
            print(f"Archivo {self.CSV_FILE.name} no encontrado.")
        except Exception as e:
            self.view.actualizar_barra_estado("✗ Error al cargar")
            messagebox.showerror("Error al cargar", f"No se pudieron cargar los usuarios:\n{str(e)}")

    def toggle_auto_guardado(self):
        if self.auto_guardado_activo:
            self.detener_auto_guardado()
        else:
            self.iniciar_auto_guardado()

    def iniciar_auto_guardado(self):
        self.auto_guardado_activo = True

        # Actualizar el texto del menú
        self.view.menu_archivo.entryconfig(
            3,  # Índice de la opción "Activar Auto-guardado"
            label="Detener Auto-guardado"
        )

        # Crear y arrancar el hilo
        self.hilo_auto_guardado = threading.Thread(
            target=self._auto_guardar_loop,
            daemon=True
        )
        self.hilo_auto_guardado.start()

        self.view.actualizar_barra_estado("🔄 Auto-guardado activado (cada 10 segundos)")

    def detener_auto_guardado(self):
        self.auto_guardado_activo = False

        # Actualizar el texto del menú
        self.view.menu_archivo.entryconfig(
            3,
            label="Activar Auto-guardado"
        )

        self.view.actualizar_barra_estado("⏸️ Auto-guardado detenido")

    def _auto_guardar_loop(self):
        while self.auto_guardado_activo:
            time.sleep(10)  # Esperar 10 segundos

            if self.auto_guardado_activo:  # Verificar de nuevo por si se detuvo
                # Usar after() para ejecutar en el hilo principal
                self.master.after(0, self._guardar_automatico)

    def _guardar_automatico(self):
        try:
            self.gestor.guardar_csv(self.CSV_FILE)
            self.view.actualizar_barra_estado(
                f"🔄 Auto-guardado: {time.strftime('%H:%M:%S')}"
            )
        except Exception as e:
            print(f"Error en auto-guardado: {e}")

    def salir(self):
        # Detener el auto-guardado antes de cerrar
        if self.auto_guardado_activo:
            self.detener_auto_guardado()

        self.master.quit()