package com.yektaie.graph.core;

import java.util.ArrayList;

public interface IGraphExploration<VertexType, EdgeType> {
    void onVisit(Vertex<VertexType, EdgeType> vertex, ArrayList<Vertex<VertexType, EdgeType>> notVisitedNeighbors);
}
