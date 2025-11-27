import time  # Librería para medir tiempo de ejecución
import matplotlib.pyplot as plt # type: ignore

# Fibonacci sin Programación Dinámica 
def fib_recursivo(n):
    if n <= 1:
        return n
    return fib_recursivo(n-1) + fib_recursivo(n-2)

# Fibonacci con Programación Dinámica.
def fib_dinamico(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_dinamico(n-1, memo) + fib_dinamico(n-2, memo)
    return memo[n]

# Valores de n a probar (de 5 a 33 en pasos de 2)
n_values = list(range(5, 35, 2))
tiempos_recursivo = []
tiempos_dinamico = []

# Medir tiempo de ejecución de ambas implementaciones
for n in n_values:
    start = time.time()
    fib_recursivo(n)
    tiempos_recursivo.append(time.time() - start)

    # pasar {} para iniciar memo vacío y medir solo el coste de la llamada actual
    start = time.time()
    fib_dinamico(n, {})
    tiempos_dinamico.append(time.time() - start)

# Graficar los tiempos medidos
plt.figure()
plt.plot(n_values, tiempos_recursivo, marker="o", label="Sin Programación Dinámica")
plt.plot(n_values, tiempos_dinamico, marker="o", label="Con Programación Dinámica")
plt.title("Complejidad Temporal - Fibonacci")
plt.xlabel("Valor de n")
plt.ylabel("Tiempo (s)")
plt.legend()
plt.grid(True)
plt.show()
