package com.yektaie.graph.clustering;

import com.yektaie.graph.core.Edge;
import com.yektaie.graph.core.Graph;
import com.yektaie.graph.core.IGraphClusterer;
import com.yektaie.graph.core.Vertex;

import java.util.ArrayList;

public class ModularityClustering<VertexType, EdgeType> implements IGraphClusterer<VertexType, EdgeType> {
    @Override
    public ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> getCommunities(Graph<VertexType, EdgeType> graph) {
        ArrayList<ModularityClusteringStep<VertexType, EdgeType>> steps = new ArrayList<>();

        while (graph.getEdges().size() > 0) {
            graph = graph.clone();

            ModularityClusteringStep<VertexType, EdgeType> step = new ModularityClusteringStep<>();
            step.graph = graph;
            step.connectedComponents = graph.getConnectedComponents();
            step.modularity = getModularity(step.graph, toVertexList(step.connectedComponents));
            steps.add(step);

            ArrayList<Edge<VertexType, EdgeType>> maxEdges = getEdgesWithMaximumBetweenness(graph);

            graph.removeEdges(maxEdges);
        }


        double maxModularity = -1;
        int i = 0;
        int index = 0;

        for (ModularityClusteringStep<VertexType, EdgeType> step : steps) {
            if (maxModularity < step.modularity) {
                index = i;
                maxModularity = step.modularity;
            }

            i++;
        }

        return toVertexList(steps.get(index).connectedComponents);
    }

    private ArrayList<Edge<VertexType, EdgeType>> getEdgesWithMaximumBetweenness(Graph<VertexType, EdgeType> graph) {
        ArrayList<Edge<VertexType, EdgeType>> maxEdges = new ArrayList<>();
        double maxBetweenness = -1;

//        System.out.print("    Calculating edge betweenness");
        int i = 0;
        for (Edge<VertexType, EdgeType> edge : graph.getEdges()) {
            i++;

//            System.out.print("\r    Calculating edge betweenness: " + i + " of " + graph.getEdges().size());
            double betweenness = edge.getBetweenness();
            if (betweenness > maxBetweenness) {
                maxEdges.clear();
                maxBetweenness = betweenness;

                maxEdges.add(edge);
            } else if (betweenness == maxBetweenness) {
                maxEdges.add(edge);
            }
        }

//        System.out.println();
        return maxEdges;
    }

    private ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> toVertexList(ArrayList<Graph<VertexType, EdgeType>> connectedComponents) {
        ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> result = new ArrayList<>();

        for (Graph<VertexType, EdgeType> g : connectedComponents) {
            ArrayList<Vertex<VertexType, EdgeType>> community = new ArrayList<>(g.getVertices());

            result.add(community);
        }

        return result;
    }

    public static double[][] createModularityMatrix(int[][] a, int m2, int[] communities) {
        double[][] modularityMatrix = createProbabilityMatrix(a, m2);
        for (int i = 0; i < modularityMatrix.length; i++) {
            for (int j = 0; j < modularityMatrix.length; j++) {
                modularityMatrix[i][j] = (a[i][j] - modularityMatrix[i][j]) * delta(communities[i], communities[j]) / m2;
            }
        }

        return modularityMatrix;
    }

    private static double delta(int i, int j) {
        if (i == j) {
            return 1.0;
        }

        return 0;
    }

    public double getModularity(Graph<VertexType, EdgeType> parentGraph, ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> communities) {
        int[][] a = parentGraph.getConnectionMatrix();
        int m2 = getTwoM(a);

        if (m2 == 0) {
            return -1;
        }

        int[] c = new int[parentGraph.getVertices().size()];
        int comIndex = 0;
        for (ArrayList<Vertex<VertexType, EdgeType>> community : communities) {
            for (Vertex<VertexType, EdgeType> v : community) {
                c[parentGraph.getVertices().indexOf(parentGraph.getVertex(v.getValue()))] = comIndex;
            }

            comIndex++;
        }

        double[][] modularityMatrix = createModularityMatrix(a, m2, c);

        double result = 0;

        for (ArrayList<Vertex<VertexType, EdgeType>> community : communities) {
            for (Vertex<VertexType, EdgeType> v : community) {
                for (Vertex<VertexType, EdgeType> u : community) {
                    result += modularityMatrix[parentGraph.getVertices().indexOf(parentGraph.getVertex(v.getValue()))][parentGraph.getVertices().indexOf(parentGraph.getVertex(u.getValue()))];
                }
            }
        }

        return result / m2;
    }

    private static int getTwoM(int[][] a) {
        int result = 0;

        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[i].length; j++) {
                result += a[i][j];
            }
        }

        return result;
    }

    private static double[][] createProbabilityMatrix(int[][] a, int m2) {
        double[][] result = new double[a.length][];
        for (int i = 0; i < result.length; i++) {
            result[i] = new double[a.length];
        }

        for (int i = 0; i < result.length; i++) {
            for (int j = 0; j < result[i].length; j++) {
                int deg_i = degree(a, i);
                int deg_j = degree(a, j);
                result[i][j] = (deg_i * deg_j * 1.0) / m2;
            }
        }

        return result;
    }

    private static int degree(int[][] a, int i) {
        int result = 0;

        for (int j = 0; j < a.length; j++) {
            result += a[i][j];
        }

        return result;
    }
}

class ModularityClusteringStep<VertexType, EdgeType> {
    public Graph<VertexType, EdgeType> graph = null;
    public ArrayList<Graph<VertexType, EdgeType>> connectedComponents = null;
    public double modularity = 0;

    @Override
    public String toString() {
        return String.format("[%d] modularity: %.3f", connectedComponents.size(), modularity);
    }
}