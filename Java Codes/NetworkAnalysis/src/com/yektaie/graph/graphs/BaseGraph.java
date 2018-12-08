package com.yektaie.graph.graphs;

import com.yektaie.graph.core.*;
import com.yektaie.graph.io.GraphLoader;
import com.yektaie.graph.utils.Utils;

import java.util.ArrayList;
import java.util.HashMap;

public abstract class BaseGraph<VertexType, EdgeType> implements Graph<VertexType, EdgeType> {
    protected boolean isDirected = true;
    protected ArrayList<Vertex<VertexType, EdgeType>> vertices = null;
    protected ArrayList<Edge<VertexType, EdgeType>> edges = null;
    private HashMap<Vertex<VertexType, EdgeType>, HashMap<Vertex<VertexType, EdgeType>, ArrayList<Path<VertexType, EdgeType>>>> cachedShortestPath= new HashMap<>();


    public BaseGraph() {
        vertices = new ArrayList<>();
        edges = new ArrayList<>();
    }

    protected void loadGraph(GraphLoader<VertexType, EdgeType> loader) {
        loader.load(this);

        setVertices(loader.getVertices());
        setEdges(loader.getEdges());
    }

    @Override
    public boolean isDirected() {
        return isDirected;
    }

    protected void setVertices(ArrayList<Vertex<VertexType, EdgeType>> vertices) {
        this.vertices = vertices;
    }

    protected void setEdges(ArrayList<Edge<VertexType, EdgeType>> edges) {
        Utils.throwExceptionIfNull(vertices, "You should set list of vertices first.");

        this.edges = edges;
    }

    public void printGraphSummary() {
        System.out.println(getGraphSummary());
    }

    public String getGraphSummary() {
        StringBuilder result = new StringBuilder();

        result.append(String.format("Graph Type: %s (%s)", getGraphType(), isDirected() ? "Directed" : "Undirected"));
        result.append(String.format("\nTotal Node Count: %d", vertices.size()));
        result.append(String.format("\nTotal Edge Count: %d", edges.size()));

        addVerticesSummary(result);

        return result.toString();
    }

    private void addVerticesSummary(StringBuilder result) {
        double degree = 0, inDegree = 0, outDegree = 0;
        result.append("\nGraph Vertices:");
        int i = 0;

        for (Vertex<VertexType, EdgeType> vertex : vertices) {
            degree += vertex.getDegree();

            if (isDirected()) {
                inDegree += vertex.getInDegree();
                outDegree += vertex.getOutDegree();

                String sinkSource = "";
                if (vertex.isDisconnectedVertex()) {
                    sinkSource = " Disconnected Vertex";
                } else if (vertex.isSinkVertex()) {
                    sinkSource = " Sink Vertex";
                } else if (vertex.isSourceVertex()) {
                    sinkSource = " Source Vertex";
                }

                result.append(String.format("\n\t[%d] \"%s\" (in: %d, out: %d)%s", i, vertex.getValue().toString(), vertex.getInDegree(), vertex.getOutDegree(), sinkSource));
            } else {
                result.append(String.format("\n\t[%d] \"%s\" (degree: %d)", i, vertex.getValue().toString(), vertex.getDegree()));
            }

            double clusteringCoef = -1;
            try {
                clusteringCoef = vertex.getClusteringCoefficient();
            } catch (Exception ignored) { }

            result.append(String.format(" [betweenness: %.3f, clustering coef: %.3f]", vertex.getBetweenness(), clusteringCoef));
            i++;
        }

        degree /= vertices.size();
        if (isDirected()) {
            inDegree /= vertices.size();
            outDegree /= vertices.size();
            result.append(String.format("\nAverage Node Degree: %.3f (in: %.3f, out: %.3f)", degree, inDegree, outDegree));
        } else {
            result.append(String.format("\nAverage Node Degree: %.3f ", degree));
        }
    }

    @Override
    public String toString() {
        return getGraphSummary();
    }

    protected abstract String getGraphType();

    public ArrayList<Path<VertexType, EdgeType>> findShortestPathsBetween(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to) {
        if (cachedShortestPath.containsKey(from)) {
            HashMap<Vertex<VertexType, EdgeType>, ArrayList<Path<VertexType, EdgeType>>> paths = cachedShortestPath.get(from);
            if (paths.containsKey(to)) {
                return paths.get(to);
            } else {
                paths.put(to, new ArrayList<>());
            }
        } else {
            cachedShortestPath.put(from, new HashMap<>());
        }

        ArrayList<Path<VertexType, EdgeType>> paths = findPathsBetween(from, to, new Path<>(), true, 100000);

        if (paths == null) {
            cachedShortestPath.get(from).put(to, null);
            return null;
        }

        ArrayList<Path<VertexType, EdgeType>> result = Utils.getShortestPath(paths);
        cachedShortestPath.get(from).put(to, result);

        return result;
    }

    public ArrayList<Path<VertexType, EdgeType>> findPathsBetween(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to) {
        return findPathsBetween(from, to, new Path<>(), false, 100000);
    }

    private ArrayList<Path<VertexType, EdgeType>> findPathsBetween(Vertex<VertexType, EdgeType> from, Vertex<VertexType, EdgeType> to, Path<VertexType, EdgeType> path, boolean shortest, int currentShortestLength) {
        if (from == to) {
            // found a path
            ArrayList<Path<VertexType, EdgeType>> list = new ArrayList<>();
            list.add(path);

            return list;
        }

        if (shortest && path.size() >= currentShortestLength) {
            return null;
        }

        ArrayList<Path<VertexType, EdgeType>> result = new ArrayList<>();
        for (Edge<VertexType, EdgeType> edge : from.getEdges()) {
            if (edge.isSelfLoop()) {
                continue;
            }

            Vertex<VertexType, EdgeType> tmpFrom = null;

            if (isDirected() && edge.getFromVertex() == from) {
                tmpFrom = edge.getToVertex();
            } else if (!isDirected()) {
                tmpFrom = edge.getOtherVertex(from);
                if (path.containsVertex(tmpFrom)) {
                    continue;
                }
            } else {
                continue;
            }

            Path<VertexType, EdgeType> tmpPath = path.duplicate();
            tmpPath.add(edge);

            if (path.hasDuplicateVertex()) {
                return null;
            }

            ArrayList<Path<VertexType, EdgeType>> pathFromHere = findPathsBetween(tmpFrom, to, tmpPath, shortest, currentShortestLength);
            if (pathFromHere != null) {
                for (Path<VertexType, EdgeType> p : pathFromHere) {
                    result.add(p);

                    if (currentShortestLength > p.size()) {
                        currentShortestLength = p.size();
                    }
                }
            }
        }

        return result;
    }

    public ArrayList<Path<VertexType, EdgeType>> getDiameterPath() {
        ArrayList<Path<VertexType, EdgeType>> paths = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> vertex1 : vertices) {
            for (Vertex<VertexType, EdgeType> vertex2 : vertices) {
                paths.addAll(findPathsBetween(vertex1, vertex2));
            }
        }

        return Utils.getLongestPath(paths);
    }

    @Override
    public double getDensity() {
        int totalPossibleEdges = vertices.size() - 1;

        if (isDirected()) {
            totalPossibleEdges *= vertices.size();
        }

        return edges.size() * 1.0 / totalPossibleEdges;
    }

    public abstract BaseGraph<VertexType, EdgeType> newInstance();

    @Override
    public ArrayList<Graph<VertexType, EdgeType>> getConnectedComponents() {
        ArrayList<Graph<VertexType, EdgeType>> result = new ArrayList<>();
        boolean[] verticesSelected = new boolean[vertices.size()];

        int index = 0;
        while ((index = getNextVertexToProcess(verticesSelected)) != -1) {
            Graph<VertexType, EdgeType> component = getConnectedComponentAndUpdateVerticesList(vertices.get(index), verticesSelected);
            result.add(component);
        }

        return result;
    }

    private Graph<VertexType, EdgeType> getConnectedComponentAndUpdateVerticesList(Vertex<VertexType, EdgeType> vertex, boolean[] verticesSelected) {
        ArrayList<Vertex<VertexType, EdgeType>> vertices = new ArrayList<>();
        ArrayList<Edge<VertexType, EdgeType>> edges = new ArrayList<>();

        growConnectedComponent(vertex, vertices, edges);

        for (Vertex<VertexType, EdgeType> v : vertices) {
            verticesSelected[this.vertices.indexOf(v)] = true;
        }

        return createSubGraphFrom(vertices, edges);
    }

    public BaseGraph<VertexType, EdgeType> createSubGraphFrom(ArrayList<Vertex<VertexType, EdgeType>> vertices, ArrayList<Edge<VertexType, EdgeType>> edges) {
        BaseGraph<VertexType, EdgeType> result = newInstance();

        ArrayList<Vertex<VertexType, EdgeType>> finalVertices = new ArrayList<>();
        ArrayList<Edge<VertexType, EdgeType>> finalEdges = new ArrayList<>();
        HashMap<VertexType, Vertex<VertexType, EdgeType>> finalVerticesMap = new HashMap<>();

        for (Vertex<VertexType, EdgeType> vertex : vertices) {
            Vertex<VertexType, EdgeType> _v = new Vertex<>();
            _v.setGraph(result);
            _v.setValue(vertex.getValue());

            finalVertices.add(_v);
            finalVerticesMap.put(vertex.getValue(), _v);
        }

        for (Edge<VertexType, EdgeType> edge : edges) {
            Edge<VertexType, EdgeType> _e = new Edge<>(isDirected());
            _e.setValue(edge.getValue());
            _e.setGraph(result);
            _e.setFromVertex(finalVerticesMap.get(edge.getFromVertex().getValue()));
            _e.setToVertex(finalVerticesMap.get(edge.getToVertex().getValue()));

            if (_e.isSelfLoop()) {
                _e.getFromVertex().addEdge(_e);
            } else {
                _e.getFromVertex().addEdge(_e);
                _e.getToVertex().addEdge(_e);
            }

            finalEdges.add(_e);
        }


        result.setVertices(finalVertices);
        result.setEdges(finalEdges);

        return result;
    }

    private void growConnectedComponent(Vertex<VertexType, EdgeType> vertex, ArrayList<Vertex<VertexType, EdgeType>> vertices, ArrayList<Edge<VertexType, EdgeType>> edges) {
        if (vertices.contains(vertex)) {
            return;
        }

        vertices.add(vertex);
        ArrayList<Edge<VertexType, EdgeType>> outEdges = vertex.getEdges();

        for (Edge<VertexType, EdgeType> edge : outEdges) {
            if (isDirected() && edge.getFromVertex() == vertex) {
                if (!edges.contains(edge)) {
                    edges.add(edge);
                }

                growConnectedComponent(edge.getToVertex(), vertices, edges);
            } else if (!isDirected()) {
                if (!edges.contains(edge)) {
                    edges.add(edge);
                }

                growConnectedComponent(edge.getOtherVertex(vertex), vertices, edges);
            }
        }
    }

    private int getNextVertexToProcess(boolean[] verticesSelected) {
        int result = -1;

        for (int i = 0; i < verticesSelected.length; i++) {
            if (!verticesSelected[i]) {
                result = i;
                break;
            }
        }

        return result;
    }

    public Vertex<VertexType, EdgeType> getVertex(VertexType value) {
        Vertex<VertexType, EdgeType> result = null;

        for (Vertex<VertexType, EdgeType> vertex : vertices) {
            if (vertex.getValue().equals(value)) {
                result = vertex;
                break;
            }
        }

        return result;
    }

    public int[][] getConnectionMatrix() {
        int[][] result = initializeConnectionMatrix();

        for (int iu = 0; iu < vertices.size(); iu++) {
            Vertex<VertexType, EdgeType> u = vertices.get(iu);
            for (int iv = 0; iv < vertices.size(); iv++) {
                Vertex<VertexType, EdgeType> v = vertices.get(iv);

                if (iu != iv) {
                    if (areVerticesDirectlyConnected(u,v)) {
                        result[iu][iv] = 1;
                    }
                }
            }
        }

        return result;
    }

    private boolean areVerticesDirectlyConnected(Vertex<VertexType, EdgeType> u, Vertex<VertexType, EdgeType> v) {
        for (Edge<VertexType, EdgeType> edge : u.getEdges()) {
            if (edge.getToVertex() == v) {
                return true;
            }
        }

        if (!isDirected()) {
            for (Edge<VertexType, EdgeType> edge : v.getEdges()) {
                if (edge.getToVertex() == u) {
                    return true;
                }
            }
        }

        return false;
    }

    private int[][] initializeConnectionMatrix() {
        int[][] result = new int[vertices.size()][];
        for (int i = 0; i < result.length; i++) {
            result[i] = new int[vertices.size()];
        }
        return result;
    }

    public Graph<VertexType, EdgeType> clone() {
        return createSubGraphFrom(vertices, edges);
    }

    public void removeEdges(ArrayList<Edge<VertexType, EdgeType>> edges) {
        this.edges.removeAll(edges);

        for (Edge<VertexType, EdgeType> edge : edges) {
            edge.getFromVertex().getEdges().remove(edge);
            edge.getToVertex().getEdges().remove(edge);
        }
    }

    public void addVertex(VertexType value) {
        Vertex<VertexType, EdgeType> vertex = new Vertex<>();
        vertex.setGraph(this);
        vertex.setValue(value);

        vertices.add(vertex);
    }

    public void addEdge(VertexType vertexFrom, VertexType vertexTo, EdgeType value) {
        if (!isDirected() && existsEdge(vertexTo, vertexFrom)) {
            return;
        }

        Edge<VertexType, EdgeType> edge = new Edge<>(isDirected());
        edge.setGraph(this);
        edge.setValue(value);
        edge.setFromVertex(getVertex(vertexFrom));
        edge.setToVertex(getVertex(vertexTo));

        edge.getFromVertex().addEdge(edge);
        edge.getToVertex().addEdge(edge);

        edges.add(edge);
    }

    private boolean existsEdge(VertexType from, VertexType to) {
        boolean result = false;

        for (Edge<VertexType, EdgeType> edge : edges) {
            if (edge.getFromVertex().getValue().equals(from) && edge.getToVertex().getValue().equals(to)) {
                result = true;
                break;
            }
        }


        return result;
    }

    public void bfs(VertexType startPoint, IGraphExploration<VertexType, EdgeType> visitCallback) {
        Vertex<VertexType, EdgeType> startVertex = getVertex(startPoint);

        ArrayList<Vertex<VertexType, EdgeType>> notVisitedPoints = new ArrayList<>(vertices);
        doBFS(startVertex, notVisitedPoints, visitCallback);
    }

    private void doBFS(Vertex<VertexType, EdgeType> vertex, ArrayList<Vertex<VertexType, EdgeType>> notVisitedPoints, IGraphExploration<VertexType, EdgeType> visitCallback) {
        if (notVisitedPoints.contains(vertex)) {
            notVisitedPoints.remove(vertex);
        } else {
            return;
        }
        visitCallback.onVisit(vertex, notVisitedPoints);

        for (Edge<VertexType, EdgeType> edge : vertex.getEdges()) {
            if (edge.getFromVertex() == vertex && notVisitedPoints.contains(edge.getToVertex())) {
                doBFS(edge.getFromVertex(), notVisitedPoints, visitCallback);
            } else if (!isDirected() && (edge.getToVertex() == vertex && notVisitedPoints.contains(edge.getFromVertex()))) {
                doBFS(edge.getToVertex(), notVisitedPoints, visitCallback);
            }
        }
    }
}
