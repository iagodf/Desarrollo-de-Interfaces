import tkinter as tk

root = tk.Tk()
root.title("Ej. 10 - Scrollbar")

texto = tk.Text(root, wrap="word", width=40, height=10)
texto.pack(side="left", fill="y")

scroll = tk.Scrollbar(root, orient="vertical", command=texto.yview)
scroll.pack(side="right", fill="y")

texto.config(yscrollcommand=scroll.set)

for i in range(1, 51):
    texto.insert(tk.END, f"Línea {i}: Este es un texto de ejemplo.\n")

root.mainloop()
