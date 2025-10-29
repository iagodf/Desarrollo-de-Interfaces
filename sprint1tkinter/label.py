import tkinter as tk

def cambiar_texto():
    etiqueta3.config(text="Texto cambiado")

root = tk.Tk()
root.title("Ej. 1 - Label")

etiqueta1 = tk.Label(root, text="Bienvenido")
etiqueta1.pack(pady=5)

etiqueta2 = tk.Label(root, text="Iago Donsión Fernández")
etiqueta2.pack(pady=5)

etiqueta3 = tk.Label(root, text="Texto original")
etiqueta3.pack(pady=5)

boton = tk.Button(root, text="Cambiar texto", command=cambiar_texto)
boton.pack(pady=10)

root.mainloop()