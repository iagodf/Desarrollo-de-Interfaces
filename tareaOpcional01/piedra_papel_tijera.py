import tkinter as tk
from tkinter import messagebox
import random

def jugar(eleccion_jugador):
    if puntos_jugador.get() == 3 or puntos_maquina.get() == 3:
        return
    eleccion_cpu = random.choice(["Piedra", "Papel", "Tijera"])
    var_jugador.set(f"Tú eliges: {eleccion_jugador}")
    var_maquina.set(f"La máquina elige: {eleccion_cpu}")
    ganador = determinar_ganador(eleccion_jugador, eleccion_cpu)
    if ganador == "jugador":
        puntos_jugador.set(puntos_jugador.get() + 1)
        var_resultado.set(f"Ganaste esta ronda ({eleccion_jugador} vence a {eleccion_cpu})")
    elif ganador == "maquina":
        puntos_maquina.set(puntos_maquina.get() + 1)
        var_resultado.set(f"Perdiste la ronda ({eleccion_cpu} vence a {eleccion_jugador})")
    else:
        var_resultado.set("Empate. No cuenta la ronda.")
    comprobar_final()

def determinar_ganador(jugador, cpu):
    if jugador == cpu:
        return "empate"
    if (jugador == "Piedra" and cpu == "Tijera") or (jugador == "Tijera" and cpu == "Papel") or (jugador == "Papel" and cpu == "Piedra"):
        return "jugador"
    return "maquina"

def comprobar_final():
    if puntos_jugador.get() == 3:
        messagebox.showinfo("Fin de partida", "¡Has ganado la partida!")
    elif puntos_maquina.get() == 3:
        messagebox.showinfo("Fin de partida", "Has perdido la partida.")

def nuevo_juego():
    puntos_jugador.set(0)
    puntos_maquina.set(0)
    var_jugador.set("")
    var_maquina.set("")
    var_resultado.set("Nueva partida. Elige tu jugada.")

def salir():
    root.quit()

root = tk.Tk()
root.title("Ej. Extra - Piedra, Papel o Tijera")

frame_superior = tk.Frame(root)
frame_superior.pack(pady=10)

tk.Label(frame_superior, text="Juega contra la máquina (mejor de 5)").pack()

frame_botones = tk.Frame(root)
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Piedra", width=10, command=lambda: jugar("Piedra")).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Papel", width=10, command=lambda: jugar("Papel")).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Tijera", width=10, command=lambda: jugar("Tijera")).grid(row=0, column=2, padx=5)

frame_info = tk.Frame(root)
frame_info.pack(pady=10)

var_jugador = tk.StringVar()
var_maquina = tk.StringVar()
var_resultado = tk.StringVar(value="Nueva partida. Elige tu jugada.")

tk.Label(frame_info, textvariable=var_jugador).pack()
tk.Label(frame_info, textvariable=var_maquina).pack()
tk.Label(frame_info, textvariable=var_resultado).pack(pady=5)


frame_marcador = tk.Frame(root)
frame_marcador.pack(pady=5)

puntos_jugador = tk.IntVar(value=0)
puntos_maquina = tk.IntVar(value=0)

tk.Label(frame_marcador, text="Jugador:").grid(row=0, column=0)
tk.Label(frame_marcador, textvariable=puntos_jugador).grid(row=0, column=1, padx=10)
tk.Label(frame_marcador, text="Máquina:").grid(row=0, column=2)
tk.Label(frame_marcador, textvariable=puntos_maquina).grid(row=0, column=3, padx=10)

frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

tk.Button(frame_controles, text="Nuevo juego", command=nuevo_juego).grid(row=0, column=0, padx=10)
tk.Button(frame_controles, text="Salir", command=salir).grid(row=0, column=1, padx=10)

root.mainloop()
