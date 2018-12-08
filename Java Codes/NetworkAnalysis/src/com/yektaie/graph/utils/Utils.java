package com.yektaie.graph.utils;

import com.yektaie.graph.core.Path;

import java.util.ArrayList;

public class Utils {
    public static void throwExceptionIfNonNull(Object value, String message) {
        if (value != null) {
            throw new RuntimeException(message);
        }
    }

    public static void throwExceptionIfNull(Object value, String message) {
        if (value == null) {
            throw new RuntimeException(message);
        }
    }

    public static <EdgeType, VertexType> ArrayList<Path<VertexType, EdgeType>> getLongestPath(ArrayList<Path<VertexType, EdgeType>> paths) {
        ArrayList<Path<VertexType, EdgeType>> result = new ArrayList<>();

        if (paths == null) {
            return result;
        }

        int longestLength = -1;

        for (Path<VertexType, EdgeType> path : paths) {
            if (path.size() > longestLength) {
                longestLength = path.size();
                result.clear();
                result.add(path);
            } else if (path.size() == longestLength) {
                result.add(path);
            }
        }

        return result;
    }

    public static <EdgeType, VertexType> ArrayList<Path<VertexType, EdgeType>> getShortestPath(ArrayList<Path<VertexType, EdgeType>> paths) {
        ArrayList<Path<VertexType, EdgeType>> result = new ArrayList<>();

        if (paths == null) {
            return result;
        }

        int shortestLength = Integer.MAX_VALUE;

        for (Path<VertexType, EdgeType> path : paths) {
            if (path.size() < shortestLength) {
                shortestLength = path.size();
                result.clear();
                result.add(path);
            } else if (path.size() == shortestLength) {
                result.add(path);
            }
        }

        return result;
    }
}
