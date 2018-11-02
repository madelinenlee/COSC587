from statistics import stdev
import pandas as pd
import math
from apyori import apriori

# Some attribute in our dataset are completely independent. These attribute are inputs and rules
# where these attributes are making the antecedents are useless. This list holds those independent variables
# which will be pruned later in the code.
GIVEN_COLUMNS = ['age', 'game_date', 'game_num', 'position', 'away', 'dome', 'weather_summary', 'humidity',
                 'visibility', 'barometer', 'dew_point', 'cloud_cover', 'position']

POSITIONS = ['TE', 'WR', 'QB', 'RB']
SUPPORTS = [0.9, 0.7, 0.5, 0.3]


# Read the merged dataset and load in pandas data frame.
def load_data_to_be_processed():
    data_set = pd.read_csv('cleaned_data/merged_data.csv')
    return data_set


# Bins a specific variable in an equi width manner. The length of the bin is specified via {bin_width} parameter.
def bin_equiwidth_value(value, bin_width):
    result = ''

    value = str(value)
    if value != 'nan':
        value = float(value.replace('%', ''))
        lower_bound = int(int(value) / bin_width) * bin_width
        upper_bound = int(int(value + bin_width) / bin_width) * bin_width

        result = str(lower_bound) + '_' + str(upper_bound)

    return result


# Bin the values for catch_pct attribute.
# This attribute binning is a little different, it needs to remove the %
def bin_catch_pct_value(value):
    bin_width = 20
    result = ''

    value = str(value)
    if value != 'nan':
        value = float(value.replace('%', ''))
        lower_bound = int(int(value) / bin_width) * bin_width
        upper_bound = int(int(value + bin_width) / bin_width) * bin_width

        result = str(lower_bound) + '_' + str(upper_bound)

    return result


# Bin the values for game_num (the week/season) attribute.
def bin_game_num_value(x):
    x = int(x)
    result = ''

    if x < 6:
        result = 'begin_season'
    elif x < 12:
        result = 'middle_season'
    else:
        result = 'end_season'

    return result


# Special binning method for {kick_ret_yds}.
def bin_kick_ret_yds_value(x):
    result = ''

    if x < 0:
        result = 'neg'
    elif x <= 100:
        result = '0_100'
    elif x <= 200:
        result = '100_200'
    elif x <= 300:
        result = '200_300'

    return result


# Special binning method for binning according to attribute's value sign.
def bin_pos_neg_value(x):
    result = ''

    if x < 0:
        result = 'neg'
    elif x == 0:
        result = '0'
    else:
        result = 'pos'

    return result


# This method prepare the loaded dataset for associate rule mining.
# The operations of this function includes dropping columns, bin values and etc.
def prepare_data_for_association_rule(data):
    # I was forced to use large bins to reduce the number of parameters for apriori algorithm.
    # In the first pass, with ~2000 different possible items, the apriori worked for 5 hours. Watching
    # it working without leading to any result, I had to cancel and make the binning width greater.
    # I used the SD of each attribute as an intuition for binning size.

    # drop the first & second column of index
    data = data.drop(data.columns[1], axis=1)
    data = data.drop(data.columns[0], axis=1)

    # remove the rows were the player didn't played.
    data = data[data['gs'].map(lambda x: x) == 1]

    # bin age with equi width (width = 2)
    data['age'] = data['age'].map(lambda x: 'age' + ':' + bin_equiwidth_value(x, 5))

    # convert touch downs to items
    data['all_td'] = data['all_td'].map(lambda x: 'all_td:' + str(x))

    # bin catch_pct
    data['catch_pct'] = data['catch_pct'].map(lambda x: 'catch_pct:' + bin_catch_pct_value(x))

    # drop irrelevant columns, since all have same value
    data = data.drop(labels=['def_int_td', 'fg_perc', 'fga', 'fgm', 'gs'], axis=1)
    # drop date column
    data = data.drop(labels=['game_date', 'year_id'], axis=1)
    # drop teams/player column
    data = data.drop(labels=['team', 'opp', 'player'], axis=1)

    # bin game_num (3 bins: begin_season, middle_season, emd_season)
    data['game_num'] = data['game_num'].map(lambda x: 'game_num:' + bin_game_num_value(x))

    # use common functions to bin a large number of the attributes in the dataset.
    data['kick_ret'] = data['kick_ret'].map(lambda x: 'kick_ret:' + str(x))
    data['kick_ret_td'] = data['kick_ret_td'].map(lambda x: 'kick_ret_td:' + str(x))
    data['kick_ret_yds'] = data['kick_ret_yds'].map(lambda x: 'kick_ret_yds:' + bin_kick_ret_yds_value(x))
    data['kick_ret_yds_per_ret'] = data['kick_ret_yds_per_ret'].map(
        lambda x: 'kick_ret_yds_per_ret:' + bin_pos_neg_value(x))
    data['pass_adj_yds_per_att'] = data['pass_adj_yds_per_att'].map(
        lambda x: 'pass_adj_yds_per_att:' + bin_pos_neg_value(x))
    data['pass_att'] = data['pass_att'].map(lambda x: 'pass_att' + ':' + bin_equiwidth_value(x, 10))
    data['pass_cmp'] = data['pass_cmp'].map(lambda x: 'pass_cmp' + ':' + bin_equiwidth_value(x, 5))
    data['pass_cmp_perc'] = data['pass_cmp_perc'].map(lambda x: 'pass_cmp_perc' + ':' + bin_equiwidth_value(x, 20))
    data['pass_int'] = data['pass_int'].map(lambda x: 'pass_int:' + str(x))
    data['pass_rating'] = data['pass_rating'].map(lambda x: 'pass_rating' + ':' + bin_equiwidth_value(x, 30))
    data['pass_sacked'] = data['pass_sacked'].map(lambda x: 'pass_sacked' + ':' + bin_equiwidth_value(x, 3))
    data['pass_sacked_yds'] = data['pass_sacked_yds'].map(
        lambda x: 'pass_sacked_yds' + ':' + bin_equiwidth_value(x, 10))
    data['pass_td'] = data['pass_td'].map(lambda x: 'pass_td' + ':' + str(x))
    data['pass_yds'] = data['pass_yds'].map(lambda x: 'pass_yds' + ':' + bin_equiwidth_value(x, 100))
    data['pass_yds_per_att'] = data['pass_yds_per_att'].map(
        lambda x: 'pass_yds_per_att' + ':' + bin_equiwidth_value(x, 10))
    data['punt_ret'] = data['punt_ret'].map(lambda x: 'punt_ret' + ':' + bin_equiwidth_value(x, 1))
    data['punt_ret_td'] = data['punt_ret_td'].map(lambda x: 'punt_ret_td' + ':' + str(x))
    data['punt_ret_yds'] = data['punt_ret_yds'].map(lambda x: 'punt_ret_yds' + ':' + bin_equiwidth_value(x, 20))
    data['punt_ret_yds_per_ret'] = data['punt_ret_yds_per_ret'].map(
        lambda x: 'punt_ret_yds_per_ret' + ':' + bin_equiwidth_value(x, 10))
    data['punt_yds_per_punt'] = data['punt_yds_per_punt'].map(
        lambda x: 'punt_yds_per_punt' + ':' + bin_equiwidth_value(x, 5))
    data['ranker'] = data['ranker'].map(lambda x: 'ranker' + ':' + bin_equiwidth_value(x, 50))
    data['rec'] = data['rec'].map(lambda x: 'rec' + ':' + bin_equiwidth_value(x, 5))
    data['rec_yds'] = data['rec_yds'].map(lambda x: 'rec_yds' + ':' + bin_equiwidth_value(x, 50))
    data['rec_yds_per_rec'] = data['rec_yds_per_rec'].map(
        lambda x: 'rec_yds_per_rec' + ':' + bin_equiwidth_value(x, 155))
    data['rec_yds_per_tgt'] = data['rec_yds_per_tgt'].map(
        lambda x: 'rec_yds_per_tgt' + ':' + bin_equiwidth_value(x, 10))
    data['rush_att'] = data['rush_att'].map(lambda x: 'rush_att' + ':' + bin_equiwidth_value(x, 10))
    data['rush_td'] = data['rush_td'].map(lambda x: 'rush_td' + ':' + str(x))
    data['rush_yds'] = data['rush_yds'].map(lambda x: 'rush_yds' + ':' + bin_equiwidth_value(x, 40))
    data['rush_yds_per_att'] = data['rush_yds_per_att'].map(
        lambda x: 'rush_yds_per_att' + ':' + bin_equiwidth_value(x, 10))
    data['scoring'] = data['scoring'].map(lambda x: 'scoring' + ':' + bin_equiwidth_value(x, 5))
    data['targets'] = data['targets'].map(lambda x: 'targets' + ':' + bin_equiwidth_value(x, 5))
    data['two_pt_md'] = data['two_pt_md'].map(lambda x: 'two_pt_md' + ':' + str(x))
    data['xp_perc'] = data['xp_perc'].map(lambda x: 'xp_perc' + ':' + bin_equiwidth_value(x, 20))
    data['rec_td'] = data['rec_td'].map(lambda x: 'rec_td' + ':' + str(x))
    data['xpa'] = data['xpa'].map(lambda x: 'xpa' + ':' + str(x))
    data['position'] = data['position'].map(lambda x: 'position' + ':' + str(x))
    data['xpm'] = data['xpm'].map(lambda x: 'xpm' + ':' + str(x))
    data['away'] = data['away'].map(lambda x: 'away' + ':' + str(x))

    # this field is useless
    data = data.drop(labels=['ranker'], axis=1)

    # drop the duplicate after merging data and other unused column
    data = data.drop(labels=['home_team', 'away_team', 'game_pl_1', 'kickoff_feels_like_x', 'kickoff_temperature_x',
                             'kickoff_wind_x'], axis=1)

    # binning and preparing the weather attributes using those same functions.
    data['kickoff_dome_x'] = data['kickoff_dome_x'].map(lambda x: 'dome' + ':' + str(x))
    data['kickoff_weather_summary_x'] = data['kickoff_weather_summary_x'].map(
        lambda x: 'weather_summary' + ':' + str(x))
    data['kickoff_humidity_x'] = data['kickoff_humidity_x'].map(lambda x: 'humidity' + ':' + bin_equiwidth_value(x, 20))
    data['kickoff_visibility_x'] = data['kickoff_visibility_x'].map(
        lambda x: 'visibility' + ':' + bin_equiwidth_value(x, 15))
    data['kickoff_barometer_x'] = data['kickoff_barometer_x'].map(
        lambda x: 'barometer' + ':' + bin_equiwidth_value(x, 1))
    data['kickoff_dew_point_x'] = data['kickoff_dew_point_x'].map(
        lambda x: 'dew_point' + ':' + bin_equiwidth_value(x, 20))
    data['kickoff_cloud_cover_x'] = data['kickoff_cloud_cover_x'].map(
        lambda x: 'cloud_cover' + ':' + bin_equiwidth_value(x, 20))

    return data


# Util function: If the value is NaN or empty, null will be returned, otherwise the value is returned
# unchanged
def nullify_if_zero(x):
    if x == 0:
        return math.nan

    return x


# Removes all the 0/empty/NaN values form the dataset and replace with null.
# Although missing values are not suitable for data analysis task, but in this case, By removing the
# zeros and empty values from the dataset, I considerably reduced the number of possible items.
# As mentioned before, with large number of possible items, the apriory becomes extremely SLOW.
def remove_all_zero_values(data):
    for column in data.columns:
        data[column] = data[column].map(lambda x: nullify_if_zero(x))

    return data


# Prior to running apriori algorithm, the dataset should be converted to item lists.
# This function transform a pandas data frame into transaction sets.
def convert_records_to_item_set():
    _records = []
    for i in range(0, data.shape[0]):
        record = []
        for j in range(0, data.shape[1]):
            value = str(data.values[i, j])
            # values with empty, 0 or NaN with ends with eighter : or :nan
            # I ignore these values to reduce the variable domain size.
            if not (value.endswith(':') or value.endswith(':nan')):
                record.append(value)

        if len(record) > 0:
            _records.append(record)

    return _records


# Util method: get the name of a feature from an item in a transaction set.
def get_feature(item):
    if ':' in item:
        ret = item[0:item.index(':')]
        return ret
    return item


# Print the list of the rules extracted.
def print_extracted_rules():
    global pruned_rule_count
    pruned_rule_count = 0
    for rule in association_results:
        support = rule.support
        ordered_statistics = rule.ordered_statistics
        confidences = []
        # Prints all the possible permutation of the rules with their respective confidence
        for order in ordered_statistics:
            base = str(order.items_base).replace('frozenset({', '').replace('})', '').replace("'", '')
            add = str(order.items_add).replace('frozenset({', '').replace('})', '').replace("'", '')
            print('{} -> {}'.format(base, add))
            print('Support: ' + str(support))
            print('Confidence: ' + str(order.confidence))
            confidences.append(order.confidence)
            print('-----------------------------------------')

        if len(confidences) >= 2:
            print('Confidence SD: ' + str(stdev(confidences)))
        print()
        print()
        print()


# filter all rows not specific a given position
def filter_data_on_position(data, position):
    data = data[data['position'].map(lambda x: x) == position]
    return data


def get_rule_side_variable_count(base):
    inp = 0
    output = 0

    parts = base.split(', ')
    for part in parts:
        if ':' in part:
            p = part[0:part.index(":")]
            if p in GIVEN_COLUMNS:
                inp += 1
            else:
                output += 1
        else:
            output += 1

    return inp, output


def is_valid_rule(base, add):
    base_i, base_o = get_rule_side_variable_count(base)
    add_i, add_o = get_rule_side_variable_count(add)

    if base_o == 0 and add_o == 0:
        return False

    if add_o == 0:
        return False

    return True


def get_valid_rule_count(rules):
    result = 0

    for rule in rules:
        ordered_statistics = rule.ordered_statistics
        for order in ordered_statistics:
            base = str(order.items_base).replace('frozenset({', '').replace('})', '').replace("'", '')
            add = str(order.items_add).replace('frozenset({', '').replace('})', '').replace("'", '')
            if is_valid_rule(base, add):
                result += 1

    return result


def get_rule_count(rules):
    result = 0

    for rule in rules:
        ordered_statistics = rule.ordered_statistics
        for order in ordered_statistics:
            result += 1

    return result


# put every thing together to extract rules from the dataset.
def main():
    global data, association_results
    # configs for better print describe function
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    for min_support in SUPPORTS:
        print('=============================================================')
        for position in POSITIONS:
            data = load_data_to_be_processed()
            data = filter_data_on_position(data, position)
            data = remove_all_zero_values(data)
            data = prepare_data_for_association_rule(data)
            # data.to_csv('/Users/yektaie/Desktop/temp.csv', index=False)
            #
            records = convert_records_to_item_set()
            min_support = min_support
            min_confidence = 0.7
            association_rules = apriori(records, min_support=min_support, min_confidence=min_confidence, min_length=2)
            association_results = list(association_rules)

            print('Support: ' + str(min_support))
            print('Position: ' + position)
            valid_rule = get_valid_rule_count(association_results)
            total_rule = get_rule_count(association_results)
            pruned_p = (total_rule - valid_rule) * 100.0 / total_rule
            print('Valid Rules:' + str(valid_rule))
            print('Total Rules:' + str(total_rule) + " " + str(pruned_p) + '%')
            print_extracted_rules()
            # print('Total rule extracted: ' + str(len(association_results)))
            # print('Pruned rule: ' + str(pruned_rule_count))
            print('-------------------------------------------------------')


if __name__ == '__main__':
    main()
