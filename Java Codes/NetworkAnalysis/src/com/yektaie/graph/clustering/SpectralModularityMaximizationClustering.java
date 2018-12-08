//https://github.com/zhiyzuo/python-modularity-maximization/blob/master/modularity_maximization/community_newman.py

//package com.yektaie.graph.clustering;
//
//import com.yektaie.graph.core.Edge;
//import com.yektaie.graph.core.Graph;
//import com.yektaie.graph.core.IGraphClusterer;
//import com.yektaie.graph.core.Vertex;
//import com.yektaie.graph.graphs.BaseGraph;
//
//import java.util.ArrayList;
//import java.util.HashMap;
//
//public class SpectralModularityMaximizationClustering<VertexType, EdgeType> implements IGraphClusterer<VertexType, EdgeType> {
//    @Override
//    public ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> getCommunities(Graph<VertexType, EdgeType> network) {
//        // only support unweighted network
//        double[][] B = ModularityClustering.createModularityMatrix(network);
//        // set flags for divisibility of communities
//        // initial community is divisible
//
//        ArrayList<Integer> divisible_community = new ArrayList<>();
//        divisible_community.add(0);
//
//        // add attributes: all node as one group
//        HashMap<VertexType, Integer> community_dict = new HashMap<>();
//
//        // overall modularity matrix
//        int comm_counter = 0;
//
//        while (divisible_community.size() > 0) {
//            // get the first divisible comm index out
//            int comm_index = divisible_community.get(0);
//            divisible_community.remove(0);
//            GraphDivisionResult<VertexType, EdgeType> division = divide(network, community_dict, comm_index, B, true);
//            ArrayList<Vertex<VertexType, EdgeType>> g1_nodes = division.g1_nodes;
//
//            if (g1_nodes == null) {
//                // indivisible, go to next
//                continue;
//            }
//
//            // Else divisible, obtain the other group g2
//            // Get the subgraphs (sub-communities)
//
//            Graph<VertexType, EdgeType> g1 = getGraphSubset(network, g1_nodes);
//            Graph<VertexType, EdgeType> g2 = getGraphComplement(network, g1_nodes);
//
//            comm_counter += 1;
//            divisible_community.add(comm_counter);
//            // update community
//            for (Vertex<VertexType, EdgeType> vertex : g1.getVertices()) {
//                community_dict.put(vertex.getValue(), comm_counter);
//            }
//
//            comm_counter += 1;
//            divisible_community.add(comm_counter);
//            // update community
//            for (Vertex<VertexType, EdgeType> vertex : g2.getVertices()) {
//                community_dict.put(vertex.getValue(), comm_counter);
//            }
//        }
////
////        return {node_name[u]: community_dict[u] for u in network}
//        return null;
//    }
//
//    private Graph<VertexType, EdgeType> getGraphComplement(Graph<VertexType, EdgeType> graph, ArrayList<Vertex<VertexType, EdgeType>> vertices) {
//        ArrayList<Vertex<VertexType, EdgeType>> temp = new ArrayList<>();
//
//        for (Vertex<VertexType, EdgeType> v : graph.getVertices()) {
//            if (!vertices.contains(v)) {
//                temp.add(v);
//            }
//        }
//
//        return getGraphSubset(graph, temp);
//    }
//
//    private Graph<VertexType, EdgeType> getGraphSubset(Graph<VertexType, EdgeType> graph, ArrayList<Vertex<VertexType, EdgeType>> vertices) {
//        ArrayList<Edge<VertexType, EdgeType>> edges = new ArrayList<>();
//        for (Edge<VertexType, EdgeType> edge : graph.getEdges()) {
//            if (vertices.contains(edge.getFromVertex()) && vertices.contains(edge.getToVertex())) {
//                edges.add(edge);
//            }
//        }
//
//        return ((BaseGraph<VertexType, EdgeType>)graph).createSubGraphFrom(vertices, edges);
//    }
//
//    private GraphDivisionResult<VertexType, EdgeType> divide(Graph<VertexType, EdgeType> network, HashMap<VertexType, Integer> community_dict, int comm_index, double[][] B, boolean refine) {
//
//    }
//}
//
//class VertexCommunityPair<VertexType, EdgeType> {
//    public Vertex<VertexType, EdgeType> vertex = null;
//    public int community = 0;
//}
//
//class GraphDivisionResult<VertexType, EdgeType> {
//    public ArrayList<Vertex<VertexType, EdgeType>> g1_nodes = null;
//    public ArrayList<Vertex<VertexType, EdgeType>> comm_nodes = null;
//}
