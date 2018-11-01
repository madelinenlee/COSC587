from pprint import pprint

import pandas as pd
import math
from apyori import apriori

GIVEN_COLUMNS = ['age', 'game_date', 'game_num', 'position', 'away']


def load_data_to_be_processed():
    data_set = pd.read_csv('cleaned_data/clean_historical_data.csv')
    return data_set


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


def bin_equiwidth_value(value, bin_width):
    result = ''

    value = str(value)
    if value != 'nan':
        value = float(value.replace('%', ''))
        lower_bound = int(int(value) / bin_width) * bin_width
        upper_bound = int(int(value + bin_width) / bin_width) * bin_width

        result = str(lower_bound) + '_' + str(upper_bound)

    return result


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


def bin_pos_neg_value(x):
    result = ''

    if x < 0:
        result = 'neg'
    elif x == 0:
        result = '0'
    else:
        result = 'pos'

    return result


def prepare_data_for_association_rule(data):
    # drop the first column of index
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
    data['xpm'] = data['xpm'].map(lambda x: 'xpm' + ':' + str(x))
    data['away'] = data['away'].map(lambda x: 'away' + ':' + str(x))

    # data = data.drop(labels=['kick_ret_td'], axis=1)
    # data = data.drop(labels=['kick_ret_yds'], axis=1)
    # data = data.drop(labels=['kick_ret_yds_per_ret'], axis=1)
    # data = data.drop(labels=['pass_adj_yds_per_att'], axis=1)
    # data = data.drop(labels=['pass_cmp_perc'], axis=1)
    # data = data.drop(labels=['pass_int'], axis=1)
    # data = data.drop(labels=['pass_sacked'], axis=1)
    # data = data.drop(labels=['pass_sacked_yds'], axis=1)
    # data = data.drop(labels=['pass_td'], axis=1)
    # data = data.drop(labels=['pass_yds'], axis=1)
    # data = data.drop(labels=['pass_yds_per_att'], axis=1)
    # data = data.drop(labels=['position'], axis=1)
    # data = data.drop(labels=['punt_ret'], axis=1)
    # data = data.drop(labels=['punt_ret_yds'], axis=1)
    # data = data.drop(labels=['punt_ret_yds_per_ret'], axis=1)
    # data = data.drop(labels=['punt_yds_per_punt'], axis=1)
    data = data.drop(labels=['ranker'], axis=1)
    # data = data.drop(labels=['rec_td'], axis=1)
    # data = data.drop(labels=['rec_yds'], axis=1)
    # data = data.drop(labels=['rec_yds_per_rec'], axis=1)
    # data = data.drop(labels=['rec_yds_per_tgt'], axis=1)
    # data = data.drop(labels=['rush_att'], axis=1)
    # data = data.drop(labels=['rush_yds'], axis=1)
    # data = data.drop(labels=['rush_yds_per_att'], axis=1)
    # data = data.drop(labels=['targets'], axis=1)
    # data = data.drop(labels=['two_pt_md'], axis=1)
    # data = data.drop(labels=['xpa'], axis=1)
    # data = data.drop(labels=['xpm'], axis=1)

    # data = data.drop(labels=['age'], axis=1)
    # data = data.drop(labels=['game_num'], axis=1)
    # data = data.drop(labels=['scoring'], axis=1)
    # data = data.drop(labels=['away'], axis=1)

    # data = data.drop(labels=['kick_ret'], axis=1)
    # data = data.drop(labels=['all_td'], axis=1)
    # data = data.drop(labels=['pass_att'], axis=1)
    # data = data.drop(labels=['catch_pct'], axis=1)
    # data = data.drop(labels=['pass_cmp'], axis=1)
    # data = data.drop(labels=['pass_rating'], axis=1)
    # data = data.drop(labels=['punt_ret_td'], axis=1)
    # data = data.drop(labels=['rec'], axis=1)
    # data = data.drop(labels=['rush_td'], axis=1)
    # data = data.drop(labels=['xp_perc'], axis=1)

    return data


def nullify_if_zero(x):
    if x == 0:
        return math.nan

    return x


def remove_all_zero_values(data):
    for column in data.columns:
        data[column] = data[column].map(lambda x: nullify_if_zero(x))

    return data


def convert_records_to_item_set():
    _records = []
    for i in range(0, data.shape[0]):
        record = []
        for j in range(0, data.shape[1]):
            value = str(data.values[i, j])
            if not (value.endswith(':') or value.endswith(':nan')):
                record.append(value)

        if len(record) > 0:
            _records.append(record)

    return _records


def is_useful_rule(_rule):
    _items = [x for x in _rule[0]]
    if len(_items) == 1:
        return _items[0] in GIVEN_COLUMNS
    else:
        result = False
        for i in range(1, len(_items)):
            if not _items[i] in GIVEN_COLUMNS:
                result = True
                break

        return result


def print_extracted_rules():
    global pruned_rule_count
    pruned_rule_count = 0
    for rule in association_results:
        if not is_useful_rule(rule):
            pruned_rule_count += 1
            continue

        # first index of the inner list
        # Contains base item and add item
        pair = rule[0]
        items = [x for x in pair]
        if len(items) == 1:
            print("Rule: " + items[0])
        else:
            r = ''
            for i in range(1, len(items)):
                r = r + ', ' + items[i]

            print("Rule: " + items[0] + ' -> ' + r[2:])
        # second index of the inner list
        print("Support: " + str(rule[1]))

        # third index of the list located at 0th
        # of the third index of the inner list

        print("Confidence: " + str(rule[2][0][2]))
        print("Lift: " + str(rule[2][0][3]))
        print("=====================================")


if __name__ == '__main__':
    # configs for better print describe function
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    #
    data = load_data_to_be_processed()
    data = remove_all_zero_values(data)
    data = prepare_data_for_association_rule(data)
    # data.to_csv('/Users/yektaie/Desktop/temp.csv', index=False)

    # print(data.describe())

    records = convert_records_to_item_set()

    support = 0.5
    confidence = 0.7

    association_rules = apriori(records, min_support=support, min_confidence=confidence, min_length=2)
    association_results = list(association_rules)

    print_extracted_rules()

    print('Total rule extracted: ' + str(len(association_results)))
    print('Pruned rule: ' + str(pruned_rule_count))
