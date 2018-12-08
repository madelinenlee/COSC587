package com.yektaie.graph.graphs;

import com.yektaie.graph.core.Edge;
import com.yektaie.graph.core.Graph;
import com.yektaie.graph.core.Vertex;
import com.yektaie.graph.io.GraphLoader;

import java.util.ArrayList;

public class EdgeListGraph<VertexType, EdgeType> extends BaseGraph<VertexType, EdgeType> {
    public EdgeListGraph() {
        super();
    }

    @Override
    protected String getGraphType() {
        return "Graph";
    }

    @Override
    public BaseGraph<VertexType, EdgeType> newInstance() {
        return new EdgeListGraph<>();
    }

    public EdgeListGraph(GraphLoader<VertexType, EdgeType> loader) {
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
    public int getMaximumEdgesCount(int verticesSize) {
        throw new RuntimeException();
    }

    @Override
    protected void setEdges(ArrayList<Edge<VertexType, EdgeType>> edges) {
        super.setEdges(edges);

        checkForDuplicatedEdges(edges);
    }

    private void checkForDuplicatedEdges(ArrayList<Edge<VertexType, EdgeType>> edges) {
        boolean[][] presence = new boolean[vertices.size()][];
        for (int i = 0; i < presence.length; i++) {
            presence[i] = new boolean[vertices.size()];
        }

        for (Edge<VertexType, EdgeType> edge : edges) {
            int i_from = vertices.indexOf(edge.getFromVertex());
            int i_to = vertices.indexOf(edge.getToVertex());

            if (presence[i_from][i_to] || (!isDirected() && presence[i_to][i_from])) {
                throw new RuntimeException(String.format("Duplicated edge between '%s' and '%s' found!", edge.getFromVertex().toString(), edge.getToVertex().toString()));
            }

            presence[i_from][i_to] = true;
            if (!isDirected()) {
                presence[i_to][i_from] = true;
            }
        }
    }
}
