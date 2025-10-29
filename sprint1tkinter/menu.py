import tkinter as tk
from tkinter import messagebox

def acerca_de():
    messagebox.showinfo("Acerca de", "Aplicación creada por Iago Donsión Fernández")

root = tk.Tk()
root.title("Ej. 9 - Menu")

menu_barra = tk.Menu(root)
root.config(menu=menu_barra)

menu_archivo = tk.Menu(menu_barra, tearoff=0)
menu_barra.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir")
menu_archivo.add_command(label="Salir", command=root.quit)

menu_ayuda = tk.Menu(menu_barra, tearoff=0)
menu_barra.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

root.mainloop()
