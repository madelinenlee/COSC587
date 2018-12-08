package com.yektaie.graph.clustering;

import com.yektaie.graph.core.*;
import com.yektaie.graph.graphs.BaseGraph;
import com.yektaie.graph.graphs.UndirectedGraph;

import java.util.ArrayList;
import java.util.Collection;

/**
 * Implement dynamic clustering for graphs.
 *
 * For more information on the algorithm, please refer to https://ieeexplore.ieee.org/document/6785700
 * @param <VertexType> Generic type for vertex value type
 * @param <EdgeType> Generic type for edge value type
 */
public class DynamicClustering<VertexType, EdgeType> {
    /**
     * Splitting Threshold: L.  Please refer to https://ieeexplore.ieee.org/document/6785700
     */
    public double splittingThreshold = 0.5;

    /**
     * Reclustering Threshold: H  Please refer to https://ieeexplore.ieee.org/document/6785700
     */
    public double reclusteringThreshold = 0.5;

    /**
     * Disbanding Threshold: M  Please refer to https://ieeexplore.ieee.org/document/6785700
     */
    public double disbanningThreshold = 1.5;

    /**
     * Clusterer is abstracted to support other static graph clustering algorithm in the future
     */
    public IGraphClusterer<VertexType, EdgeType> clusterer = new ModularityClustering<>();

    /**
     * Given a dynamic graph, this method returns the cluster over time.
     * @param graphs Input dynamic series.
     * @return List of cluster over time.
     */
    public ArrayList<ArrayList<ArrayList<Vertex<VertexType, EdgeType>>>> getDynamicClusters(ArrayList<Graph<VertexType, EdgeType>> graphs) {
        ArrayList<ArrayList<ArrayList<Vertex<VertexType, EdgeType>>>> result = new ArrayList<>();

        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> t_prev_cluster = clusterer.getCommunities(graphs.get(0));
        double[] clusterDensities = getClusteringDensities(t_prev_cluster, graphs.get(0));
        result.add(t_prev_cluster);

        // Algorithm explained in paper: https://ieeexplore.ieee.org/document/6785700
        for (int i = 1; i < graphs.size(); i++) {
            ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters = duplicate(t_prev_cluster);
            removeElements(clusters, graphs.get(i - 1), graphs.get(i));
            addElements(clusters, graphs.get(i - 1), graphs.get(i));

            double[] clusterDensitiesNew = getClusteringDensities(clusters, graphs.get(i));
            splitClusters(clusters, graphs.get(i), clusterDensities, clusterDensitiesNew);
            reCluster(clusters, graphs.get(i));
            disbanClusters(clusters, graphs.get(i));

            result.add(clusters);
            clusterDensities = getClusteringDensities(clusters, graphs.get(i));
            t_prev_cluster = clusters;
        }

        // Empty clusters are generated as part of this implementation. They should be removed before returning cluster
        // list.
        for (ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters : result) {
            removeEmptyClusters(clusters);
        }


        return result;
    }

    /**
     * Get density of each cluster.
     * @param clusters List of clusters to calculate density.
     * @param graph Graph which the clusters are derived from.
     * @return A double array containing the density of each cluster.
     */
    private double[] getClusteringDensities(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        double[] result = new double[clusters.size()];

        for (int i = 0; i < result.length; i++) {
            int clusterEdgesCount = getClusterEdgesCount(clusters.get(i), graph);
            int maxEdgesCount = graph.getMaximumEdgesCount(clusters.get(i).size());

            if (clusterEdgesCount == 0 || maxEdgesCount == 0) {
                result[i] = 0;
            } else {
                result[i] = clusterEdgesCount * 1.0 / maxEdgesCount;
            }
        }

        return result;
    }

    /**
     * Get number of edges inside the cluster
     * @param cluster Cluster to count inner edges.
     * @param graph The graph which the cluster was derived from
     * @return Number of edges inside the cluster
     */
    private int getClusterEdgesCount(ArrayList<Vertex<VertexType, EdgeType>> cluster, Graph<VertexType, EdgeType> graph) {
        int result = 0;
        ArrayList<VertexType> values = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> cVertex : cluster) {
            values.add(cVertex.getValue());
        }

        for (Vertex<VertexType, EdgeType> cVertex : cluster) {
            Vertex<VertexType, EdgeType> gVertex = graph.getVertex(cVertex.getValue());

            if (gVertex != null) {
                for (Edge<VertexType, EdgeType> edge : gVertex.getEdges()) {
                    if (values.contains(edge.getFromVertex().getValue()) && values.contains(edge.getToVertex().getValue())) {
                        result++;
                    }
                }
            }
        }

        return result;

    }

    /**
     * Disban weak clusters. For more information refer to https://ieeexplore.ieee.org/document/6785700
     * @param clusters List of cluster to analyze.
     * @param graph The graph which these cluster were derived from.
     */
    private void disbanClusters(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clustersToBeDisbanned = new ArrayList<>();

        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            if (connectivityScore(cluster, clusters, graph) > disbanningThreshold) {
                clustersToBeDisbanned.add(cluster);
            }
        }

        ArrayList<Vertex<VertexType, EdgeType>> vertices = new ArrayList<>();
        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clustersToBeDisbanned) {
            vertices.addAll(cluster);
            cluster.clear();
        }

        addNewVerticesToClusters(clusters, graph, vertices);
    }

    /**
     * Add new vertices to a cluster. This part deviate from the original algorithm presented in https://ieeexplore.ieee.org/document/6785700
     * @param clusters List of current clusters.
     * @param graph Graph which the clusters derived from.
     * @param vertices List of new vertices that doesn't belong to any cluster.
     */
    private void addNewVerticesToClusters(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph, ArrayList<Vertex<VertexType, EdgeType>> vertices) {
        for (Vertex<VertexType, EdgeType> vertex : vertices) {
            Collection<Vertex<VertexType, EdgeType>> c = findBestCluster(vertex, clusters, graph);
            if (c != null) {
                c.add(vertex);
            } else {
                ArrayList<Vertex<VertexType, EdgeType>> newCluster = new ArrayList<>();
                newCluster.add(vertex);
                clusters.add(newCluster);
            }
        }
    }

    /**
     * Calculate the connectivity score by considering the strength of inner edges and inter-cluster edges. For more
     * information refer to https://ieeexplore.ieee.org/document/6785700.
     *
     * @param cluster Cluster to find connectivity score.
     * @param clusters List of all clusters.
     * @param graph Graph which these clusters are derived from.
     * @return A score of how good the cluster is.
     */
    private double connectivityScore(ArrayList<Vertex<VertexType, EdgeType>> cluster, ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        double result = 0;
        int edgeInCluster = getEdgeInCluster(cluster, graph);

        if (edgeInCluster == 0) {
            return 0;
        }

        for (ArrayList<Vertex<VertexType, EdgeType>> c : clusters) {
            if (c != cluster) {
                result += (getEdgesBetween(cluster, c, graph).size() * 1.0 / edgeInCluster);
            }
        }

        return result;
    }

    /**
     * Get number of inner edges in a cluster.
     * @param cluster Cluster to calculate edge count.
     * @param graph Graph which cluster is derived from.
     * @return Number of edges in cluster.
     */
    private int getEdgeInCluster(ArrayList<Vertex<VertexType, EdgeType>> cluster, Graph<VertexType, EdgeType> graph) {
        int edgeInCluster = 0;

        ArrayList<VertexType> values = new ArrayList<>();
        for (Vertex<VertexType, EdgeType> v : cluster) {
            values.add(v.getValue());
        }

        for (Edge<VertexType, EdgeType> e : graph.getEdges()) {
            if (values.contains(e.getFromVertex().getValue()) && values.contains(e.getToVertex().getValue())) {
                edgeInCluster++;
            }
        }
        return edgeInCluster;
    }

    /**
     * Re cluster clusters that can be strengthen. Please refer to https://ieeexplore.ieee.org/document/6785700
     * @param clusters List of clusters.
     * @param graph Graph which cluster are derived from.
     */
    private void reCluster(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer> clustersGraph = createClusterGraphs(clusters, graph);
        ArrayList<Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer>> components = clustersGraph.getConnectedComponents();
        for (Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer> component : components) {
            ArrayList<Vertex<VertexType, EdgeType>> largestCluster = getLargestCluster(component);

            component.bfs(largestCluster, new IGraphExploration<ArrayList<Vertex<VertexType, EdgeType>>, Integer>() {
                @Override
                public void onVisit(Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> vertex, ArrayList<Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer>> notVisitedNeighbors) {
                    if (!notVisitedNeighbors.isEmpty()) {
                        Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> nextLargest = getLargestCluster(notVisitedNeighbors);
                        if (!nextLargest.getValue().isEmpty() && !vertex.getValue().isEmpty()) {
                            notVisitedNeighbors.remove(nextLargest);

                            reclusterClusters(clusters, vertex.getValue(), nextLargest.getValue(), graph);
                            vertex.getValue().clear();
                            nextLargest.getValue().clear();
                        }
                    }
                }
            });
        }

    }

    /**
     * Recluster two connected clusers.
     * @param clusters List of clusters.
     * @param cluster1 Cluster 1 to analyse.
     * @param cluster2 Cluster 2 to analyse.
     * @param graph Graph which clusters are derived from.
     */
    private void reclusterClusters(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, ArrayList<Vertex<VertexType, EdgeType>> cluster1, ArrayList<Vertex<VertexType, EdgeType>> cluster2, Graph<VertexType, EdgeType> graph) {
        Graph<VertexType, EdgeType> newGraph = ((BaseGraph<VertexType, EdgeType>) graph).newInstance();
        ArrayList<VertexType> vs = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> v : cluster1) {
            newGraph.addVertex(v.getValue());
            vs.add(v.getValue());
        }

        for (Vertex<VertexType, EdgeType> v : cluster2) {
            newGraph.addVertex(v.getValue());
            vs.add(v.getValue());
        }

        for (Edge<VertexType, EdgeType> e : graph.getEdges()) {
            if (vs.contains(e.getFromVertex().getValue()) && vs.contains(e.getToVertex().getValue())) {
                newGraph.addEdge(e.getFromVertex().getValue(), e.getToVertex().getValue(), e.getValue());
            }
        }

        clusters.addAll(clusterer.getCommunities(newGraph));
    }

    private ArrayList<Vertex<VertexType, EdgeType>> getLargestCluster(Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer> component) {
        ArrayList<Vertex<VertexType, EdgeType>> result = null;

        for (Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> cluster : component.getVertices()) {
            if (result == null) {
                result = cluster.getValue();
            } else {
                if (cluster.getValue().size() > result.size()) {
                    result = cluster.getValue();
                }
            }
        }

        return result;
    }

    private Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> getLargestCluster(ArrayList<Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer>> vertices) {
        Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> result = null;

        for (Vertex<ArrayList<Vertex<VertexType, EdgeType>>, Integer> cluster : vertices) {
            if (result == null) {
                result = cluster;
            } else {
                if (cluster.getValue().size() > result.getValue().size()) {
                    result = cluster;
                }
            }
        }

        return result;
    }

    private Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer> createClusterGraphs(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        Graph<ArrayList<Vertex<VertexType, EdgeType>>, Integer> clustersGraph = new UndirectedGraph<>();

        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            if (!cluster.isEmpty()) {
                clustersGraph.addVertex(cluster);
            }
        }

        for (ArrayList<Vertex<VertexType, EdgeType>> clusterA : clusters) {
            for (ArrayList<Vertex<VertexType, EdgeType>> clusterB : clusters) {
                if (clusterA != clusterB && !clusterA.isEmpty() && !clusterB.isEmpty()) {
                    ArrayList<Edge<VertexType, EdgeType>> edges = getEdgesBetween(clusterA, clusterB, graph);
                    if (!edges.isEmpty()) {
                        clustersGraph.addEdge(clusterA, clusterB, edges.size());
                    }
                }
            }
        }

        return clustersGraph;
    }

    private ArrayList<Edge<VertexType, EdgeType>> getEdgesBetween(ArrayList<Vertex<VertexType, EdgeType>> clusterA, ArrayList<Vertex<VertexType, EdgeType>> clusterB, Graph<VertexType, EdgeType> graph) {
        ArrayList<Edge<VertexType, EdgeType>> result = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> a : clusterA) {
            for (Vertex<VertexType, EdgeType> b : clusterB) {
                Edge<VertexType, EdgeType> edge = getEdgeBetween(a, b, graph);
                if (edge != null) {
                    result.add(edge);
                }
            }
        }

        return result;
    }

    private Edge<VertexType, EdgeType> getEdgeBetween(Vertex<VertexType, EdgeType> a, Vertex<VertexType, EdgeType> b, Graph<VertexType, EdgeType> graph) {
        Edge<VertexType, EdgeType> result = null;

        for (Edge<VertexType, EdgeType> edge : graph.getEdges()) {
            if ((edge.getFromVertex().getValue().equals(a.getValue()) && edge.getToVertex().getValue().equals(b.getValue())) ||
                    (edge.getFromVertex().getValue().equals(b.getValue()) && edge.getToVertex().getValue().equals(a.getValue()))) {
                result = edge;
                break;
            }
        }

        return result;
    }

    private void splitClusters(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph, double[] clusterDensities, double[] clusterDensitiesNew) {
        int i = 0;

        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> newClusters = new ArrayList<>();
        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            if (cluster.size() > 0 && getDeltaDensity(clusterDensities, clusterDensitiesNew, i) > splittingThreshold) {
                Graph<VertexType, EdgeType> subGraph = getGraphSubset(graph, cluster);
                if (subGraph.getEdges().size() == 0) {
                    for (Vertex<VertexType, EdgeType> v : subGraph.getVertices()) {
                        ArrayList<Vertex<VertexType, EdgeType>> c = new ArrayList<>();
                        c.add(v);

                        newClusters.add(c);
                    }
                } else {
                    newClusters.addAll(clusterer.getCommunities(subGraph));
                }
                cluster.clear();
            }
            i++;
        }

        clusters.addAll(newClusters);
    }

    private Graph<VertexType, EdgeType> getGraphSubset(Graph<VertexType, EdgeType> graph, ArrayList<Vertex<VertexType, EdgeType>> vertices) {
        ArrayList<VertexType> values = new ArrayList<>();
        ArrayList<Vertex<VertexType, EdgeType>> finalVertices = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> v : vertices) {
            values.add(v.getValue());
        }

        ArrayList<Edge<VertexType, EdgeType>> edges = new ArrayList<>();
        for (Edge<VertexType, EdgeType> edge : graph.getEdges()) {
            if (values.contains(edge.getFromVertex().getValue()) && values.contains(edge.getToVertex().getValue())) {
                edges.add(edge);
            }

            if (!finalVertices.contains(edge.getToVertex())) {
                finalVertices.add(edge.getToVertex());
            }

            if (!finalVertices.contains(edge.getFromVertex())) {
                finalVertices.add(edge.getFromVertex());
            }
        }

        return ((BaseGraph<VertexType, EdgeType>) graph).createSubGraphFrom(vertices, edges);
    }


    private double getDeltaDensity(double[] oldDensity, double[] newDensity, int i) {
        if (oldDensity.length <= i) {
            return 1.0;
        }

        if (newDensity[i] == 0) {
            return 1.0;
        }

        return oldDensity[i] / newDensity[i];
    }

    private void addElements(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graphOld, Graph<VertexType, EdgeType> graphNew) {
        ArrayList<Vertex<VertexType, EdgeType>> addedVertices = subtractVertices(graphNew.getVertices(), graphOld.getVertices());

        addNewVerticesToClusters((ArrayList<ArrayList<Vertex<VertexType, EdgeType>>>) clusters, (Graph<VertexType, EdgeType>) graphNew, (ArrayList<Vertex<VertexType, EdgeType>>) addedVertices);
    }

    private Collection<Vertex<VertexType, EdgeType>> findBestCluster(Vertex<VertexType, EdgeType> vertex, ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graph) {
        int maxConnections = 0;
        ArrayList<Vertex<VertexType, EdgeType>> bestCluster = null;

        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            int connections = getConnectionCount(cluster, vertex, graph);
            if (connections > maxConnections) {
                maxConnections = connections;
                bestCluster = cluster;
            }
        }

        return bestCluster;
    }

    private int getConnectionCount(ArrayList<Vertex<VertexType, EdgeType>> cluster, Vertex<VertexType, EdgeType> vertex, Graph<VertexType, EdgeType> graph) {
        int result = 0;

        for (Vertex<VertexType, EdgeType> cVertex : cluster) {
            Vertex<VertexType, EdgeType> gVertex = graph.getVertex(cVertex.getValue());

            if (gVertex != null) {
                for (Edge<VertexType, EdgeType> edge : gVertex.getEdges()) {
                    if (edge.getOtherVertex(gVertex).getValue().equals(vertex.getValue())) {
                        result++;
                    }
                }
            }
        }

        return result;
    }

    private void removeElements(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters, Graph<VertexType, EdgeType> graphOld, Graph<VertexType, EdgeType> graphNew) {
        ArrayList<Vertex<VertexType, EdgeType>> removedVertices = subtractVertices(graphOld.getVertices(), graphNew.getVertices());
        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            for (Vertex<VertexType, EdgeType> removed : removedVertices) {
                Vertex<VertexType, EdgeType> corresponding = getVertex(removed.getValue(), cluster);
                if (corresponding != null) {
                    cluster.remove(corresponding);
                }
            }
        }
    }

    private void removeEmptyClusters(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters) {
        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> emptyClusters = new ArrayList<>();
        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            if (cluster.size() == 0) {
                emptyClusters.add(cluster);
            }
        }

        clusters.removeAll(emptyClusters);
    }

    private ArrayList<Vertex<VertexType, EdgeType>> subtractVertices(ArrayList<Vertex<VertexType, EdgeType>> vertices1, ArrayList<Vertex<VertexType, EdgeType>> vertices2) {
        ArrayList<Vertex<VertexType, EdgeType>> result = new ArrayList<>();

        for (Vertex<VertexType, EdgeType> v : vertices1) {
            Vertex<VertexType, EdgeType> corresponding = getVertex(v.getValue(), vertices2);
            if (corresponding == null) {
                result.add(v);
            }
        }

        return result;
    }

    private Vertex<VertexType, EdgeType> getVertex(VertexType value, ArrayList<Vertex<VertexType, EdgeType>> vertices) {
        Vertex<VertexType, EdgeType> result = null;

        for (Vertex<VertexType, EdgeType> v : vertices) {
            if (v.getValue().equals(value)) {
                result = v;
                break;
            }
        }

        return result;
    }

    private ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> duplicate(ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> clusters) {
        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> result = new ArrayList<>();

        for (ArrayList<Vertex<VertexType, EdgeType>> cluster : clusters) {
            result.add(new ArrayList<>(cluster));
        }

        return result;
    }
}
