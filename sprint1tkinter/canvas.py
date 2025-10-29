import tkinter as tk

def dibujar():
    x1 = int(entrada_x1.get())
    y1 = int(entrada_y1.get())
    x2 = int(entrada_x2.get())
    y2 = int(entrada_y2.get())
    canvas.delete("all")
    canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue")
    canvas.create_oval(x1, y1, x2, y2, fill="pink")

root = tk.Tk()
root.title("Ej. 7 - Canvas")

tk.Label(root, text="x1:").pack()
entrada_x1 = tk.Entry(root, width=5)
entrada_x1.pack()

tk.Label(root, text="y1:").pack()
entrada_y1 = tk.Entry(root, width=5)
entrada_y1.pack()

tk.Label(root, text="x2:").pack()
entrada_x2 = tk.Entry(root, width=5)
entrada_x2.pack()

tk.Label(root, text="y2:").pack()
entrada_y2 = tk.Entry(root, width=5)
entrada_y2.pack()

boton = tk.Button(root, text="Dibujar", command=dibujar)
boton.pack(pady=5)

canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(pady=10)

root.mainloop()
