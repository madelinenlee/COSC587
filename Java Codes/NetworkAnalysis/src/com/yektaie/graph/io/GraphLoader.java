package com.yektaie.graph.io;

import com.yektaie.graph.core.Edge;
import com.yektaie.graph.core.Graph;
import com.yektaie.graph.core.Vertex;

import java.util.ArrayList;

public interface GraphLoader<VertexType, EdgeType> {
    void load(Graph<VertexType, EdgeType> graph);
    ArrayList<Vertex<VertexType, EdgeType>> getVertices();
    ArrayList<Edge<VertexType, EdgeType>> getEdges();
}
