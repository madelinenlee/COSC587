package com.yektaie.graph.core;

import java.util.ArrayList;

public interface Graph<VertexType, EdgeType> {
    int vertexCount();

    int edgeCountCount();

    boolean isDirected();

    ArrayList<Vertex<VertexType, EdgeType>> getVertices();

    ArrayList<Edge<VertexType, EdgeType>> getEdges();

    void printGraphSummary();

    String getGraphSummary();

    ArrayList<Path<VertexType, EdgeType>> findPathsBetween(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to);

    ArrayList<Path<VertexType, EdgeType>> findShortestPathsBetween(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to);

    ArrayList<Path<VertexType, EdgeType>> getDiameterPath();

    double getDensity();

    ArrayList<Graph<VertexType, EdgeType>> getConnectedComponents();

    Vertex<VertexType, EdgeType> getVertex(VertexType value);

    int[][] getConnectionMatrix();

    Graph<VertexType, EdgeType> clone();

    void removeEdges(ArrayList<Edge<VertexType, EdgeType>> edges);

    int getMaximumEdgesCount(int verticesSize);

    void addVertex(VertexType vertex);

    void addEdge(VertexType vertexFrom, VertexType vertexTo, EdgeType value);

    void bfs(VertexType startPoint, IGraphExploration<VertexType, EdgeType> visitCallback);
}
