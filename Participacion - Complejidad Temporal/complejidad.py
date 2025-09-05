import tkinter as tk
import numpy as npy 
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#GENERAR DATOS
def generar_datos(n):
    datos=npy.random.randint(low= 0, high= 1000, size=n)
    return datos.tolist()
    
#ORDENAMIENTOS
def bubblesort(vectorbs):
    inicio = time.perf_counter()
    
    n = 0 
    for _ in vectorbs:
        n += 1 
    
    for i in range(n-1): 
        for j in range(0, n-i-1): 
            if vectorbs[j] > vectorbs[j+1] :
                vectorbs[j], vectorbs[j+1] = vectorbs[j+1], vectorbs[j]
          
    fin = time.perf_counter()
    tiempo= (fin-inicio)*1000
    
    return fin-inicio

def mergesort(vectormerge): 
    inicio = time.perf_counter()
    
    def merge(vectormerge):
    
        def largo(vec):
                largovec = 0 
                for _ in vec:
                    largovec += 1
                return largovec
        
        if largo(vectormerge) >1: 
            medio = largo(vectormerge)//2 
            
            izq = vectormerge[:medio]  
            der = vectormerge[medio:]
            
            merge(izq) 
            merge(der) 
            
            i = j = k = 0
        
            while i < largo(izq) and j < largo(der): 
                if izq[i] < der[j]: 
                    vectormerge[k] = izq[i] 
                    i+= 1
                else: 
                    vectormerge[k] = der[j] 
                    j+= 1
                k += 1
            
            while i < largo(izq): 
                vectormerge[k] = izq[i] 
                i+= 1
                k+= 1
            
            while j < largo(der): 
                vectormerge[k] = der[j] 
                j+= 1
                k+= 1
    merge(vectormerge)

    fin = time.perf_counter()
    tiempo= (fin-inicio)*1000
    
    return fin-inicio
    
def quicksort(vectorquick):
    inicio = time.perf_counter()
    
    def quick(vectorquick, start, end):
        if start >= end:
            return

        def particion(vectorquick, start, end):
            pivot = vectorquick[start]
            menor = start + 1
            mayor = end

            while True:
                while menor <= mayor and vectorquick[mayor] >= pivot:
                    mayor -= 1
                while menor <= mayor and vectorquick[menor] <= pivot:
                    menor += 1
                if menor <= mayor:
                    vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
                else:
                    break

            vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]
            return mayor
        
        p = particion(vectorquick, start, end)
        quick(vectorquick, start, p - 1)
        quick(vectorquick, p + 1, end)

    quick(vectorquick, 0, len(vectorquick) - 1)
    fin = time.perf_counter()
    tiempo= (fin-inicio)*1000
    
    return fin-inicio

def graficar_resultados():
    tamanos = list(range(50, 1050, 50))
    tiempos_bubble = []
    tiempos_merge = []
    tiempos_quick = []

    for n in tamanos:
        datos = generar_datos(n)

        datos_bubble = datos.copy()
        datos_merge = datos.copy()
        datos_quick = datos.copy()

        tiempo_bubble = bubblesort(datos_bubble)
        tiempo_merge = mergesort(datos_merge)
        tiempo_quick = quicksort(datos_quick)

        tiempos_bubble.append(tiempo_bubble)
        tiempos_merge.append(tiempo_merge)
        tiempos_quick.append(tiempo_quick)

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(tamanos, tiempos_bubble, label="Bubble Sort", marker='o', color='red')
    ax.plot(tamanos, tiempos_merge, label="Merge Sort", marker='s', color='green')
    ax.plot(tamanos, tiempos_quick, label="Quick Sort", marker='^', color='blue')

    ax.set_title("Comparacion de Tiempos de Ordenamiento")
    ax.set_xlabel("Tamaño de la lista (N)")
    ax.set_ylabel("Tiempo (s)")
    ax.legend()
    ax.grid(True)

    ventana = tk.Tk()
    ventana.title("Grafica Comparativa")
    
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack()

    ventana.mainloop()

if __name__ == "__main__":
    graficar_resultados()