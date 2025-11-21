import pytest
import math
from weighted_graph import WeightedGraph  # Asumir archivo con clase

def test_dijkstra_simple():
    g = WeightedGraph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 5)
    g.add_edge(2, 3, 2)
    g.add_edge(1, 3, 3)
    
    dist, _ = g.dijkstra(0)
    assert dist[3] == 7
    assert math.isinf(dist[3]) == False

def test_dijkstra_zero_weight():
    g = WeightedGraph(3)
    g.add_edge(0, 1, 0)
    g.add_edge(1, 2, 5)
    
    dist, _ = g.dijkstra(0)
    assert dist[2] == 5

def test_dijkstra_disconnected():
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    dist, _ = g.dijkstra(0)
    assert math.isinf(dist[2])

def test_dijkstra_single_node():
    g = WeightedGraph(1)
    
    dist, _ = g.dijkstra(0)
    assert dist[0] == 0

def test_floyd_warshall_simple():
    g = WeightedGraph(3)
    g.add_edge(0, 1, 4)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 0, 3)
    
    fw = g.floyd_warshall()
    assert fw[0][2] == 5  # 0-1-2

def test_floyd_warshall_negative_no_cycle():
    g = WeightedGraph(3)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, -1)
    
    fw = g.floyd_warshall()
    assert fw[0][2] == 1

def test_floyd_warshall_negative_cycle():
    g = WeightedGraph(2)
    g.add_edge(0, 1, -2)
    g.add_edge(1, 0, -1)
    
    with pytest.raises(ValueError):
        g.floyd_warshall()

def test_floyd_warshall_disconnected():
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    fw = g.floyd_warshall()
    assert math.isinf(fw[0][2])

# Edge cases
def test_dijkstra_non_existent_src():
    g = WeightedGraph(1)
    with pytest.raises(IndexError):
        g.dijkstra(1)

def test_floyd_warshall_empty():
    g = WeightedGraph(0)
    with pytest.raises(ValueError):
        g.floyd_warshall()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])



# Contenido de pytest.py
from weighted_graph import WeightedGraph  # Esto falla si el archivo no existe