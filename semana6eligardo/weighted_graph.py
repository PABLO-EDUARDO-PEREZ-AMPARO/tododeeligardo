import heapq
import math
from collections import defaultdict
from typing import Dict, List, Tuple

class WeightedGraph:
    def __init__(self, n: int):
        self.n = n
        # MEJORA (Eficiencia/Espacio): Usar defaultdict
        self.adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    
    def add_edge(self, u: int, v: int, w: float):
        self.adj[u].append((v, w))
    
    # Dijkstra Optimizado (Eliminación de 'visited')
    def dijkstra(self, src: int) -> Tuple[List[float], List[int]]:
        # MEJORA (Robustez): Chequeo del nodo fuente
        if src < 0 or src >= self.n:
             raise ValueError(f"Nodo de origen {src} fuera del rango [0, {self.n - 1}]")

        dist = [math.inf] * self.n
        parent = [-1] * self.n
        dist[src] = 0
        pq = [(0, src)]  # (dist, node)
        
        while pq:
            cost, u = heapq.heappop(pq)
            
            # MEJORA (Eficiencia): Ignorar si ya encontramos un camino más corto a 'u'
            if cost > dist[u]: 
                continue
            
            for v, w in self.adj[u]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, parent
    
    # Floyd-Warshall Mejorado (Inicialización Concisa)
    def floyd_warshall(self) -> List[List[float]]:
        # MEJORA (Robustez): Chequeo de grafo vacío
        if self.n == 0:
            raise ValueError("No se puede ejecutar Floyd-Warshall en un grafo sin nodos.")
            
        N = self.n
        # Inicialización de la matriz de distancias
        dist = [[math.inf] * N for _ in range(N)]
        
        for i in range(N):
            dist[i][i] = 0
            # MEJORA (Claridad): Incluir aristas conocidas
            for v, w in self.adj[i]:
                dist[i][v] = w
        
        # Algoritmo principal
        for k in range(N):
            for i in range(N):
                for j in range(N):
                    # Relajación
                    sum_dist = dist[i][k] + dist[k][j]
                    if sum_dist < dist[i][j]:
                        dist[i][j] = sum_dist
        
        # Detectar ciclos negativos
        for i in range(N):
            if dist[i][i] < 0:
                raise ValueError("Ciclo negativo detectado")
        
        return dist

# Ejemplo de uso
g = WeightedGraph(6)
g.add_edge(0,1,10); g.add_edge(0,2,5)
g.add_edge(1,3,3); g.add_edge(2,3,2); g.add_edge(2,4,8)
g.add_edge(3,4,4); g.add_edge(1,5,15); g.add_edge(4,5,7)

dist, parent = g.dijkstra(0)
print(f"Dijkstra dist 0-5: {dist[5]}") 
# Camino: 0 -> 2 (5) -> 3 (2) -> 4 (4) -> 5 (7) = 18

fw = g.floyd_warshall()
print(f"FW dist 0-5: {fw[0][5]}")