package com.yektaie.graph.core;

import java.util.ArrayList;

public interface IGraphClusterer<VertexType, EdgeType> {
    ArrayList<ArrayList<Vertex<VertexType, EdgeType>>> getCommunities(Graph<VertexType, EdgeType> graph);
}
