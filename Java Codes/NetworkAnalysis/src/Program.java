import com.yektaie.graph.clustering.DynamicClustering;
import com.yektaie.graph.core.Graph;
import com.yektaie.graph.core.Vertex;
import com.yektaie.graph.graphs.MultiGraph;
import com.yektaie.graph.graphs.UndirectedGraph;
import com.yektaie.graph.io.Factory;
import com.yektaie.graph.io.GraphLoader;
import com.yektaie.graph.io.loaders.SimpleCSVFileLoader;

import java.util.ArrayList;
import java.util.HashMap;

public class Program {
    public static void main(String[] args) {
        Factory<String> strFactory = new Factory<String>() {
            @Override
            public String newInstance(String str) {
                return str;
            }
        };

        Factory<Double> doubleFacotry = new Factory<Double>() {
            @Override
            public Double newInstance(String str) {
                return Double.valueOf(str);
            }
        };

        GraphLoader<String, Double> loader = new SimpleCSVFileLoader<>("examples/karate.csv", true, strFactory, doubleFacotry);
        Graph<String, Double> graph = new UndirectedGraph<>(loader);
        System.out.println(graph);

//        ArrayList<Graph<String, Double>> series = loadTimedGraph();
//        System.out.println(series);

//        DynamicClustering<String, Double> clusterer = new DynamicClustering<>();
//        ArrayList<ArrayList<ArrayList<Vertex<String, Double>>>> clusters = clusterer.getDynamicClusters(series);
//
//        double[][] relationMatrix = createRelationMatrix(clusters, series);
//        System.out.println(clusters);
    }

    private static double[][] createRelationMatrix(ArrayList<ArrayList<ArrayList<Vertex<String, Double>>>> clusters, ArrayList<Graph<String, Double>> series) {
        ArrayList<String> players = getPlayers(series);
        ArrayList<String> weathers = getWeather(series);

        double[][] result = new double[players.size()][];
        for (int i = 0; i < result.length; i++) {
            result[i] = new double[weathers.size()];
        }

        double sum = 0;
        double max = 0;
        for (ArrayList<ArrayList<Vertex<String, Double>>> clusterSet : clusters) {
            for (ArrayList<Vertex<String, Double>> cluster : clusterSet) {
                ArrayList<String> clusterPlayers = getClusterPlayers(cluster);
                ArrayList<String> clusterWeather = getClusterWeather(cluster);

                for (String player : clusterPlayers) {
                    int p = players.indexOf(player);

                    for (String weather : clusterWeather) {
                        int w = weathers.indexOf(weather);

                        result[p][w] += 1;
                        sum += 1;
                        max = Math.max(max, result[p][w]);
                    }
                }
            }
        }

        for (int i = 0; i < players.size(); i++) {
            int yearsIn = getYearsCountFor(clusters, players.get(i));

            for (int j = 0; j < result[i].length; j++) {
                result[i][j] = result[i][j] / yearsIn;
            }
        }

        HashMap<Double, Integer> histogram = new HashMap<>();
        for (int i = 0; i < result.length; i++) {
            for (int j = 0; j < result[i].length; j++) {
                double value = result[i][j];
                int count = histogram.getOrDefault(value, 0);
                count++;

                histogram.put(value, count);
            }
        }

        double[] columnVariance = new double[weathers.size()];
        double[] columnMean = new double[weathers.size()];
        double[] columnMax = new double[weathers.size()];
        for (int i = 0; i < columnVariance.length; i++) {
            columnVariance[i] = calculateVariance(result, i);
            columnMean[i] = calculateMean(result, i);
            columnMax[i] = getMax(result, i);
        }

        double[][] temp = transpose(result);

        return result;
    }

    private static double[][] transpose(double[][] matrix) {
        double[][] result = new double[matrix[0].length][];
        for (int i = 0; i < result.length; i++) {
            result[i] = new double[matrix.length];
        }

        for (int i = 0; i < result.length; i++) {
            for (int j = 0; j < result[i].length; j++) {
                result[i][j] = matrix[j][i];
            }
        }
        return result;
    }

    private static double getMax(double[][] result, int i) {
        double max = 0;

        for (int j = 0; j < result.length; j++) {
            double value = result[j][i];
            max = Math.max(value, max);
        }

        return max;
    }

    private static double calculateVariance(double[][] result, int i) {
        double sum = 0;
        double sumSq = 0;

        for (int j = 0; j < result.length; j++) {
            double value = result[j][i];
            sum += value;
            sumSq += value * value;
        }


        double mean = sum / result.length;
        return Math.sqrt(sumSq / result.length - mean * mean);
    }

    private static double calculateMean(double[][] result, int i) {
        double sum = 0;

        for (int j = 0; j < result.length; j++) {
            double value = result[j][i];
            sum += value;
        }


        return sum / result.length;
    }

    private static int getYearsCountFor(ArrayList<ArrayList<ArrayList<Vertex<String, Double>>>> clusters, String player) {
        int result = 0;

        for (ArrayList<ArrayList<Vertex<String, Double>>> clusterSet : clusters) {
            if (hasPlayer(clusterSet, player)) {
                result++;
            }
        }

        return result;
    }

    private static boolean hasPlayer(ArrayList<ArrayList<Vertex<String, Double>>> clusterSet, String player) {
        for (ArrayList<Vertex<String, Double>> cluster : clusterSet) {
            for (Vertex<String, Double> v : cluster) {
                if (v.getValue().equals(player)) {
                    return true;
                }
            }
        }

        return false;
    }

    private static ArrayList<String> getClusterPlayers(ArrayList<Vertex<String, Double>> cluster) {
        ArrayList<String> result = new ArrayList<>();

        for (Vertex<String, Double> v : cluster) {
            String value = v.getValue();

            if (!value.startsWith("___")) {
                if (!result.contains(value)) {
                    result.add(value);
                }
            }
        }

        return result;
    }

    private static ArrayList<String> getClusterWeather(ArrayList<Vertex<String, Double>> cluster) {
        ArrayList<String> result = new ArrayList<>();

        for (Vertex<String, Double> v : cluster) {
            String value = v.getValue();

            if (value.startsWith("___")) {
                value = value.substring(3);

                if (!result.contains(value)) {
                    result.add(value);
                }
            }
        }

        return result;
    }

    private static ArrayList<String> getWeather(ArrayList<Graph<String, Double>> series) {
        ArrayList<String> result = new ArrayList<>();

        for (Graph<String, Double> graph : series) {
            for (Vertex<String, Double> vertex : graph.getVertices()) {
                String value = vertex.getValue();

                if (value.startsWith("___")) {
                    value = value.substring(3);

                    if (!result.contains(value)) {
                        result.add(value);
                    }
                }
            }
        }

        return result;
    }

    private static ArrayList<String> getPlayers(ArrayList<Graph<String, Double>> series) {
        ArrayList<String> result = new ArrayList<>();

        for (Graph<String, Double> graph : series) {
            for (Vertex<String, Double> vertex : graph.getVertices()) {
                String value = vertex.getValue();

                if (!value.startsWith("___")) {
                    if (!result.contains(value)) {
                        result.add(value);
                    }
                }
            }
        }

        return result;
    }

    private static ArrayList<Graph<String, Double>> loadTimedGraph() {
        ArrayList<Graph<String, Double>> result = new ArrayList<>();

        Factory<String> strFactory = new Factory<String>() {
            @Override
            public String newInstance(String str) {
                return str;
            }
        };

        Factory<Double> doubleFacotry = new Factory<Double>() {
            @Override
            public Double newInstance(String str) {
                return Double.valueOf(str);
            }
        };


        for (int i = 2013; i <= 2017; i++) {
            GraphLoader<String, Double> loader = new SimpleCSVFileLoader<>(String.format("/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/graphs/%d.csv", i), true, strFactory, doubleFacotry);
            Graph<String, Double> graph = new MultiGraph<>(loader);
            result.add(graph);
        }

        return result;
    }
}
