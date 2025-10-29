import tkinter as tk

def cambiar_color():
    root.config(bg=var_color.get())

root = tk.Tk()
root.title("Ej. 5 - Radiobutton")

var_color = tk.StringVar(value="white")

radio_rojo = tk.Radiobutton(root, text="Rojo", variable=var_color, value="red", command=cambiar_color)
radio_rojo.pack()
radio_verde = tk.Radiobutton(root, text="Verde", variable=var_color, value="green", command=cambiar_color)
radio_verde.pack()
radio_azul = tk.Radiobutton(root, text="Azul", variable=var_color, value="blue", command=cambiar_color)
radio_azul.pack()

root.mainloop()
