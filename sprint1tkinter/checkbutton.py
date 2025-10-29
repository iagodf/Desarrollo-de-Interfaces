import tkinter as tk

def actualizar():
    seleccionadas = []
    if var_leer.get():
        seleccionadas.append("Leer")
    if var_deporte.get():
        seleccionadas.append("Deporte")
    if var_musica.get():
        seleccionadas.append("Música")
    etiqueta.config(text="Aficiones: " + ", ".join(seleccionadas))

root = tk.Tk()
root.title("Ej. 4 - Checkbutton")

var_leer = tk.BooleanVar()
var_deporte = tk.BooleanVar()
var_musica = tk.BooleanVar()

check1 = tk.Checkbutton(root, text="Leer", variable=var_leer, command=actualizar)
check1.pack()
check2 = tk.Checkbutton(root, text="Deporte", variable=var_deporte, command=actualizar)
check2.pack()
check3 = tk.Checkbutton(root, text="Música", variable=var_musica, command=actualizar)
check3.pack()

etiqueta = tk.Label(root, text="Aficiones:")
etiqueta.pack(pady=10)

root.mainloop()
