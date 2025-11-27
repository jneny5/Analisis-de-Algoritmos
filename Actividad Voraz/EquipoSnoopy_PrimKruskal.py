import heapq
from collections import defaultdict

class GrafoAutobuses:    
    def __init__(self):
        self.grafo = defaultdict(list)
        self.nodos = set()
        self.aristas = []
    
    def agregar_arista(self, u, v, peso):
        #Agrega una arista bidireccional al grafo
        self.grafo[u].append((v, peso))
        self.grafo[v].append((u, peso))
        self.nodos.add(u)
        self.nodos.add(v)
        self.aristas.append((peso, u, v))
    
    def obtener_nodos(self):
        return list(self.nodos)


class UnionFind: 
    def __init__(self, nodos):
        self.padre = {nodo: nodo for nodo in nodos}
        self.rango = {nodo: 0 for nodo in nodos}
    
    def encontrar(self, nodo):
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.encontrar(self.padre[nodo])
        return self.padre[nodo]
    
    def unir(self, u, v):
        raiz_u=self.encontrar(u)
        raiz_v=self.encontrar(v)
        
        if raiz_u==raiz_v:
            return False
        
        if self.rango[raiz_u] < self.rango[raiz_v]:
            self.padre[raiz_u] = raiz_v
        elif self.rango[raiz_u] > self.rango[raiz_v]:
            self.padre[raiz_v] = raiz_u
        else:
            self.padre[raiz_v]=raiz_u
            self.rango[raiz_u] += 1
        
        return True


def algoritmo_prim(grafo):
    nodos = grafo.obtener_nodos()
    if not nodos:
        return [], 0
    
    #inicializar
    inicio = nodos[0]
    visitados = {inicio}
    mst = []
    peso_total = 0
    
    #HEAP
    heap = []
    for vecino, peso in grafo.grafo[inicio]:
        heapq.heappush(heap, (peso, inicio, vecino))
    
    #construir MST
    while heap and len(visitados) < len(nodos):
        peso, u, v = heapq.heappop(heap)
        
        if v in visitados:
            continue
    
        visitados.add(v) #agrega arista al MST
        mst.append((u, v, peso))
        peso_total += peso
        
        for vecino, peso_arista in grafo.grafo[v]:  #agrega aristas del nuevo nodo
            if vecino not in visitados:
                heapq.heappush(heap, (peso_arista, v, vecino))
    
    return mst, peso_total


def algoritmo_kruskal(grafo):
    nodos = grafo.obtener_nodos()
    aristas = sorted(grafo.aristas)  #ordenar por peso
    
    uf = UnionFind(nodos)
    mst = []
    peso_total = 0
    
    for peso, u, v in aristas:
        if uf.unir(u, v):
            mst.append((u, v, peso))
            peso_total += peso
            
            if len(mst) == len(nodos) - 1: # MST completo cuando tiene n-1 aristas
                break
    
    return mst, peso_total


def algoritmo_dijkstra(grafo, origen):
    distancias = {nodo: float('inf') for nodo in grafo.obtener_nodos()}
    distancias[origen] = 0
    predecesores = {nodo: None for nodo in grafo.obtener_nodos()}
    
    #HEAP
    heap = [(0, origen)]
    visitados = set()
    
    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)
        
        if nodo_actual in visitados:
            continue
        
        visitados.add(nodo_actual)
        
        for vecino, peso in grafo.grafo[nodo_actual]:
            distancia = dist_actual + peso
            
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(heap, (distancia, vecino))
    
    return distancias, predecesores


def crear_red_guadalajara():
    grafo = GrafoAutobuses()
    
    conexiones = [
        ("Centro", "Minerva", 3.5),
        ("Centro", "Oblatos", 4.2),
        ("Centro", "Analco", 2.1),
        ("Minerva", "Chapalita", 5.8),
        ("Minerva", "Patria", 3.0),
        ("Chapalita", "Zapopan", 4.5),
        ("Zapopan", "Patria", 6.2),
        ("Oblatos", "Tlaquepaque", 5.5),
        ("Analco", "Tlaquepaque", 3.8),
        ("Patria", "Tlaquepaque", 7.0)
    ]
    
    for zona1, zona2, distancia in conexiones:
        grafo.agregar_arista(zona1, zona2, distancia)
    
    return grafo


def imprimir_resultados():
    print("=" * 70)
    print("SISTEMA DE OPTIMIZACIÓN DE RUTAS DE AUTOBUSES - GUADALAJARA")
    print("="*70)
    print()
    
    #crear grafo
    grafo = crear_red_guadalajara()
    
    print("RED DE TRANSPORTE ACTUAL")
    print("-"*70)
    print("Zonas conectadas:")
    zonas = grafo.obtener_nodos()
    print(f"  {', '.join(sorted(zonas))}")
    print(f"\nTotal de zonas: {len(zonas)}")
    print(f"Total de conexiones: {len(grafo.aristas)}")
    print()
    
    print("Conexiones existentes:")
    for peso, u, v in sorted(grafo.aristas):
        print(f"  {u} ↔ {v}: {peso} km")
    print()
    
    # Algoritmo de Prim
    print("=" *70)
    print("ALGORITMO DE PRIM (con HEAP)")
    print("=" * 70)
    mst_prim, peso_prim = algoritmo_prim(grafo)
    print("Rutas seleccionadas para el MST:")
    for u, v, peso in mst_prim:
        print(f"  {u} {v}: {peso} km")
    print(f"\nDistancia total minima: {peso_prim} km")
    print(f"   Rutas en el MST: {len(mst_prim)}")
    print()
    
    # Algoritmo de Kruskal
    print("=" * 70)
    print("ALGORITMO DE KRUSKAL (con Union-Find)")
    print("=" * 70)
    mst_kruskal, peso_kruskal = algoritmo_kruskal(grafo)
    print("Rutas seleccionadas para el MST:")
    for u, v, peso in mst_kruskal:
        print(f"  {u}  {v}: {peso} km")
    print(f"\nDistancia total minima: {peso_kruskal} km")
    print(f"   Rutas en el MST: {len(mst_kruskal)}")
    print()
    
    # Verificar consistencia
    print("=" * 70)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 70)
    if abs(peso_prim - peso_kruskal) < 0.01:
        print(f"   Peso total del MST: {peso_prim} km")
    else:
        print("Los pesos difieren")
    print()
    print("=" * 70)
    print("ALGORITMO DE DIJKSTRA(ruta minima)")
    print("=" * 70)
    origen = "Centro"
    distancias, predecesores = algoritmo_dijkstra(grafo, origen)
    
    print(f"Distancias mínimas desde '{origen}' a todas las zonas:\n")
    print(f"{'Destino':<15} {'Distancia':<12} {'Ruta'}")
    print("-" * 70)
    
    for destino in sorted(distancias.keys()):
        if distancias[destino] == float('inf'):
            print(f"{destino:<15} {'No disponible':<12} No alcanzable")
        else:
            ruta = []
            actual = destino
            while actual is not None:
                ruta.append(actual)
                actual = predecesores[actual]
            ruta.reverse()
            
            ruta_str = " ".join(ruta)
            print(f"{destino:<15} {distancias[destino]:<12.1f} {ruta_str}")
    
if __name__ == "__main__":
    imprimir_resultados()