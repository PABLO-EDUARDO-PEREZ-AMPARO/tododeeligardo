using Xunit;

public class GraphTraversalTests
{
    [Fact]
    public void BFS_SimpleGraph_ReturnsCorrectOrder()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        graph.AddEdge(1, 3);
        graph.AddEdge(2, 4);
        
        var result = graph.BFS(1);
        
        Assert.Equal(new[] { 1, 2, 3, 4 }, result);
    }
    
    [Fact]
    public void BFS_FindsShortestPath()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        graph.AddEdge(1, 3);
        graph.AddEdge(2, 4);
        graph.AddEdge(3, 4);
        graph.AddEdge(4, 5);
        
        var path = graph.BFSShortestPath(1, 5);
        
        Assert.NotNull(path);
        Assert.Equal(4, path.Count);  // Longitud 3 aristas
        Assert.Equal(1, path[0]);
        Assert.Equal(5, path[^1]);
    }
    
    [Fact]
    public void DFS_DetectsCycleInDirectedGraph()
    {
        var graph = new GraphTraversal();
        graph.AddDirectedEdge(1, 2);
        graph.AddDirectedEdge(2, 3);
        graph.AddDirectedEdge(3, 1);  // Ciclo
        
        Assert.True(graph.HasCycleDirected());
    }
    
    [Fact]
    public void TopologicalSort_OnDAG_ReturnsValidOrder()
    {
        var graph = new GraphTraversal();
        graph.AddDirectedEdge(1, 2);
        graph.AddDirectedEdge(1, 3);
        graph.AddDirectedEdge(2, 4);
        graph.AddDirectedEdge(3, 4);
        
        var order = graph.TopologicalSort();
        
        Assert.NotNull(order);
        Assert.Equal(1, order[0]);  // 1 debe ser primero
        Assert.Equal(4, order[^1]); // 4 debe ser último
    }
    
    [Fact]
    public void FindConnectedComponents_ThreeComponents()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        graph.AddEdge(3, 4);
        graph.AddEdge(5, 6);
        
        var components = graph.FindConnectedComponents();
        
        Assert.Equal(3, components.Count);
    }
    
    // ========================================
    // TESTS PARA CASOS LÍMITE (EDGE CASES)
    // ========================================
    
    [Fact]
    public void BFS_NonExistentNode_ThrowsException()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        
        Assert.Throws(() => graph.BFS(99));
    }
    
    [Fact]
    public void DFS_NonExistentNode_ThrowsException()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        
        Assert.Throws(() => graph.DFSRecursive(99));
        Assert.Throws(() => graph.DFSIterative(99));
    }
    
    [Fact]
    public void BFS_EmptyGraph_ThrowsException()
    {
        var graph = new GraphTraversal();
        
        Assert.Throws(() => graph.BFS(1));
    }
    
    [Fact]
    public void BFS_SingleNode_ReturnsOneNode()
    {
        var graph = new GraphTraversal();
        // Agregar nodo aislado
        graph.AddEdge(1, 1); // Self-loop (o simplemente crear nodo manualmente)
        
        var result = graph.BFS(1);
        
        Assert.Single(result);
        Assert.Equal(1, result[0]);
    }
    
    [Fact]
    public void DFS_IsolatedNode_ReturnsOneNode()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 1); // Nodo aislado con self-loop
        
        var result = graph.DFSRecursive(1);
        
        Assert.Single(result);
    }
    
    [Fact]
    public void BFS_DisconnectedGraph_VisitsOnlyReachableNodes()
    {
        var graph = new GraphTraversal();
        graph.AddEdge(1, 2);
        graph.AddEdge(3, 4);
        
        var result = graph.BFS(1);
        
        Assert.Equal(2, result.Count);
        Assert.Contains(1, result);
        Assert.Contains(2, result);
        Assert.DoesNotContain(3, result);
        Assert.DoesNotContain(4, result);
    }
}