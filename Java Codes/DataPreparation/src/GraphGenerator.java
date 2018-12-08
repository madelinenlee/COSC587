import java.util.ArrayList;

public class GraphGenerator {
    public static void main(String[] args) {
        ArrayList<String[]> data = loadData("/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/cleaned_data/merged_data.csv");
        filterPositions(data);
        data = removeUnusedData(data);
        double meanRecYards = getAverageRecYards(data);
        double stdRecYards = getStdRecYards(data);

        double threshold = meanRecYards + 0.5 * stdRecYards;
        ArrayList<String> years = getYears(data);

        for (String year : years) {
            String graph = toGraph(year, data, threshold);
            Program.writeAllText("/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/graphs/" + year + ".csv", graph);
        }
    }

    private static String toGraph(String year, ArrayList<String[]> data, double threshold) {
        ArrayList<String> nodes = new ArrayList<>();
        StringBuilder result = new StringBuilder();

        result.append("From,To,Weight");

        for (String[] row : data) {
            if (row[2].equals(year)) {
                String player = row[0];
                double recYards = Double.valueOf(row[1]);
                String weather = row[3];

                if (!nodes.contains(player)) {
                    result.append("\n").append(player);
                    nodes.add(player);
                }

                if (recYards >= threshold) {
                    result.append("\n").append(String.format("%s,%s,%d", player, weather, (int)recYards));
                }
            }
        }

        return result.toString();
    }

    private static ArrayList<String> getYears(ArrayList<String[]> data) {
        ArrayList<String> result = new ArrayList<>();

        for (String[] row : data) {
            if (!result.contains(row[2])) {
                result.add(row[2]);
            }
        }

        return result;
    }

    private static double getAverageRecYards(ArrayList<String[]> data) {
        double result = 0;

        for (String[] row : data) {
            result += Double.valueOf(row[1]);
        }

        return result / data.size();
    }

    private static double getStdRecYards(ArrayList<String[]> data) {
        double sum = 0;
        double sumSq = 0;

        for (String[] row : data) {
            double v = Double.valueOf(row[1]);
            sum += v;
            sumSq += (v*v);
        }

        double mean = sum / data.size();
        return Math.sqrt(sumSq / data.size() - (mean * mean));
    }

    private static ArrayList<String[]> removeUnusedData(ArrayList<String[]> data) {
        int[] toKeep = {28,38,52,58};
        ArrayList<String[]> result = new ArrayList<>();

        for (String[] row : data) {
            String[] values = keepOnly(row, toKeep);
            values[3] = "___" + values[3];
            result.add(values);
        }

        return result;
    }

    private static String[] keepOnly(String[] row, int[] toKeep) {
        String[] result = new String[toKeep.length];

        for (int i = 0; i < result.length; i++) {
            result[i] = row[toKeep[i]];
        }

        return result;
    }

    private static void filterPositions(ArrayList<String[]> data) {
        ArrayList<String[]> toBeRemoved = new ArrayList<>();

        for (String[] row : data) {
            if (!row[29].equals("WR") || row[11].equals("0")) {
                toBeRemoved.add(row);
            }
        }

        data.removeAll(toBeRemoved);
    }

    private static ArrayList<String[]> loadData(String path) {
        ArrayList<String> lines = Program.readAllLines(path);
        ArrayList<String[]> result = new ArrayList<>();

        for (String line : lines) {
            result.add(line.split(","));
        }

        return result;
    }
}
