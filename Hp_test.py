import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from statsmodels.formula.api import ols
from sklearn.model_selection import KFold
from sklearn import svm
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import scikitplot as skplt


def t_test_positions():
    """This function handles the first hypothesis using t-test,
    where we are interested to see if there is a significant difference between
    the means of receptions of Wide Receivers and Tight Ends."""
    qb_fantasy = fantasy_df[(fantasy_df['Position'] == 'WR')&(fantasy_df['Receptions'] >5)]['Receptions']
    rb_fantasy = fantasy_df[(fantasy_df['Position'] == 'TE')& (fantasy_df['Receptions'] >5)]['Receptions']
    _, pvalue = stats.ttest_ind(qb_fantasy, rb_fantasy)
    return format(pvalue, '.20f')


def linear_regression():
    """This function handles the second hypothesis using Linear Regression,
    where we are interested to see if the more intense the wind is, the less passing is completed."""
    df = merged_df[(merged_df['kickoff_dome_x'] == "N")]
    df = df[pandas.notnull(df['kickoff_wind_x'])]
    df["wind_intensity"], df["wind_direction"] = zip(*df['kickoff_wind_x'].apply(lambda x: x.split("mi")))
    df["wind_intensity"] = df["wind_intensity"].astype(int)
    df = df[df["pass_cmp_perc"] > 0]
    model = ols(formula="pass_cmp_perc ~ wind_intensity", data=df).fit()
    print(model.pvalues)


def get_parts_of_df(position):
    """This function helps getting part of the original data, which only includes Quarterback's
     passing completion percentage when the game is not played in a dome."""

    # Filter out undesired positions, and in-dome games.
    qb_df = merged_df[(merged_df['position'] == position) & (merged_df['kickoff_dome_x'] == "N")]
    qb_df = qb_df[pandas.notnull(qb_df['kickoff_wind_x'])]
    # Separate kickoff_wind as wind intensity and wind direction.
    qb_df["wind_intensity"], qb_df["wind_direction"] = zip(*qb_df['kickoff_wind_x'].apply(lambda x: x.split("mi")))

    # Get weather related columns
    passing_attribute_names = ["kickoff_weather_summary_x", "kickoff_humidity_x",
                               "kickoff_visibility_x", "wind_intensity", "wind_direction",
                               "kickoff_dew_point_x", "pass_cmp_perc"]
    passing_weather_df = qb_df[passing_attribute_names].copy()
    return passing_weather_df


def clean_weather_df(df):
    """This function cleans the data, and replaces the string labels with numbers"""
    df = df.dropna()
    m = string_to_int(df, "wind_direction")
    df.replace({"wind_direction": m}, inplace=True)
    m = string_to_int(df, "kickoff_weather_summary_x")
    df.replace({"kickoff_weather_summary_x": m}, inplace=True)
    df["pass_cmp_perc"].replace("%", '', inplace=True)
    df["pass_cmp_perc"].astype(int)
    # Filter out low passing completion percentage.
    df = df[df["pass_cmp_perc"] >= 0]
    df["wind_intensity"] = df["wind_intensity"].astype(int)
    df["kickoff_visibility_x"] = df["kickoff_visibility_x"].astype(int)
    return df


def string_to_int(df, col_name):
    """This is a helper function for converting the string labels to numerical"""
    i = 0
    m = {}
    for e in df[col_name].unique():
        m.update({e: i})
        i += 1
    return m


def create_bins_width(df, col_name, bin_num):
    """This function cuts bins using equal width method"""
    max = df[col_name].max()
    min = df[col_name].min()
    bins = np.arange(min, max, bin_num)
    new_col_name = col_name + " group"
    df[new_col_name] = np.digitize(df[col_name], bins)
    df.drop(col_name, axis=1, inplace=True)
    return df


def create_bins_depth(df, col_name, bin_num):
    """This function cuts bins using equal depth method"""
    new_col_name = col_name + " group"
    df[new_col_name] = pandas.qcut(df[col_name], bin_num, labels=list(range(bin_num)))
    df[new_col_name] = df[new_col_name].astype(int)
    df.drop(col_name, axis=1, inplace=True)
    return df


def draw_roc_curve(name, model, X_validate, Y_validate):
    """This functions draws ROC graphs."""
    predicted_probas = model.predict_proba(X_validate)
    skplt.metrics.plot_roc(Y_validate, predicted_probas)
    # uncomment here to see the plots(Included in the write-up)
    # plt.show()
    # plt.savefig(name)


def separate_training_testing(myData):
    """This function seperates the training sets and validation sets."""
    valueArray = myData.values
    X = valueArray[:, 0:myData.shape[1] - 1]
    Y = valueArray[:, myData.shape[1] - 1]
    test_size = 0.20
    seed = 7
    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=test_size, random_state=seed)
    return X_train, X_validate, Y_train, Y_validate


def model_evaluate(X_train, X_validate, Y_train, Y_validate, num_folds, num_instances, seed, scoring, models):
    """"This function handles evaluation of machine learning methods"""
    results = []
    names = []
    for name, model in models:
        kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=False)
        cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        model.fit(X_train, Y_train)
        draw_roc_curve(name, model, X_validate, Y_validate)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)


def hypothesis(position, models, bin_width):
    """This function is the driver code for the third hypothesis
    where we are interested to see if we can predict Quarterbacks's
    passing completion percentage based on the weather.

    Args:
        position: Player's position
        models: A list of machine learning models used in this hypothesis
        bin_width: Width of passing completion percentage bins.
    """
    passing_weather_df = get_parts_of_df(position)
    cleaned_weather_df = clean_weather_df(passing_weather_df)
    cleaned_weather_df = create_bins_width(cleaned_weather_df,"kickoff_humidity_x", 20)
    cleaned_weather_df = create_bins_width(cleaned_weather_df, "kickoff_dew_point_x", 20)
    cleaned_weather_df = create_bins_width(cleaned_weather_df, "wind_intensity", 3)
    # Performance using equal depth is really low. Here I decided to use equal width.
    cleaned_weather_df = create_bins_width(cleaned_weather_df, "pass_cmp_perc", bin_width)
    # cleaned_weather_df.to_csv("cleaned_weather_df_0.csv", encoding='utf-8', index=False)
    X_train, X_validate, Y_train, Y_validate = separate_training_testing(cleaned_weather_df)
    model_evaluate(X_train, X_validate, Y_train, Y_validate, 10, len(X_train), 7, 'accuracy', models)


def main():
    print(t_test_positions())
    models_hype1 = [('KNN', KNeighborsClassifier()), ('CART', DecisionTreeClassifier()),
                    ('RFC', RandomForestClassifier()),('NB', GaussianNB()),
                    ('SVM', svm.SVC(gamma=0.001, decision_function_shape='ovo', probability=True))]
    linear_regression()
    hypothesis("QB", models_hype1, 25)

if __name__ == "__main__":
    # fantasy_df = pandas.read_csv("clean_fantasy_data.csv")
    fantasy_url = "https://raw.githubusercontent.com/madelinenlee/COSC587/master/cleaned_data/clean_fantasy_data.csv"
    fantasy_df = pandas.read_csv(fantasy_url,
                                 index_col=0, parse_dates=[0])
    # merged_df = pandas.read_csv("merged_data.csv")
    merged_url = "https://raw.githubusercontent.com/madelinenlee/COSC587/master/cleaned_data/merged_data.csv"
    merged_df = pandas.read_csv(merged_url,
        index_col=0, parse_dates=[0])
    main()
