import tkinter as tk
from tkinter import messagebox

def añadir_usuario():
    nombre = entrada_nombre.get()
    edad = escala_edad.get()
    genero = var_genero.get()
    if nombre:
        lista.insert(tk.END, f"{nombre} - {edad} años - {genero}")
        entrada_nombre.delete(0, tk.END)

def eliminar_usuario():
    seleccion = lista.curselection()
    if seleccion:
        lista.delete(seleccion[0])

def guardar_lista():
    messagebox.showinfo("Guardar Lista", "Función de guardado simulada.")

def cargar_lista():
    messagebox.showinfo("Cargar Lista", "Función de carga simulada.")

def salir():
    root.quit()

root = tk.Tk()
root.title("Ej. 12 - Registro de Usuarios")

tk.Label(root, text="Nombre:").pack()
entrada_nombre = tk.Entry(root, width=25)
entrada_nombre.pack()

tk.Label(root, text="Edad:").pack()
escala_edad = tk.Scale(root, from_=0, to=100, orient="horizontal")
escala_edad.pack()

tk.Label(root, text="Género:").pack()
var_genero = tk.StringVar(value="Otro")
tk.Radiobutton(root, text="Masculino", variable=var_genero, value="Masculino").pack()
tk.Radiobutton(root, text="Femenino", variable=var_genero, value="Femenino").pack()
tk.Radiobutton(root, text="Otro", variable=var_genero, value="Otro").pack()

tk.Button(root, text="Añadir", command=añadir_usuario).pack(pady=5)

frame_lista = tk.Frame(root)
frame_lista.pack()

scroll = tk.Scrollbar(frame_lista)
scroll.pack(side="right", fill="y")

lista = tk.Listbox(frame_lista, width=40, height=8, yscrollcommand=scroll.set)
lista.pack(side="left")
scroll.config(command=lista.yview)

tk.Button(root, text="Eliminar", command=eliminar_usuario).pack(pady=5)
tk.Button(root, text="Salir", command=salir).pack(pady=5)

menu_barra = tk.Menu(root)
root.config(menu=menu_barra)
menu_archivo = tk.Menu(menu_barra, tearoff=0)
menu_barra.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Guardar Lista", command=guardar_lista)
menu_archivo.add_command(label="Cargar Lista", command=cargar_lista)

root.mainloop()
