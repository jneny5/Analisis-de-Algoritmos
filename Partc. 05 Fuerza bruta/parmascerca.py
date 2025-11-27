import math
import tkinter as tk
import random

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def comparacion(puntos):
    dist_min = 1000000  
    punto1 = None
    punto2 = None
    for i in range(len(puntos)):
        for j in range(i+1, len(puntos)):
            d = dist(puntos[i], puntos[j])
            if d < dist_min:
                dist_min = d
                punto1 = puntos[i]
                punto2 = puntos[j]
    return punto1, punto2, dist_min

def calcular():
    puntos = []
    for i in range(5):
        try:
            x = float(entradas_x[i].get())
            y = float(entradas_y[i].get())
            if x <0 or x> 40 or y<0 or y >40:
                resultado.set("Los valores deben estar entre 0 y 40")
                return
            puntos.append((x,y))
        except:
            resultado.set("Por favor, escribe números válidos")
            return
    p1, p2, d = comparacion(puntos)
    resultado.set(f"Puntos mas cercanos: {p1} y {p2} \nDistancia: {d:.2f}")

def generar():
    for i in range(5):
        x = random.uniform(0,40)
        y = random.uniform(0,40)
        entradas_x[i].delete(0, tk.END)
        entradas_x[i].insert(0, f"{x:.2f}")
        entradas_y[i].delete(0, tk.END)
        entradas_y[i].insert(0, f"{y:.2f}")
    calcular() 

def limpiar():
    for i in range(5):
        entradas_x[i].delete(0, tk.END)
        entradas_y[i].delete(0, tk.END)
    resultado.set("")

root = tk.Tk()
root.title("Par mas cercano")

entradas_x = []
entradas_y = []

tk.Label(root, text="Puntos").grid(row=0, column=0)
tk.Label(root, text="X").grid(row=0, column=1)
tk.Label(root, text="Y").grid(row=0, column=2)
for i in range(5):
    tk.Label(root, text=f"Punto {i+1}").grid(row=i+1, column=0)
    entrada_x = tk.Entry(root,width=8)
    entrada_x.grid(row=i+1, column=1)
    entradas_x.append(entrada_x)
    entrada_y = tk.Entry(root, width=8)
    entrada_y.grid(row=i+1, column=2)
    entradas_y.append(entrada_y)

# Botones
frame_botones = tk.Frame(root)
frame_botones.grid(row=6, column=0, columnspan=3, pady=10)

boton_calcular = tk.Button(frame_botones, text="Calcular", command=calcular)
boton_calcular.pack(side='left', padx=5)

boton_aleatorio = tk.Button(frame_botones, text="Generar aleatorios", command=generar)
boton_aleatorio.pack(side='left', padx=5)

boton_limpiar = tk.Button(frame_botones, text="Limpiar", command=limpiar)
boton_limpiar.pack(side='left', padx=5)


#mostrar resultado
resultado = tk.StringVar()
etiqueta_resultado = tk.Label(root, textvariable=resultado)
etiqueta_resultado.grid(row=7, column=0, columnspan=4)

root.mainloop()
