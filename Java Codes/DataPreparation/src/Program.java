import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class Program {
    private static List<String> headerList;

    public static void main(String[] args) {
        String[] positions = {"K", "QB", "RB", "TE", "WR"};

        for (String position : positions) {
//            String[][] originalData = loadData("/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/cleaned_data/merged_data.csv");
            String[][] originalData = loadData("/Users/yektaie/Downloads/minimerged.csv");
            originalData = removeUnstartedGames(originalData);
            originalData = filterPositionAndKeepOnly(originalData, position);
            String[][] data = transpose(originalData);
            ArrayList<String[]> newData = prepareDataEncodings(data);
            String[] outputs = {"all_td", "def_int_td", "fga", "fgm", "kick_ret", "kick_ret_td", "kick_ret_yds", "pass_att", "pass_cmp", "pass_int", "pass_rating", "pass_sacked", "pass_sacked_yds", "pass_td", "pass_yds", "punt_ret", "punt_ret_td", "punt_ret_yds", "punt_ret_yds_per_ret", "punt_yds_per_punt", "rec", "rec_td", "rec_yds", "rush_att", "rush_td", "rush_yds", "scoring", "targets", "two_pt_md", "xpa", "xpm"};

            for (String output : outputs) {
                System.out.println(output);
                String[] variable = data[getHeaderIndex(output, data)];
                newData.add(variable);
                saveCSV(transpose(toArray(newData)), "/Volumes/Files/Georgetown/Introduction to Data Analytics/project/COSC587/test_data/" + output + "-" + position + ".csv");
                newData.remove(newData.size() - 1);
            }
        }
    }

    private static String[][] removeUnstartedGames(String[][] originalData) {
        ArrayList<String[]> temp = new ArrayList<>();
        temp.add(originalData[0]);

        for (String[] row : originalData) {
            if (row[row.length - 1].equals("1")) {
                temp.add(row);
            }
        }

        originalData = new String[temp.size()][];
        for (int i = 0; i < temp.size(); i++) {
            originalData[i] = temp.get(i);
        }
        return originalData;
    }

    private static String[][] filterPositionAndKeepOnly(String[][] originalData, String position) {
        ArrayList<String[]> temp = new ArrayList<>();
        temp.add(originalData[0]);

        for (String[] row : originalData) {
            if (row[2].equals(position)) {
                temp.add(row);
            }
        }

        originalData = new String[temp.size()][];
        for (int i = 0; i < temp.size(); i++) {
            originalData[i] = temp.get(i);
        }
        return originalData;
    }

    private static String[][] toArray(ArrayList<String[]> newData) {
        String[][] result = new String[newData.size()][];

        for (int i = 0; i < newData.size(); i++) {
            result[i] = newData.get(i);
        }

        return result;
    }

    private static int getHeaderIndex(String output, String[][] data) {
        int index = -1;

        for (int i = 0; i < data.length; i++) {
            if (data[i][0].equals(output)) {
                index = i;
                break;
            }
        }

        return index;
    }

    private static ArrayList<String[]> prepareDataEncodings(String[][] data) {
        ArrayList<String[]> newData = new ArrayList<>();

        newData.add(data[0]); // age
        newData.add(data[1]); // game_num
        addPositionData(newData, data[2]);
        newData.add(data[3]); // away
        addDomeData(newData, data[4]);
        addWeatherSummaryData(newData, data[5]);
        addWindData(newData, data[6]);
        addHumidityData(newData, data[7]);
        newData.add(data[8]); // kick_off_visibility
        newData.add(data[9]); // kick_off_barometer
        newData.add(data[10]); // kick_off_dew_point
        addCloudCoverData(newData, data[11]);
        newData.add(data[getHeaderIndex("gs", data)]);

        return newData;
    }

    private static void addHumidityData(ArrayList<String[]> newData, String[] data) {
        for (int i = 1; i < data.length; i++) {
            if (data[i].equals("") || data[i].contains(" ")) {
                data[i] = "0";
            }
        }

        newData.add(data);
    }

    private static void addCloudCoverData(ArrayList<String[]> newData, String[] data) {
        for (int i = 1; i < data.length; i++) {
            if (data[i].equals("")) {
                data[i] = "0";
            } else {
                data[i] = data[i].replace("%", "");
            }
        }

        newData.add(data);
    }

    private static void addWindData(ArrayList<String[]> newData, String[] data) {
        String[] speed = new String[data.length];

        speed[0] = "wind_speed";
        for (int i = 1; i < data.length; i++) {
            String va = data[i];
            if (va.equals("")) {
                speed[i] = "0";
            } else {
                try {
                    speed[i] = va.substring(0, va.indexOf("mi"));
                    Integer.valueOf(speed[i]);
                    if (speed[i].contains(" ")) {
                        int h = 0;
                    }
                    data[i] = va.substring(va.indexOf(" ") + 1);
                } catch (Exception ex) {
                    System.out.println(va);
                }
            }
        }

        newData.add(speed);

        HashMap<String, int[]> values = new HashMap<>();
        values.put("West - SouthWest", new int[]{0, 0, 0, 0, 0});
        values.put("North", new int[]{1, 0, 0, 0, 0});
        values.put("NorthWest", new int[]{0, 1, 0, 0, 0});
        values.put("South - SouthWest", new int[]{1, 1, 0, 0, 0});
        values.put("West - NorthWest", new int[]{0, 0, 1, 0, 0});
        values.put("East - SouthEast", new int[]{1, 0, 1, 0, 0});
        values.put("South", new int[]{0, 1, 1, 0, 0});
        values.put("South - SouthEast", new int[]{1, 1, 1, 0, 0});
        values.put("North - NorthEast", new int[]{0, 0, 0, 1, 0});
        values.put("North - NorthWest", new int[]{1, 0, 0, 1, 0});
        values.put("West", new int[]{0, 1, 0, 1, 0});
        values.put("SouthEast", new int[]{1, 1, 0, 1, 0});
        values.put("NorthEast", new int[]{0, 0, 1, 1, 0});
        values.put("SouthWest", new int[]{1, 0, 1, 1, 0});
        values.put("East", new int[]{0, 1, 1, 1, 0});
        values.put("East - NorthEast", new int[]{1, 1, 1, 1, 0});
        values.put("0", new int[]{0, 0, 0, 0, 1});
        values.put("", new int[]{1, 0, 0, 0, 1});

        String[][] columns = new String[5][];

        for (int i = 0; i < 5; i++) {
            columns[i] = new String[data.length];
            columns[i][0] = "wind_direction_" + (i + 1);
        }

        for (int i = 1; i < data.length; i++) {
            if (i == 658) {
                int h = 0;
            }

            int[] bits = values.get(data[i]);

            for (int j = 0; j < 5; j++) {
                columns[j][i] = String.valueOf(bits[j]);
            }
        }

        newData.addAll(Arrays.asList(columns).subList(0, 5));

    }

    private static void addWeatherSummaryData(ArrayList<String[]> newData, String[] data) {
        HashMap<String, int[]> values = new HashMap<>();
        values.put("Clear", new int[]{0, 0, 0, 0, 0, 0});
        values.put("Overcast", new int[]{1, 0, 0, 0, 0, 0});
        values.put("Partly Cloudy", new int[]{0, 1, 0, 0, 0, 0});
        values.put("Mostly Cloudy", new int[]{1, 1, 0, 0, 0, 0});
        values.put("Possible Drizzle", new int[]{0, 0, 1, 0, 0, 0});
        values.put("Fair", new int[]{1, 0, 1, 0, 0, 0});
        values.put("A Few Clouds", new int[]{0, 1, 1, 0, 0, 0});
        values.put("Breezy", new int[]{1, 1, 1, 0, 0, 0});
        values.put("Mostly Clear", new int[]{0, 0, 0, 1, 0, 0});
        values.put("Overcast and Breezy", new int[]{1, 0, 0, 1, 0, 0});
        values.put("Fog", new int[]{0, 1, 0, 1, 0, 0});
        values.put("Mostly Cloudy and Breezy", new int[]{1, 1, 0, 1, 0, 0});
        values.put("Humid and Mostly Cloudy", new int[]{0, 0, 1, 1, 0, 0});
        values.put("Rain", new int[]{1, 0, 1, 1, 0, 0});
        values.put("Flurries", new int[]{0, 1, 1, 1, 0, 0});
        values.put("Light Rain", new int[]{1, 1, 1, 1, 0, 0});
        values.put("Fair with Haze", new int[]{0, 0, 0, 0, 1, 0});
        values.put("Light Freezing Rain", new int[]{1, 0, 0, 0, 1, 0});
        values.put("Overcast with Haze", new int[]{0, 1, 0, 0, 1, 0});
        values.put("Sunny", new int[]{1, 1, 0, 0, 1, 0});
        values.put("Showers in Vicinity", new int[]{0, 0, 1, 0, 1, 0});
        values.put("0", new int[]{1, 0, 1, 0, 1, 0});
        values.put("Fair and Breezy", new int[]{0, 1, 1, 0, 1, 0});
        values.put("Thunderstorm Rain Fog/Mist", new int[]{1, 1, 1, 0, 1, 0});
        values.put("Showers", new int[]{0, 0, 0, 1, 1, 0});
        values.put("Rain Fog/Mist", new int[]{1, 0, 0, 1, 1, 0});
        values.put("Drizzle", new int[]{0, 1, 0, 1, 1, 0});
        values.put("Snow", new int[]{1, 1, 0, 1, 1, 0});
        values.put("Areas Drizzle", new int[]{0, 0, 1, 1, 1, 0});
        values.put("Fog/Mist", new int[]{1, 0, 1, 1, 1, 0});
        values.put("Partly Cloudy with Haze", new int[]{0, 1, 1, 1, 1, 0});
        values.put("Chance Showers", new int[]{1, 1, 1, 1, 1, 0});
        values.put("Light Rain Fog/Mist", new int[]{0, 0, 0, 0, 0, 1});
        values.put("Partly Cloudy and Breezy", new int[]{1, 0, 0, 0, 0, 1});
        values.put("Light Snow", new int[]{0, 1, 0, 0, 0, 1});
        values.put("Light Drizzle Fog/Mist", new int[]{1, 1, 0, 0, 0, 1});
        values.put("Light Snow Fog/Mist", new int[]{0, 0, 1, 0, 0, 1});
        values.put("Humid and Partly Cloudy", new int[]{1, 0, 1, 0, 0, 1});
        values.put("Wintry Mix", new int[]{0, 1, 1, 0, 0, 1});
        values.put("Lt Rain", new int[]{1, 1, 1, 0, 0, 1});
        values.put("\"Mod Rain", new int[]{0, 0, 0, 1, 0, 1});
        values.put("Heavy Rain", new int[]{1, 0, 0, 1, 0, 1});
        values.put("Heavy Rain Fog/Mist", new int[]{0, 1, 0, 1, 0, 1});
        values.put("Thunderstorm", new int[]{1, 1, 0, 1, 0, 1});
        values.put("Foggy", new int[]{0, 0, 1, 1, 0, 1});
        values.put("Heavy Snow Freezing Fog", new int[]{1, 0, 1, 1, 0, 1});
        values.put("Possible Light Rain", new int[]{0, 1, 1, 1, 0, 1});
        values.put("Overcast and Windy", new int[]{1, 1, 1, 1, 0, 1});
        values.put("Dry and Partly Cloudy", new int[]{0, 0, 0, 0, 1, 1});
        values.put("Dry", new int[]{1, 0, 0, 0, 1, 1});
        values.put("Humid", new int[]{0, 1, 0, 0, 1, 1});
        values.put("Thunderstorm Heavy Rain Fog/Mist", new int[]{1, 1, 0, 0, 1, 1});
        values.put("A Few Clouds with Haze", new int[]{0, 0, 1, 0, 1, 1});
        values.put("A few Clouds", new int[]{1, 0, 1, 0, 1, 1});
        values.put("\"Thunder", new int[]{0, 1, 1, 0, 1, 1});
        values.put("Areas Fog", new int[]{1, 1, 1, 0, 1, 1});
        values.put("Chance Snow", new int[]{0, 0, 0, 1, 1, 1});
        values.put("Cloudy", new int[]{1, 0, 0, 1, 1, 1});
        values.put("Snow and Breezy", new int[]{0, 1, 0, 1, 1, 1});
        values.put("Mostly Sunny", new int[]{1, 1, 0, 1, 1, 1});

        String[][] columns = new String[6][];

        for (int i = 0; i < 6; i++) {
            columns[i] = new String[data.length];
            columns[i][0] = "kickoff_weather_summary_x_bit_" + (i + 1);
        }

        for (int i = 1; i < data.length; i++) {
            int[] bits = values.get(data[i]);

            for (int j = 0; j < 6; j++) {
                columns[j][i] = String.valueOf(bits[j]);
            }
        }

        newData.addAll(Arrays.asList(columns).subList(0, 6));
    }

    private static void printUniques(String[] data) {
        ArrayList<String> values = new ArrayList<>();

        for (int i = 1; i < data.length; i++) {
            if (!values.contains(data[i])) {
                values.add(data[i]);
            }
        }

        int count = (int) Math.ceil(Math.log(values.size()) / Math.log(2));
        int i = 0;
        for (String v : values) {
            String encoded = "";
            String del = "";
            int value = i;
            for (int j = 0; j < count; j++) {
                int bit = value & 0x0001;
                encoded += del;
                encoded += bit;
                del = ",";

                value = value >> 1;
            }
            System.out.println("values.put(\"" + v.replace("\"", "\\\"") + "\", new int[] {" + encoded + "});");
            i++;
        }
    }

    private static void addDomeData(ArrayList<String[]> newData, String[] dome) {
        for (int i = 1; i < dome.length; i++) {
            if (dome[i].equals("Y")) {
                dome[i] = "1";
            } else {
                dome[i] = "0";
            }
        }

        newData.add(dome);
    }

    private static void addPositionData(ArrayList<String[]> newData, String[] positions) {
        HashMap<String, int[]> values = new HashMap<>();
        values.put("K", new int[]{0, 0, 1});
        values.put("QB", new int[]{0, 1, 0});
        values.put("RB", new int[]{0, 1, 1});
        values.put("TE", new int[]{1, 0, 0});
        values.put("WR", new int[]{1, 0, 1});

        String[] col1 = new String[positions.length];
        String[] col2 = new String[positions.length];
        String[] col3 = new String[positions.length];
        col1[0] = "position_bit_1";
        col2[0] = "position_bit_2";
        col3[0] = "position_bit_3";

        for (int i = 1; i < positions.length; i++) {
            int[] bits = values.get(positions[i]);

            col1[i] = String.valueOf(bits[0]);
            col2[i] = String.valueOf(bits[1]);
            col3[i] = String.valueOf(bits[2]);
        }

        newData.add(col1);
        newData.add(col2);
        newData.add(col3);
    }

    private static String[][] transpose(String[][] data) {
        String[][] result = new String[data[0].length][];
        for (int i = 0; i < result.length; i++) {
            result[i] = new String[data.length];
        }

        for (int i = 0; i < data.length; i++) {
            for (int j = 0; j < data[i].length; j++) {
                result[j][i] = data[i][j];
            }
        }

        return result;
    }

    private static void saveCSV(String[][] data, String path) {
        StringBuilder result = new StringBuilder();
        int i = 0;
        for (String[] line : data) {
            String del = "";
            for (String value : line) {
                result.append(del);
                del = ",";
                if (value == null || value.equals("")) {
                    result.append("0");
                } else {
                    result.append(value);
                }
            }
            result.append("\n");
            i++;
        }

        writeAllText(path, result.toString());
    }

    public static String[][] loadData(String path) {
        String[][] result = null;
        ArrayList<String> lines = readAllLines(path);
        String[] header = lines.get(0).split(",");
        headerList = Arrays.asList(header);

        result = new String[lines.size()][];
        lines.remove(0);
        for (int i = 0; i < result.length; i++) {
            result[i] = new String[44];
        }

        setValuesInResult(result[0], header, headerList);
        int i = 1;
        for (String line : lines) {
            String[] parts = line.replace(",,", ",0,").split(",");

            setValuesInResult(result[i], parts, headerList);
            i++;
        }

        return result;
    }

    private static void setValuesInResult(String[] row, String[] parts, List<String> headers) {
        row[0] = getValueFromParts(headers, parts, "age");
        row[1] = getValueFromParts(headers, parts, "game_num");
        row[2] = getValueFromParts(headers, parts, "position");
        row[3] = getValueFromParts(headers, parts, "away");
        row[4] = getValueFromParts(headers, parts, "kickoff_dome_x");
        row[5] = getValueFromParts(headers, parts, "kickoff_weather_summary_x");
        row[8 - 2] = getValueFromParts(headers, parts, "kickoff_wind_x");
        row[9 - 2] = getValueFromParts(headers, parts, "kickoff_humidity_x");
        row[10 - 2] = getValueFromParts(headers, parts, "kickoff_visibility_x");
        row[11 - 2] = getValueFromParts(headers, parts, "kickoff_barometer_x");
        row[12 - 2] = getValueFromParts(headers, parts, "kickoff_dew_point_x");
        row[13 - 2] = getValueFromParts(headers, parts, "kickoff_cloud_cover_x");
        row[14 - 2] = getValueFromParts(headers, parts, "all_td");
        row[15 - 2] = getValueFromParts(headers, parts, "def_int_td");
        row[16 - 2] = getValueFromParts(headers, parts, "fga");
        row[17 - 2] = getValueFromParts(headers, parts, "fgm");
        row[18 - 2] = getValueFromParts(headers, parts, "kick_ret");
        row[19 - 2] = getValueFromParts(headers, parts, "kick_ret_td");
        row[20 - 2] = getValueFromParts(headers, parts, "kick_ret_yds");
        row[21 - 2] = getValueFromParts(headers, parts, "pass_att");
        row[22 - 2] = getValueFromParts(headers, parts, "pass_cmp");
        row[23 - 2] = getValueFromParts(headers, parts, "pass_int");
        row[24 - 2] = getValueFromParts(headers, parts, "pass_rating");
        row[25 - 2] = getValueFromParts(headers, parts, "pass_sacked");
        row[26 - 2] = getValueFromParts(headers, parts, "pass_sacked_yds");
        row[27 - 2] = getValueFromParts(headers, parts, "pass_td");
        row[28 - 2] = getValueFromParts(headers, parts, "pass_yds");
        row[30 - 1 - 2] = getValueFromParts(headers, parts, "punt_ret");
        row[31 - 1 - 2] = getValueFromParts(headers, parts, "punt_ret_td");
        row[32 - 1 - 2] = getValueFromParts(headers, parts, "punt_ret_yds");
        row[33 - 1 - 2] = getValueFromParts(headers, parts, "punt_ret_yds_per_ret");
        row[34 - 1 - 2] = getValueFromParts(headers, parts, "punt_yds_per_punt");
        row[35 - 1 - 2] = getValueFromParts(headers, parts, "rec");
        row[36 - 1 - 2] = getValueFromParts(headers, parts, "rec_td");
        row[37 - 1 - 2] = getValueFromParts(headers, parts, "rec_yds");
        row[38 - 1 - 2] = getValueFromParts(headers, parts, "rush_att");
        row[39 - 1 - 2] = getValueFromParts(headers, parts, "rush_td");
        row[40 - 1 - 2] = getValueFromParts(headers, parts, "rush_yds");
        row[41 - 1 - 2] = getValueFromParts(headers, parts, "scoring");
        row[42 - 1 - 2] = getValueFromParts(headers, parts, "targets");
        row[43 - 1 - 2] = getValueFromParts(headers, parts, "two_pt_md");
        row[44 - 1 - 2] = getValueFromParts(headers, parts, "xpa");
        row[45 - 1 - 2] = getValueFromParts(headers, parts, "xpm");
        row[46 - 1 - 2] = getValueFromParts(headers, parts, "gs");
    }

    private static String getValueFromParts(List<String> headers, String[] parts, String field) {
        int index = headers.indexOf(field);
        if (index < parts.length) {
            return parts[index];
        }

        return "";
    }

    public static String readAllText(String path) {
        try {
            FileInputStream fs = new FileInputStream(path);
            byte[] data = new byte[fs.available()];

            fs.read(data);
            fs.close();

            return new String(data);
        } catch (Exception e) {
//            e.printStackTrace();
        }

        return null;
    }

    public static ArrayList<String> readAllLines(String path) {
        String[] lines = readAllText(path).split("\n");
        ArrayList<String> result = new ArrayList<>();

        for (String line : lines) {
            String ln = line.replace("\r", "");
            result.add(ln);
        }

        return result;
    }

    public static void writeAllText(String path, String content) {
        try {
            writeAllBytes(path, content.getBytes("utf-8"));
        } catch (UnsupportedEncodingException e) {
            writeAllBytes(path, content.getBytes());
        }
    }

    public static void writeAllBytes(String path, byte[] content) {
        try {
            FileOutputStream fs = new FileOutputStream(path);
            fs.write(content);

            fs.flush();
            fs.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}
