import tkinter as tk

def mostrar():
    etiqueta_resultado.config(text=entrada.get())

def borrar():
    entrada.delete(0, tk.END)
    etiqueta_resultado.config(text="")

root = tk.Tk()
root.title("Ej. 8 - Frame")

frame_superior = tk.Frame(root)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Introduce texto:").grid(row=0, column=0, padx=5)
entrada = tk.Entry(frame_superior, width=20)
entrada.grid(row=0, column=1, padx=5)
etiqueta_resultado = tk.Label(frame_superior, text="")
etiqueta_resultado.grid(row=1, column=0, columnspan=2, pady=5)

frame_inferior = tk.Frame(root)
frame_inferior.pack()

boton_mostrar = tk.Button(frame_inferior, text="Mostrar", command=mostrar)
boton_mostrar.grid(row=0, column=0, padx=5)

boton_borrar = tk.Button(frame_inferior, text="Borrar", command=borrar)
boton_borrar.grid(row=0, column=1, padx=5)

root.mainloop()
