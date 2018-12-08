package com.yektaie.graph.core;

import java.util.ArrayList;
import java.util.HashMap;

public class Path<VertexType, EdgeType> extends ArrayList<Edge<VertexType, EdgeType>> {
    public Path<VertexType, EdgeType> duplicate() {
        Path<VertexType, EdgeType> result = new Path<>();

        result.addAll(this);

        return result;
    }

    public boolean containsVertex(Vertex<VertexType, EdgeType> vertex) {
        for (Edge<VertexType, EdgeType> edge : this) {
            if (edge.getFromVertex() == vertex || edge.getToVertex() == vertex) {
                return true;
            }
        }

        return false;
    }

    public boolean hasDuplicateVertex() {
        if (size() == 0) {
            return false;
        }

        HashMap<Vertex<VertexType, EdgeType>, Integer> counts = new HashMap<>();

        for (Edge<VertexType, EdgeType> edge : this) {
            if (counts.containsKey(edge.getFromVertex())) {
                int count = counts.get(edge.getFromVertex()) + 1;
                counts.put(edge.getFromVertex(), count);
            } else {
                counts.put(edge.getFromVertex(), 1);
            }

            if (counts.containsKey(edge.getToVertex())) {
                int count = counts.get(edge.getToVertex()) + 1;
                counts.put(edge.getToVertex(), count);
            } else {
                counts.put(edge.getToVertex(), 1);
            }
        }

        int count = counts.get(get(0).getFromVertex()) + 1;
        counts.put(get(0).getFromVertex(), count);

        count = counts.get(get(size() - 1).getToVertex()) + 1;
        counts.put(get(size() - 1).getToVertex(), count);

        for (Vertex<VertexType, EdgeType> v : counts.keySet()) {
            count = counts.get(v);
            if (count != 2) {
                return true;
            }
        }

        return false;
    }
}
