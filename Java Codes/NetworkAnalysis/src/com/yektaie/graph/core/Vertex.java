package com.yektaie.graph.core;

import com.yektaie.graph.graphs.MultiGraph;
import com.yektaie.graph.utils.Utils;

import java.util.ArrayList;

public class Vertex<VertexType, EdgeType> {
    private VertexType value = null;
    private Graph<VertexType, EdgeType> graph = null;
    private ArrayList<Edge<VertexType, EdgeType>> edges = new ArrayList<>();

    public Vertex() {
        this(null, null);
    }

    public Vertex(VertexType value) {
        this(null, value);
    }

    public Vertex(Graph<VertexType, EdgeType> graph) {
        this(graph, null);
    }

    public Vertex(Graph<VertexType, EdgeType> graph, VertexType value) {
        setGraph(graph);
        setValue(value);
    }

    public VertexType getValue() {
        return value;
    }

    public void setValue(VertexType value) {
        this.value = value;
    }

    public Graph<VertexType, EdgeType> getGraph() {
        return graph;
    }

    public void setGraph(Graph<VertexType, EdgeType> graph) {
        Utils.throwExceptionIfNonNull(this.graph, "You can not change the parent of a node after it is set.");
        this.graph = graph;
    }

    @Override
    public String toString() {
        return value.toString();
    }

    public void addEdge(Edge<VertexType, EdgeType> edge) {
        this.edges.add(edge);
    }

    public ArrayList<Edge<VertexType, EdgeType>> getEdges() {
        return edges;
    }

    public ArrayList<Edge<VertexType, EdgeType>> getOutEdges() {
        if (!graph.isDirected()) {
            throw new RuntimeException("This operation is only valid for directed graphs.");
        }

        ArrayList<Edge<VertexType, EdgeType>> result = new ArrayList<>();

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (edge.getFromVertex() == this) {
                result.add(edge);
            }
        }

        return result;
    }

    public ArrayList<Edge<VertexType, EdgeType>> getInEdges() {
        if (!graph.isDirected()) {
            throw new RuntimeException("This operation is only valid for directed graphs.");
        }

        ArrayList<Edge<VertexType, EdgeType>> result = new ArrayList<>();

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (edge.getToVertex() == this) {
                result.add(edge);
            }
        }

        return result;
    }

    public int getDegree() {
        return edges.size();
    }

    public int getInDegree() {
        int result = 0;

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (edge.getToVertex() == this) {
                result++;
            }
        }

        return result;
    }

    public int getOutDegree() {
        int result = 0;

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (edge.getFromVertex() == this) {
                result++;
            }
        }

        return result;
    }

    public boolean isSinkVertex() {
        return getOutDegree() == 0;
    }

    public boolean isSourceVertex(){
        return getInDegree() == 0;
    }

    public boolean isDisconnectedVertex() {
        return getDegree() == 0;
    }

    public double getClusteringCoefficient() {
        if (graph instanceof MultiGraph ) {
            throw new RuntimeException("Clustering coefficient for multi graph is not defined.");
        }

        ArrayList<Vertex<VertexType, EdgeType>> neibors = getNeibors();

        if (neibors.size() == 0) {
            throw new RuntimeException("Clustering coefficient for an isolated node is not defined.");
        }

        int neiborsConnection = 0;
        int neiborsPossibleConnection = neibors.size()*(neibors.size()-1);
        if (!graph.isDirected()) {
            neiborsPossibleConnection/=2;
        }

        for (Vertex<VertexType, EdgeType> vertex : neibors) {
            for (Edge<VertexType, EdgeType> edge : vertex.edges) {
                if (neibors.contains(edge.getFromVertex()) && neibors.contains(edge.getToVertex())) {
                    neiborsConnection++;
                }
            }
        }

        neiborsConnection = neiborsConnection / 2;
        return neiborsConnection * 1.0 / neiborsPossibleConnection;
    }

    private ArrayList<Vertex<VertexType, EdgeType>> getNeibors() {
        ArrayList<Vertex<VertexType, EdgeType>> result = new ArrayList<>();

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (!edge.isSelfLoop()) {
                Vertex<VertexType, EdgeType> n = edge.getOtherVertex(this);
                if (!result.contains(n) ) {
                    result.add(n);
                }
            }
        }

        return result;
    }

    public double getBetweenness() {
        double result = 0;
        int pathsWithThisVertex = 0;
        int pathsCount = 0;

        for (Vertex<VertexType, EdgeType> a : graph.getVertices()) {
            for (Vertex<VertexType, EdgeType> b : graph.getVertices()) {
                if (a != b && a != this && b != this) {
                    ArrayList<Path<VertexType, EdgeType>> paths = graph.findShortestPathsBetween(a, b);
                    pathsCount+= paths.size();
                    for (Path<VertexType, EdgeType> path : paths) {
                        if (path.containsVertex(this)) {
                            pathsWithThisVertex++;
                        }
                    }
                }
            }
        }

        result = pathsWithThisVertex * 1.0 / pathsCount;
        return result;
    }
}
