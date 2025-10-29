import tkinter as tk

def actualizar(valor):
    etiqueta.config(text=f"Valor seleccionado: {valor}")

root = tk.Tk()
root.title("Ej. 11 - Scale")

var = tk.IntVar()

escala = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=var, command=actualizar)
escala.pack(pady=10)

etiqueta = tk.Label(root, text="Valor seleccionado: 0")
etiqueta.pack(pady=10)

root.mainloop()
