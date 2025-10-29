import tkinter as tk
from tkinter import messagebox

class RegistroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ej. 14 - RegistroApp (clases)")

        tk.Label(root, text="Nombre:").pack()
        self.entrada_nombre = tk.Entry(root, width=25)
        self.entrada_nombre.pack()

        tk.Label(root, text="Edad:").pack()
        self.escala_edad = tk.Scale(root, from_=0, to=100, orient="horizontal")
        self.escala_edad.pack()

        tk.Label(root, text="Género:").pack()
        self.var_genero = tk.StringVar(value="Otro")
        tk.Radiobutton(root, text="Masculino", variable=self.var_genero, value="Masculino").pack()
        tk.Radiobutton(root, text="Femenino", variable=self.var_genero, value="Femenino").pack()
        tk.Radiobutton(root, text="Otro", variable=self.var_genero, value="Otro").pack()

        tk.Button(root, text="Añadir", command=self.añadir_usuario).pack(pady=5)

        frame_lista = tk.Frame(root)
        frame_lista.pack()

        self.scroll = tk.Scrollbar(frame_lista)
        self.scroll.pack(side="right", fill="y")

        self.lista = tk.Listbox(frame_lista, width=40, height=8, yscrollcommand=self.scroll.set)
        self.lista.pack(side="left")
        self.scroll.config(command=self.lista.yview)

        tk.Button(root, text="Eliminar", command=self.eliminar_usuario).pack(pady=5)
        tk.Button(root, text="Salir", command=self.salir).pack(pady=5)

        menu_barra = tk.Menu(root)
        root.config(menu=menu_barra)
        menu_archivo = tk.Menu(menu_barra, tearoff=0)
        menu_barra.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Guardar Lista", command=self.guardar_lista)
        menu_archivo.add_command(label="Cargar Lista", command=self.cargar_lista)

    def añadir_usuario(self):
        nombre = self.entrada_nombre.get()
        edad = self.escala_edad.get()
        genero = self.var_genero.get()
        if nombre:
            self.lista.insert(tk.END, f"{nombre} - {edad} años - {genero}")
            self.entrada_nombre.delete(0, tk.END)

    def eliminar_usuario(self):
        seleccion = self.lista.curselection()
        if seleccion:
            self.lista.delete(seleccion[0])

    def guardar_lista(self):
        messagebox.showinfo("Guardar Lista", "Función de guardado simulada.")

    def cargar_lista(self):
        messagebox.showinfo("Cargar Lista", "Función de carga simulada.")

    def salir(self):
        self.root.quit()

root = tk.Tk()
app = RegistroApp(root)
root.mainloop()