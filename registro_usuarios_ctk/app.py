import customtkinter as ctk
from controller import AppController

if __name__ == "__main__":
    # Configurar la apariencia de CustomTkinter
    ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
    ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

    # Crear la ventana principal
    app = ctk.CTk()
    app.title("Registro de Usuarios (CTk + MVC)")
    app.geometry("800x500")

    # Crear el controlador (que a su vez crea modelo y vista)
    controller = AppController(app)

    # Iniciar el bucle principal
    app.mainloop()