import tkinter as tk
import numpy as npy 
import time 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


#IMPLEMENTACION DE ALGORTIMOS
def busqueda_lineal(lista, x):
    for i in range(0, len(lista)):
        if lista[i]==x:
            return i #se encontró
    return -1 #no se encontró

def busqueda_binaria(lista, x):
    l, r = 0, len(lista) - 1

    while l <= r:
        mid=l + (r-l)//2
        if lista[mid]==x:
            return mid
        elif lista[mid]<x:
            l=mid+1
        else:
            r=mid-1
    return -1 #no se encontró

#GENERAR DATOS
datos=[]
def generador_numeros():
    global datos
    try:
        tam = int(entrada_tam.get())
    except ValueError:
        lbl_datos.config(text=f"Porfavor ingrese un numero valido (ej. 100, 1000, 10000 o 100000)")
        return
    if tam not in [100, 1000, 10000, 100000]:
        lbl_datos.config(text="Tamaño invalido, use: 100, 1000, 10000 o 100000")
        return
    datos = npy.random.randint(0, tam * 10, size=tam)
    datos = npy.sort(datos)  #ordenamos
    lbl_datos.config(text=f"Datos generados: {tam} elementos")
    return datos.tolist()

#VALOR A BUSCAR
def valor_lineal():
    if len(datos) == 0:
        lbl_resultado.config(text="Primero genere los datos")
        return
    try:
        val = int(entrada_valor.get())
    except ValueError:
        lbl_resultado.config(text=f"Por favor ingrese un numero valido")
        return
    
    inicio = time.perf_counter()
    indice=busqueda_lineal(datos, val)
    fin = time.perf_counter()
    tiempo= (fin-inicio)*1000

    if indice != -1:
        lbl_resultado.config(text=f"Lineal - Indice: {indice}   Tiempo: {tiempo:.4f} ms")
    else:
        lbl_resultado.config(text=f"Lineal - No encontrado   Tiempo: {tiempo:.4f} ms")


def valor_binaria():
    if len(datos) == 0:
        lbl_resultado.config(text="Primero genere los datos")
        return
    try:
        val= int(entrada_valor.get())
    except ValueError:
        lbl_resultado.config(text=f"Porfavor ingrese un numero valido")
        return
    inicio = time.perf_counter()
    indice=busqueda_binaria(datos, val)
    fin = time.perf_counter()
    tiempo= (fin-inicio)*1000

    if indice !=-1:
        lbl_resultado.config(text=f"Binaria - Indice: {indice}   Tiempo: {tiempo:.4f}ms")
    else:
        lbl_resultado.config(text=f"Binaria - No encontrado   Tiempo: {tiempo:.4f}ms")

def comparar_tiempos():
    tamanos = [100, 1000, 10000, 100000]
    repeticiones = 5

    tiempos_lineal = []
    tiempos_binaria = []

    for tam in tamanos:
        lista = npy.random.randint(0, tam*10, size=tam)
        lista = npy.sort(lista)
        val = npy.random.choice(lista) 

        #Lineal
        total= 0
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            busqueda_lineal(lista, val)
            fin = time.perf_counter()
            total += (fin - inicio) * 1000
        tiempos_lineal.append(total / repeticiones)

        #Binaria
        total = 0
        for _ in range(repeticiones):
            inicio= time.perf_counter()
            busqueda_binaria(lista, val)
            fin = time.perf_counter()
            total += (fin - inicio) * 1000
        tiempos_binaria.append(total / repeticiones)

    #GRAFICA
    fig = Figure(figsize=(5,3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(tamanos, tiempos_lineal, marker="o", label="Lineal")
    ax.plot(tamanos, tiempos_binaria, marker="o", label="Binaria")
    ax.set_title("Comparacion de tiempos")
    ax.set_xlabel("Tamaño de lista")
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.legend()

    for widget in frame_grafica.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#INTERFAZ GRAFICA
root = tk.Tk()
root.title("No se")
root.geometry("450x750")
root.configure(background='lightgreen')

lbl = tk.Label(root, text="Tamaño de lista (usar 100, 1000, 10000 o 100000): ", bg='lightgreen')
lbl.pack(pady=10)
entrada_tam= tk.Entry(root, width=8)
entrada_tam.pack(pady=3)

btn=tk.Button(root, text="Generar datos", bg='lightgreen', command=generador_numeros)
btn.pack(pady=10)

lbl_datos = tk.Label(root, text="", bg='lightgreen')
lbl_datos.pack(pady=10)

lbl = tk.Label(root, text="Valor a buscar:", bg='lightgreen')
lbl.pack(pady=15)
entrada_valor= tk.Entry(root, width=8)
entrada_valor.pack(pady=3)

btn=tk.Button(root, text="Busqueda Lineal", bg='lightgreen', command=valor_lineal)
btn.pack(pady=2)

btn=tk.Button(root, text="Busqueda Binaria", bg='lightgreen', command= valor_binaria)
btn.pack(pady=2)

lbl_resultado = tk.Label(root, text="", bg='lightgreen')
lbl_resultado.pack(pady=10)

frame_grafica = tk.Frame(root, bg="lightgreen", height=200)
frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

btn = tk.Button(root, text="Comparar tiempos", bg='lightgreen', command=comparar_tiempos)
btn.pack(pady=5)

root.mainloop()