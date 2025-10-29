import tkinter as tk

def mostrar_mensaje():
    etiqueta.config(text="Has presionado el boton")

root = tk.Tk()
root.title("Ej. 2 - Button")

etiqueta = tk.Label(root, text="")
etiqueta.pack(pady=10)

boton_mostrar = tk.Button(root, text="Mostrar mensaje", command=mostrar_mensaje)
boton_mostrar.pack(pady=5)

boton_salir = tk.Button(root, text="Salir", command=root.quit)
boton_salir.pack(pady=5)

root.mainloop()
