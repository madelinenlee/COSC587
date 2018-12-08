package com.yektaie.graph.core;

import com.yektaie.graph.utils.Utils;

import java.util.ArrayList;

public class Edge<VertexType, EdgeType> {
    private boolean isDirected = false;
    private Vertex<VertexType, EdgeType> fromVertex = null;
    private Vertex<VertexType, EdgeType> toVertex = null;
    private EdgeType value = null;
    private Graph<VertexType, EdgeType> graph = null;

    public Edge(boolean isDirected) {
        this.isDirected = isDirected;
    }

    public Graph<VertexType, EdgeType> getGraph() {
        return graph;
    }

    public void setGraph(Graph<VertexType, EdgeType> graph) {
        this.graph = graph;
    }

    public boolean isDirected() {
        return isDirected;
    }

    public Vertex<VertexType, EdgeType> getFromVertex() {
        return fromVertex;
    }

    public void setFromVertex(Vertex<VertexType, EdgeType> fromVertex) {
        Utils.throwExceptionIfNonNull(this.fromVertex, "You can not change the value of this field.");
        this.fromVertex = fromVertex;
    }

    public Vertex<VertexType, EdgeType> getToVertex() {
        return toVertex;
    }

    public void setToVertex(Vertex<VertexType, EdgeType> toVertex) {
        Utils.throwExceptionIfNonNull(this.toVertex, "You can not change the value of this field.");
        this.toVertex = toVertex;
    }

    public EdgeType getValue() {
        return value;
    }

    public void setValue(EdgeType value) {
        this.value = value;
    }

    public boolean isSelfLoop() {
        return fromVertex == toVertex;
    }

    @Override
    public String toString() {
        if (value != null) {
            return String.format("%s ---%s---> %s", fromVertex.toString(), value.toString(), toVertex.toString());
        } else {
            return String.format("%s ------> %s", fromVertex.toString(), toVertex.toString());
        }
    }

    public Vertex<VertexType, EdgeType> getOtherVertex(Vertex<VertexType, EdgeType> vertex) {
        if (vertex == fromVertex) {
            return toVertex;
        }

        return fromVertex;
    }

    public double getBetweenness() {
        double result = 0;
        int pathsWithThisEdge = 0;
        int pathsCount = 0;

        for (Vertex<VertexType, EdgeType> a : graph.getVertices()) {
            for (Vertex<VertexType, EdgeType> b : graph.getVertices()) {
                if (a != b) {
                    ArrayList<Path<VertexType, EdgeType>> paths = graph.findShortestPathsBetween(a, b);
                    pathsCount+= paths.size();
                    for (Path<VertexType, EdgeType> path : paths) {
                        if (path.contains(this)) {
                            pathsWithThisEdge++;
                        }
                    }
                }
            }
        }

        result = pathsWithThisEdge * 1.0 / pathsCount;
        return result;
    }
}
