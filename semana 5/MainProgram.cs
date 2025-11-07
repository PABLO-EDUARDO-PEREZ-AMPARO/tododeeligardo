using System;
using DataStructures.Week5;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Prueba de GraphTraversal ===\n");

        var g = new GraphTraversal();

        // Agregamos aristas de prueba
        g.AddEdge(1, 2);
        g.AddEdge(2, 3);
        g.AddEdge(3, 4);
        g.AddEdge(4, 1);

        // Prueba de BFS
        var bfs = g.BFS(1);
        Console.WriteLine("BFS desde 1: " + string.Join(", ", bfs));

        // Prueba de DFS
        var dfs = g.DFSIterative(1);
        Console.WriteLine("DFS desde 1: " + string.Join(", ", dfs));

        Console.WriteLine("\nCompilación y ejecución correctas ✅");
    }
}
