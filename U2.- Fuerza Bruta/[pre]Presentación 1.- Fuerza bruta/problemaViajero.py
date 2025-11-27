# Matriz 
distancias = [

    [1, 2, 3, 5], 
    [2, 1, 8, 7], 
    [3, 8, 1, 4], 
    [5, 7, 4, 1] 
]

mejorRuta = None
mejorCosto = 999999999  

def costoRuta(ruta, matriz):
    total = 0
    for i in range(len(ruta) - 1):
        total += matriz[ruta[i]][ruta[i+1]]
    return total

def rutas(ciudades, pos, matriz):
    global mejorRuta, mejorCosto

    if pos == len(ciudades):
        ruta = [0] + ciudades+[0]  
        costo = costoRuta(ruta, matriz)
        if costo < mejorCosto:
            mejorCosto = costo
            mejorRuta = ruta[:]
        return
    
    for i in range(pos, len(ciudades)):
        ciudades[pos], ciudades[i] = ciudades[i], ciudades[pos]
        rutas(ciudades, pos + 1, matriz)
        ciudades[pos], ciudades[i] = ciudades[i], ciudades[pos] 

def viajero(matriz):
    n = len(matriz)
    ciudades = list(range(1, n)) 
    rutas(ciudades, 0, matriz)
    return mejorRuta, mejorCosto

rutaTop, costoTop = viajero(distancias)
print("Mejor ruta encontrada:", rutaTop)
print("Con costo:", costoTop)
