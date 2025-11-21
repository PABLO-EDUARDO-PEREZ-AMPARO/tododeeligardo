import heapq
import math
from collections import defaultdict
from typing import Dict, List, Tuple

class WeightedGraph:
    def __init__(self, n: int):
        self.n = n
        # Optimización sugerida por IA: Inicialización perezosa (defaultdict) para eficiencia espacial en grafos dispersos.
        self.adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    
    def add_edge(self, u: int, v: int, w: float):
        # Asegura que el nodo u está dentro del rango definido, aunque defaultdict es flexible.
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
             raise IndexError("Nodos fuera del rango definido del grafo.")
        self.adj[u].append((v, w))
    
    # Dijkstra Optimizado (Origen Único)
    def dijkstra(self, src: int) -> Tuple[List[float], List[int]]:
        # Optimización sugerida por IA: Chequeo de robustez para nodo de origen.
        if src < 0 or src >= self.n:
             raise ValueError(f"Nodo de origen {src} fuera del rango [0, {self.n - 1}]")

        dist = [math.inf] * self.n
        parent = [-1] * self.n
        dist[src] = 0
        pq = [(0, src)]  # (distancia, nodo)
        
        while pq:
            cost, u = heapq.heappop(pq)
            
            # Optimización sugerida por IA: Sustitución de la lista 'visited' por un chequeo de costo.
            # Ignora nodos extraídos con un costo mayor al ya conocido (camino subóptimo).
            if cost > dist[u]: 
                continue
            
            # Relajación
            for v, w in self.adj[u]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, parent
    
    # Floyd-Warshall Mejorado (Todos los Pares)
    def floyd_warshall(self) -> List[List[float]]:
        # Optimización sugerida por IA: Chequeo de robustez para grafo vacío.
        if self.n == 0:
            raise ValueError("No se puede ejecutar Floyd-Warshall en un grafo sin nodos.")
            
        N = self.n
        dist = [[math.inf] * N for _ in range(N)]
        
        for i in range(N):
            dist[i][i] = 0
            # Optimización sugerida por IA: Inicialización concisa de la matriz,
            # combinando la inicialización a 0 y la carga de aristas iniciales.
            for v, w in self.adj[i]:
                dist[i][v] = w
        
        # Algoritmo principal (Iteración sobre el nodo intermedio k)
        for k in range(N):
            for i in range(N):
                for j in range(N):
                    # Relajación
                    # Se verifica la posibilidad de un camino más corto a través de k
                    sum_dist = dist[i][k] + dist[k][j]
                    if sum_dist < dist[i][j]:
                        dist[i][j] = sum_dist
        
        # Detección de ciclos negativos (Revisando la diagonal principal)
        for i in range(N):
            if dist[i][i] < 0:
                raise ValueError("Ciclo negativo detectado")
        
        return dist