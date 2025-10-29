import tkinter as tk

def dibujar(event):
    x, y = event.x, event.y
    canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")

def limpiar(event):
    canvas.delete("all")

root = tk.Tk()
root.title("Ej. 13 - Eventos de teclado y ratón")

canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

canvas.bind("<Button-1>", dibujar)
root.bind("<KeyPress-c>", limpiar)

root.mainloop()