import tkinter as tk

def mostrar_fruta():
    seleccion = lista.curselection()
    if seleccion:
        fruta = lista.get(seleccion[0])
        etiqueta.config(text=f"Fruta seleccionada: {fruta}")

root = tk.Tk()
root.title("Ej. 6 - Listbox")

lista = tk.Listbox(root, height=5)
for fruta in ["Manzana", "Banana", "Naranja"]:
    lista.insert(tk.END, fruta)
lista.pack(pady=5)

boton = tk.Button(root, text="Mostrar selección", command=mostrar_fruta)
boton.pack(pady=5)

etiqueta = tk.Label(root, text="")
etiqueta.pack(pady=10)

root.mainloop()
