import java.util.ArrayList;
import java.util.HashMap;

public class ModelSelection {
    public static void main(String[] args) {
        ArrayList<String[]> data = loadData("/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/predictions/summary-final.csv");
        ArrayList<String[]> result = new ArrayList<>();
        ArrayList<String> done = new ArrayList<>();

        result.add(data.get(0));
        HashMap<String, Integer> counts = new HashMap<>();
        counts.put("svr", 0);
        counts.put("dt", 0);
        counts.put("linear_regression", 0);
        counts.put("keras", 0);
        counts.put("knn", 0);

        HashMap<String, Double> errors = new HashMap<>();
        HashMap<String, Integer> choosedCount = new HashMap<>();
        HashMap<String, Double> std = new HashMap<>();

        errors.put("keras", 0.0);
        errors.put("svr", 0.0);
        errors.put("knn", 0.0);
        errors.put("dt", 0.0);
        errors.put("linear_regression", 0.0);

        choosedCount.put("keras", 0);
        choosedCount.put("svr", 0);
        choosedCount.put("knn", 0);
        choosedCount.put("dt", 0);
        choosedCount.put("linear_regression", 0);

        std.put("keras", 0.0);
        std.put("svr", 0.0);
        std.put("knn", 0.0);
        std.put("dt", 0.0);
        std.put("linear_regression", 0.0);

        int i = 1;
        while (i < data.size()) {
            errors.put(data.get(i)[2], errors.get(data.get(i)[2]) + Double.valueOf(data.get(i)[5]));
            choosedCount.put(data.get(i)[2], choosedCount.get(data.get(i)[2]) + 1);

            std.put(data.get(i)[2], std.get(data.get(i)[2]) + Double.valueOf(data.get(i)[6]));
            i++;
        }

        for (String key : errors.keySet()) {
            System.out.println(String.format("%s,%.5f,%.5f", key, errors.get(key) / choosedCount.get(key), std.get(key) / choosedCount.get(key)));
        }

        i = 1;
        while (i < data.size()) {
            String variable = data.get(i)[0];
            String position = data.get(i)[1];

            String index = variable + "_" + position;
            if (!done.contains(index)) {
                done.add(index);

                String[] min = getMinValue(data, variable, position);
                result.add(min);

                counts.put(min[2], counts.get(min[2]) + 1);

            }
            i++;
        }

        StringBuilder selection = new StringBuilder();
        for (String[] row : result) {
            String del = "";
            for (String cell : row) {
                selection.append(del);
                selection.append(cell);
                del = ",";
            }

            selection.append("\n");
        }

        System.out.println(selection.toString());
    }

    private static String[] getMinValue(ArrayList<String[]> data, String variable, String position) {
        String[] result = null;
        double error = 100;

        for (String[] row : data) {
            String v = row[0];
            String p = row[1];

            if (v.equals(variable) && position.equals(p)) {
                double e = Double.valueOf(row[5]);
                if (e < error) {
                    result = row;
                    error = e;
                }
            }

        }

        return result;
    }

    private static ArrayList<String[]> loadData(String path) {
        ArrayList<String> lines = Program.readAllLines(path);
        ArrayList<String[]> result = new ArrayList<>();

        for (String line : lines) {
            result.add(line.split(","));
        }

        return result;
    }

    private static ArrayList<String[]> toList(String[][] data) {
        ArrayList<String[]> result = new ArrayList<>();

        for (int i = 0; i < data.length; i++) {
            result.add(data[i]);
        }

        return result;
    }
}
