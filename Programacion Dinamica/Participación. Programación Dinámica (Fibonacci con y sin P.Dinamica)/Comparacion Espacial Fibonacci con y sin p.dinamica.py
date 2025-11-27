import tracemalloc #Librería para medir uso de memoria
import matplotlib.pyplot as plt # type: ignore

# Fibonacci sin Programación Dinámica (recursivo)
def fib_recursivo(n):
    # casos base
    if n <= 1:
        return n
    # llamada recursiva doble: exponencial en tiempo y uso de pila
    return fib_recursivo(n-1) + fib_recursivo(n-2)

# Fibonacci con Programación Dinámica
def fib_dinamico(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_dinamico(n-1, memo) + fib_dinamico(n-2, memo)
    return memo[n]

# Valores de n a probar (5,7,...,33)
n_values = list(range(5, 35, 2))
memoria_recursivo = []
memoria_dinamico = []

for n in n_values:
    # medir memoria usada por la ejecución del fib_recursivo
    tracemalloc.start()
    fib_recursivo(n)
    # get_traced_memory()[1] devuelve el pico de memoria rastreada (bytes)
    memoria_recursivo.append(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()

    # medir memoria usada por la ejecución del fib_dinamico
    tracemalloc.start()
    
    fib_dinamico(n, {})
    memoria_dinamico.append(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()

# Gráfica comparativa de memoria
plt.figure()
plt.plot(n_values, memoria_recursivo, marker="o", label="Sin Programación Dinámica")
plt.plot(n_values, memoria_dinamico, marker="o", label="Con Programación Dinámica")
plt.title("Complejidad Espacial - Fibonacci")
plt.xlabel("Valor de n")
plt.ylabel("Memoria utilizada (bytes)")
plt.legend()
plt.grid(True)
plt.show()
