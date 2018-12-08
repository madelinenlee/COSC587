package com.yektaie.graph.graphs;

import com.yektaie.graph.core.*;
import com.yektaie.graph.io.GraphLoader;

import java.util.ArrayList;

public class MultiGraph<VertexType, EdgeType> extends BaseGraph<VertexType, EdgeType> {
    public MultiGraph() {
        super();
    }

    @Override
    protected String getGraphType() {
        return "MultiGraph";
    }

    public MultiGraph(GraphLoader<VertexType, EdgeType> loader) {
        super();

        loadGraph(loader);
    }

    @Override
    public int vertexCount() {
        return vertices.size();
    }

    @Override
    public int edgeCountCount() {
        return edges.size();
    }

    @Override
    public ArrayList<Vertex<VertexType, EdgeType>> getVertices() {
        return vertices;
    }

    @Override
    public ArrayList<Edge<VertexType, EdgeType>> getEdges() {
        return edges;
    }

    @Override
    public double getDensity() {
        throw new RuntimeException("Graph density is undefined for multi graphs!");
    }

    @Override
    public int getMaximumEdgesCount(int verticesSize) {
        return 5;
    }

    @Override
    public BaseGraph<VertexType, EdgeType> newInstance() {
        return new MultiGraph<>();
    }
}
