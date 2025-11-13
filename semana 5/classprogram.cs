class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("=== DEMOSTRACIÓN BFS Y DFS ===\n");
        
        // Crear grafo de ejemplo (red social simplificada)
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        graph.AddEdge(1, 3);
        graph.AddEdge(2, 4);
        graph.AddEdge(2, 5);
        graph.AddEdge(3, 6);
        graph.AddEdge(5, 7);
        
        Console.WriteLine("Grafo: 1-2, 1-3, 2-4, 2-5, 3-6, 5-7");
        Console.WriteLine();
        
        // BFS
        Console.WriteLine("--- BFS desde nodo 1 ---");
        var bfsResult = graph.BFS(1);
        Console.WriteLine("Orden: " + string.Join(" → ", bfsResult));
        
        var distances = graph.BFSDistances(1);
        Console.WriteLine("Distancias desde 1:");
        foreach (var kvp in distances.OrderBy(x => x.Key))
        {
            Console.WriteLine($"  Nodo {kvp.Key}: {kvp.Value} aristas");
        }
        Console.WriteLine();
        
        // DFS
        Console.WriteLine("--- DFS desde nodo 1 ---");
        var dfsRecResult = graph.DFSRecursive(1);
        Console.WriteLine("Recursivo: " + string.Join(" → ", dfsRecResult));
        
        var dfsIterResult = graph.DFSIterative(1);
        Console.WriteLine("Iterativo: " + string.Join(" → ", dfsIterResult));
        Console.WriteLine();
        
        // Camino más corto
        Console.WriteLine("--- Camino más corto de 1 a 7 ---");
        var path = graph.BFSShortestPath(1, 7);
        Console.WriteLine("Camino: " + string.Join(" → ", path));
        Console.WriteLine($"Longitud: {path.Count - 1} aristas");
        Console.WriteLine();
        
        // Detección de ciclos (grafo dirigido)
        Console.WriteLine("--- Detección de Ciclos ---");
        var digraph = new GraphTraversal();
        digraph.AddDirectedEdge(1, 2);
        digraph.AddDirectedEdge(2, 3);
        digraph.AddDirectedEdge(3, 1); // Ciclo: 1→2→3→1
        digraph.AddDirectedEdge(3, 4);
        
        Console.WriteLine("Grafo dirigido: 1→2, 2→3, 3→1, 3→4");
        Console.WriteLine($"¿Tiene ciclo? {(digraph.HasCycleDirected() ? "SÍ" : "NO")}");
        Console.WriteLine();
        
        // Ordenamiento topológico (DAG)
        var dag = new GraphTraversal();
        dag.AddDirectedEdge(1, 2);
        dag.AddDirectedEdge(1, 3);
        dag.AddDirectedEdge(2, 4);
        dag.AddDirectedEdge(3, 4);
        
        Console.WriteLine("--- Ordenamiento Topológico ---");
        Console.WriteLine("DAG: 1→2, 1→3, 2→4, 3→4");
        var topoSort = dag.TopologicalSort();
        Console.WriteLine("Orden topológico: " + string.Join(" → ", topoSort));
        Console.WriteLine();
        
        // Componentes conectadas
        var disconnected = new GraphTraversal();
        disconnected.AddEdge(1, 2);
        disconnected.AddEdge(2, 3);
        disconnected.AddEdge(4, 5);
        disconnected.AddEdge(6, 7);
        disconnected.AddEdge(7, 8);
        
        Console.WriteLine("--- Componentes Conectadas ---");
        Console.WriteLine("Grafo: {1-2-3}, {4-5}, {6-7-8}");
        var components = disconnected.FindConnectedComponents();
        Console.WriteLine($"Número de componentes: {components.Count}");
        for (int i = 0; i < components.Count; i++)
        {
            Console.WriteLine($"  Componente {i + 1}: [{string.Join(", ", components[i].OrderBy(x => x))}]");
        }
    }
}