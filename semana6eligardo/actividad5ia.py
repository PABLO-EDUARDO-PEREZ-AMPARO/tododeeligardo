import heapq
import math
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# --- Clases de Algoritmos Optimizadas ---

class WeightedGraph:
    """
    Clase para representar un grafo ponderado dirigido.
    Optimizado con defaultdict y Dijkstra sin lista 'visited'.
    """
    def __init__(self, n: int):
        self.n = n
        # Optimización sugerida por IA: Inicialización perezosa (defaultdict) para eficiencia espacial.
        self.adj: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    
    def add_edge(self, u: int, v: int, w: float):
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
             raise IndexError("Nodos fuera del rango definido del grafo.")
        self.adj[u].append((v, w))
    
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
            
            # Optimización sugerida por IA: Sustitución de 'visited'. Ignora caminos subóptimos.
            if cost > dist[u]: 
                continue
            
            for v, w in self.adj[u]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, parent
    
    def floyd_warshall(self) -> List[List[float]]:
        # Optimización sugerida por IA: Chequeo de robustez para grafo vacío.
        if self.n == 0:
            return []
            
        N = self.n
        dist = [[math.inf] * N for _ in range(N)]
        
        for i in range(N):
            dist[i][i] = 0
            # Optimización sugerida por IA: Inicialización concisa.
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
        
        # Detección de ciclos negativos
        for i in range(N):
            if dist[i][i] < 0:
                raise ValueError("Ciclo negativo detectado")
        
        return dist

# --- Funcionalidades de Análisis de Transporte (Pseudocódigo Implementado) ---

def calcular_tiempo_promedio(matriz_distancias: List[List[float]]) -> float:
    """Calcula el tiempo de viaje promedio entre todos los pares accesibles."""
    if not matriz_distancias:
        return 0.0
        
    total_distancia = 0.0
    conteo_pares = 0
    
    for i in range(len(matriz_distancias)):
        for j in range(len(matriz_distancias)):
            if i != j and matriz_distancias[i][j] != math.inf:
                total_distancia += matriz_distancias[i][j]
                conteo_pares += 1
                
    return total_distancia / conteo_pares if conteo_pares > 0 else math.inf

def simular_cierre_estacion(grafo_original: WeightedGraph, estacion_cerrada: int) -> List[List[float]]:
    """Simula el cierre de una estación eliminando todas las aristas relacionadas."""
    N = grafo_original.n
    
    # Crear un nuevo grafo (sin copiar la lógica de los métodos, solo la estructura)
    grafo_simulado = WeightedGraph(N)
    
    # Copiar solo las aristas que NO involucran a la estación cerrada
    for u in range(N):
        if u == estacion_cerrada:
            continue  # No copiamos aristas salientes de la estación cerrada
            
        for v, w in grafo_original.adj[u]:
            if v != estacion_cerrada:
                grafo_simulado.add_edge(u, v, w)
    
    # Recalcular la matriz de distancias completa con la nueva topología
    # NOTA: Los tiempos desde/hacia la estación cerrada serán INF
    matriz_impacto = grafo_simulado.floyd_warshall()
    
    return matriz_impacto

# --- Configuración del Ejemplo CDMX ---

estaciones_cdmx = {
    0: "Pantitlán", 1: "Balderas", 2: "Centro Médico", 3: "Insurgentes", 4: "Tacubaya"
}
N_NODOS = len(estaciones_cdmx)

grafo_transporte = WeightedGraph(N_NODOS)

# Aristas y Pesos (Tiempo en minutos)
# (u, v, peso)
aristas = [
    (0, 1, 10.0), (1, 0, 10.0),  # Pantitlán <-> Balderas (L1)
    (1, 3, 3.0), (3, 1, 3.0),    # Balderas <-> Insurgentes (L1)
    (3, 4, 4.0), (4, 3, 4.0),    # Insurgentes <-> Tacubaya (L1)
    (1, 2, 8.0), (2, 1, 8.0),    # Balderas <-> Centro Médico (L3/L9)
    (4, 2, 7.0), (2, 4, 7.0)     # Tacubaya <-> Centro Médico (L9/L3)
]

for u, v, w in aristas:
    grafo_transporte.add_edge(u, v, w)

# --- Ejecución del Análisis ---
print("==============================================")
print("📊 Análisis de Red de Transporte (CDMX Ejemplo)")
print("==============================================\n")

# 1. Tiempos desde una Estación Central (Dijkstra)
ESTACION_CENTRAL = 1  # Balderas
dist_balderas, _ = grafo_transporte.dijkstra(ESTACION_CENTRAL)

print(f"1. Tiempos desde la Central ({estaciones_cdmx[ESTACION_CENTRAL]}):")
for i, dist in enumerate(dist_balderas):
    if dist != math.inf:
        print(f"   -> {estaciones_cdmx[i]}: {dist:.1f} min")
print("-" * 40)

# 2. Precomputar Matriz Completa (Floyd-Warshall)
matriz_original = grafo_transporte.floyd_warshall()
tiempo_promedio_original = calcular_tiempo_promedio(matriz_original)

print("2. Matriz de Distancias (FW - Minutos):")
header = [f"{estaciones_cdmx[i][:3]}" for i in range(N_NODOS)]
print("     " + " ".join(f"{h:<5}" for h in header))
for i in range(N_NODOS):
    row_label = f"{estaciones_cdmx[i][:3]}:"
    row_values = [f"{v:.1f}" if v != math.inf else " INF" for v in matriz_original[i]]
    print(f"{row_label:<5} " + " ".join(f"{v:<5}" for v in row_values))
    
print(f"\nTiempo promedio de viaje (original): {tiempo_promedio_original:.2f} min")
print("-" * 40)


# 4. Simular Impacto de Cierre
ESTACION_CERRADA = 4 # Tacubaya (Nodo clave de transferencia)

matriz_impacto = simular_cierre_estacion(grafo_transporte, ESTACION_CERRADA)
tiempo_promedio_impacto = calcular_tiempo_promedio(matriz_impacto)
impacto_en_tiempo = tiempo_promedio_impacto - tiempo_promedio_original

print(f"4. Simulación: Cierre de {estaciones_cdmx[ESTACION_CERRADA]}:")
print(f"   Nuevo tiempo promedio: {tiempo_promedio_impacto:.2f} min")
print(f"   Impacto (Aumento): +{impacto_en_tiempo:.2f} min")

print(f"\nMatriz de Impacto (Rutas afectadas):")
print("     " + " ".join(f"{h:<5}" for h in header))
for i in range(N_NODOS):
    row_label = f"{estaciones_cdmx[i][:3]}:"
    row_values = []
    for j in range(N_NODOS):
        val = matriz_impacto[i][j]
        # Resaltar cambios si la distancia ha aumentado significativamente
        if val != math.inf and val > matriz_original[i][j] + 0.1:
             row_values.append(f"*{val:.1f}*") # Usar asteriscos para indicar aumento
        elif val == math.inf and matriz_original[i][j] != math.inf:
             row_values.append(" LOST")
        else:
             row_values.append(f" {val:.1f} ")
             
    print(f"{row_label:<5} " + " ".join(f"{v:<5}" for v in row_values))
print("==============================================")