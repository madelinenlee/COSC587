package com.yektaie.graph.io.loaders;

import com.yektaie.graph.core.Edge;
import com.yektaie.graph.core.Graph;
import com.yektaie.graph.core.Vertex;
import com.yektaie.graph.io.Factory;
import com.yektaie.graph.io.GraphLoader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class SimpleCSVFileLoader<VertexType, EdgeType> implements GraphLoader<VertexType, EdgeType> {
    private final String filePath;
    private final boolean hasHeader;
    private ArrayList<Vertex<VertexType, EdgeType>> vertices = new ArrayList<>();
    private ArrayList<Edge<VertexType, EdgeType>> edges = new ArrayList<>();
    private HashMap<String, Vertex<VertexType, EdgeType>> nodeNameToNode = new HashMap<>();
    private Factory<VertexType> vertexTypeFactory = null;
    private Factory<EdgeType> edgeTypeFactory = null;

    public SimpleCSVFileLoader(String filePath, boolean hasHeader, Factory<VertexType> vertexTypeFactory, Factory<EdgeType> edgeTypeFactory) {
        this.filePath = filePath;
        this.hasHeader = hasHeader;

        this.vertexTypeFactory = vertexTypeFactory;
        this.edgeTypeFactory = edgeTypeFactory;
    }

    private void readCSVFile(String filePath, boolean hasHeader, Graph<VertexType, EdgeType> graph) {
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line = null;
            while ((line = br.readLine()) != null) {
                if (hasHeader) {
                    // Skip the header line
                    hasHeader = false;
                    continue;
                }

                processCSVLine(line, graph);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void processCSVLine(String line, Graph<VertexType, EdgeType> graph) {
        String[] parts = line.split(",");

        if (parts.length == 1) {
            Vertex<VertexType, EdgeType> from = getVertex(parts[0], graph);
            return;
        }

        Vertex<VertexType, EdgeType> from = getVertex(parts[0], graph);
        Vertex<VertexType, EdgeType> to = getVertex(parts[1], graph);
        Edge<VertexType, EdgeType> edge = createEdge(from, to, parts.length > 2 ? getEdgeValue(parts[2]) : null, graph);

        if (edge.isSelfLoop()) {
            from.addEdge(edge);
        } else {
            from.addEdge(edge);
            to.addEdge(edge);
        }

        edges.add(edge);
    }

    private EdgeType getEdgeValue(String value) {
        EdgeType r = null;

        try {
            r = edgeTypeFactory.newInstance(value);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        return r;
    }

    private Edge<VertexType,EdgeType> createEdge(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to, EdgeType value, Graph<VertexType, EdgeType> graph) {
        Edge<VertexType,EdgeType> result = new Edge<>(graph.isDirected());
        result.setGraph(graph);
        result.setFromVertex(from);
        result.setToVertex(to);
        result.setValue(value);

        return result;
    }

    private Vertex<VertexType, EdgeType> getVertex(String name, Graph<VertexType, EdgeType> graph) {
        if (nodeNameToNode.containsKey(name)) {
            return nodeNameToNode.get(name);
        }

        Vertex<VertexType, EdgeType> vertex = new Vertex<>();
        nodeNameToNode.put(name, vertex);

        vertex.setValue(toVertexValue(name));
        vertex.setGraph(graph);
        this.vertices.add(vertex);

        return vertex;
    }

    private VertexType toVertexValue(String name) {
        VertexType r = null;

        try {
            r = vertexTypeFactory.newInstance(name);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        return r;
    }

    @Override
    public void load(Graph<VertexType, EdgeType> graph) {
        readCSVFile(filePath, hasHeader, graph);
    }

    @Override
    public ArrayList<Vertex<VertexType, EdgeType>> getVertices() {
        return vertices;
    }

    @Override
    public ArrayList<Edge<VertexType, EdgeType>> getEdges() {
        return edges;
    }
}
