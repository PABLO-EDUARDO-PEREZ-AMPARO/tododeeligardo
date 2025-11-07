using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

class Program
{
    static void Main()
    {
        Console.WriteLine("=== Análisis de Mapas de Tráfico - Proyecto Semana 3 ===");

        // ===============================
        // Carga de grafos desde archivos
        // ===============================
        var undirectedGraph = LoadGraph("edges_undirected.txt", isDirected: false);
        if (undirectedGraph != null)
        {
            AnalyzeGraph(undirectedGraph, "No Dirigido");

            // Extraer secuencia de grados y validar
            var degreeSeq = GraphValidator.ExtractDegreeSequence(undirectedGraph);
            Console.WriteLine($"\n📈 Secuencia de grados (No Dirigido): [{string.Join(", ", degreeSeq)}]");
            Console.WriteLine($"¿Es gráfica? {GraphValidator.IsGraphicalSequence(degreeSeq)}");
            Console.WriteLine($"¿Consistente? {GraphValidator.ValidateConsistency(undirectedGraph)}");
        }

        var directedGraph = LoadGraph("edges_directed.txt", isDirected: true);
        if (directedGraph != null)
        {
            AnalyzeGraph(directedGraph, "Dirigido");

            var degreeSeq = GraphValidator.ExtractDegreeSequence(directedGraph);
            Console.WriteLine($"\n📈 Secuencia de grados (Dirigido): [{string.Join(", ", degreeSeq)}]");
            Console.WriteLine($"¿Es gráfica? {GraphValidator.IsGraphicalSequence(degreeSeq)}");
        }

        // ===============================
        // Ejemplo de uso del validador
        // ===============================
        Console.WriteLine("\n=== Pruebas de secuencias gráficas (manuales) ===");
        var seq1 = new List<int> { 4, 3, 3, 2, 2, 2, 1, 1 };
        Console.WriteLine($"Secuencia: [{string.Join(", ", seq1)}] → ¿Gráfica? {GraphValidator.IsGraphicalSequence(seq1)}");

        var seq2 = new List<int> { 3, 3, 3, 1 };
        Console.WriteLine($"Secuencia: [{string.Join(", ", seq2)}] → ¿Gráfica? {GraphValidator.IsGraphicalSequence(seq2)}");
    }

    // ==============================================================
    // FUNCIONES DE ANÁLISIS DE GRAFOS
    // ==============================================================

    static Dictionary<string, List<(string, double)>>? LoadGraph(string filePath, bool isDirected)
    {
        var adjacencyList = new Dictionary<string, List<(string, double)>>();

        if (!File.Exists(filePath))
        {
            Console.WriteLine($"❌ Error: El archivo '{filePath}' no existe.");
            return null;
        }

        try
        {
            string[] lines = File.ReadAllLines(filePath);
            foreach (string rawLine in lines)
            {
                string line = rawLine.Trim();

                if (string.IsNullOrEmpty(line) || line.StartsWith("#"))
                    continue;

                string[] parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length < 2) continue;

                string fromVertex = parts[0];
                string toVertex = parts[1];
                double weight = 1.0;

                if (parts.Length > 2)
                    double.TryParse(parts[2], out weight);

                if (!adjacencyList.ContainsKey(fromVertex))
                    adjacencyList[fromVertex] = new List<(string, double)>();

                if (!adjacencyList.ContainsKey(toVertex))
                    adjacencyList[toVertex] = new List<(string, double)>();

                adjacencyList[fromVertex].Add((toVertex, weight));

                if (!isDirected)
                    adjacencyList[toVertex].Add((fromVertex, weight));
            }

            Console.WriteLine($"✅ Archivo '{filePath}' cargado exitosamente.");
            return adjacencyList;
        }
        catch (Exception e)
        {
            Console.WriteLine($"❌ Error inesperado al leer '{filePath}': {e.Message}");
            return null;
        }
    }

    static void AnalyzeGraph(Dictionary<string, List<(string, double)>> graph, string graphType)
    {
        Console.WriteLine($"\n==================================================");
        Console.WriteLine($"🔍 Análisis del Grafo {graphType}");
        Console.WriteLine($"==================================================");

        if (!graph.Any())
        {
            Console.WriteLine("⚠️ El grafo está vacío");
            return;
        }

        var vertices = graph.Keys.OrderBy(v => v).ToList();
        int n = vertices.Count;
        int edgeCount = graph.Values.Sum(list => list.Count);

        Console.WriteLine("📊 Estadísticas generales:");
        Console.WriteLine($"   • Vértices: {n}");

        double maxPossibleEdges;
        if (graphType == "No Dirigido")
        {
            int actualEdges = edgeCount / 2;
            Console.WriteLine($"   • Aristas: {actualEdges}");

            maxPossibleEdges = (double)(n * (n - 1)) / 2;
            if (maxPossibleEdges > 0)
            {
                double density = actualEdges / maxPossibleEdges;
                Console.WriteLine($"   • Densidad: {density:F3}");
            }
        }
        else
        {
            Console.WriteLine($"   • Aristas: {edgeCount}");

            maxPossibleEdges = n * (n - 1);
            if (maxPossibleEdges > 0)
            {
                double density = edgeCount / maxPossibleEdges;
                Console.WriteLine($"   • Densidad: {density:F3}");
            }
        }

        Console.WriteLine("\n🔍 Detalles por vértice:");
        foreach (var vertex in vertices)
        {
            var neighbors = graph.GetValueOrDefault(vertex, new List<(string, double)>());
            int outDeg = neighbors.Count;
            int inDeg = graph.Values.SelectMany(n => n).Count(edge => edge.Item1 == vertex);

            string neighborStr = string.Join(", ", neighbors.Select(n => $"{n.Item1}({n.Item2:F1}km)"));

            Console.WriteLine($"{vertex}: Out-degree={outDeg}, In-degree={inDeg}");
            Console.WriteLine($"   └─ Vecinos: [{neighborStr}]");
        }
    }
}

// ===============================================================
// CLASE: GraphValidator (equivalente al código Python)
// ===============================================================

public static class GraphValidator
{
    /// <summary>
    /// Valida si una secuencia es gráfica usando Havel-Hakimi.
    /// (Equivalente a is_graphical_sequence en Python)
    /// </summary>
    public static bool IsGraphicalSequence(List<int> degrees)
    {
        if (degrees.Count == 0) return true;

        var seq = new List<int>(degrees);
        seq.Sort((a, b) => b.CompareTo(a)); // Ordenar descendente

        int totalSum = seq.Sum();
        if (totalSum % 2 != 0) return false;

        while (seq.Count > 0)
        {
            int d1 = seq[0];
            seq.RemoveAt(0);

            if (d1 == 0) return true;
            if (d1 > seq.Count) return false;

            for (int i = 0; i < d1; i++)
            {
                seq[i]--;
                if (seq[i] < 0)
                    return false;
            }

            seq.Sort((a, b) => b.CompareTo(a));
        }

        return true;
    }

    /// <summary>
    /// Verifica consistencia: suma de grados debe ser par en grafo no dirigido.
    /// (Equivalente a validate_consistency en Python)
    /// </summary>
    public static bool ValidateConsistency(Dictionary<string, List<(string, double)>> graph)
    {
        int totalDegree = graph.Sum(kvp => kvp.Value.Count);
        return totalDegree % 2 == 0;
    }

    /// <summary>
    /// Extrae la secuencia de grados de un grafo.
    /// (Equivalente a extract_degree_sequence en Python)
    /// </summary>
    public static List<int> ExtractDegreeSequence(Dictionary<string, List<(string, double)>> graph)
    {
        var degrees = graph.Select(kvp => kvp.Value.Count).OrderByDescending(d => d).ToList();
        return degrees;
    }
}
