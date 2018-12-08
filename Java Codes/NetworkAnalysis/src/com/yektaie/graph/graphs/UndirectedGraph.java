package com.yektaie.graph.graphs;

import com.yektaie.graph.io.GraphLoader;

public class UndirectedGraph<VertexType, EdgeType> extends EdgeListGraph<VertexType, EdgeType> {
    public UndirectedGraph() {
        super();

        this.isDirected = false;
    }

    public UndirectedGraph(GraphLoader<VertexType, EdgeType> loader) {
        super();

        this.isDirected = false;
        loadGraph(loader);
    }

    @Override
    protected String getGraphType() {
        return "Graph";
    }

    @Override
    public BaseGraph<VertexType, EdgeType> newInstance() {
        return new UndirectedGraph<>();
    }

    @Override
    public int getMaximumEdgesCount(int verticesSize) {
        return verticesSize * (verticesSize-1) / 2;
    }
}
