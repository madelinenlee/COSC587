import os

import numpy
import pandas
import sklearn
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification

DATA_SETS = ["all_td", "def_int_td", "fga", "fgm", "kick_ret", "kick_ret_td", "kick_ret_yds", "pass_att", "pass_cmp",
             "pass_int", "pass_rating", "pass_sacked", "pass_sacked_yds", "pass_td", "pass_yds", "punt_ret",
             "punt_ret_td", "punt_ret_yds", "punt_ret_yds_per_ret", "punt_yds_per_punt", "rec", "rec_td", "rec_yds",
             "rush_att", "rush_td", "rush_yds", "scoring", "targets", "two_pt_md", "xpa", "xpm"]
POSITIONS = ["K", "QB", "RB", "TE", "WR"]
SEED = 12
FEATURE_COUNT = 25
TRAIN_RATIO = 0.6
ITERATION_COUNT = 100

MODELS = [
    'linear_regression',
    # 'keras',
    # 'svr',
    # 'knn',
    # 'dt'
]


# create model
def baseline_model():
    model = Sequential()
    model.add(Dense(FEATURE_COUNT, input_dim=FEATURE_COUNT, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(20, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(10, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(5, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    # print(model.summary())
    return model


def split_to_train_test(X, Y):
    l = len(X)
    train_count = int(l * TRAIN_RATIO)

    x_train = X[0:train_count, ]
    x_test = X[train_count:, ]

    y_train = Y[0:train_count, ]
    y_test = Y[train_count:, ]

    # load test data
    dataset = numpy.loadtxt("../test_data/" + DATASET_FILE_NAME + ".csv", delimiter=",", skiprows=1)
    dataset = scale_data_set(dataset)

    # split into input (X) and output (Y) variables
    x_test = dataset[:, 0:FEATURE_COUNT]
    y_test = dataset[:, FEATURE_COUNT]

    return x_train, y_train, x_test, y_test


def scale_data_set(X):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(X)
    return scaler.transform(X)


def load_and_train_model():
    numpy.random.seed(SEED)
    # load dataset
    dataset = numpy.loadtxt("../training_data/" + DATASET_FILE_NAME + ".csv", delimiter=",", skiprows=1)
    dataset = scale_data_set(dataset)

    # split into input (X) and output (Y) variables
    X = dataset[:, 0:FEATURE_COUNT]
    Y = dataset[:, FEATURE_COUNT]

    x_train, y_train, x_test, y_test = split_to_train_test(X, Y)

    params = ''
    if CURRENT_MODEL == 'keras':
        estimator = train_neural_net_with_keras(x_train, y_train)
    elif CURRENT_MODEL == 'knn':
        estimator, params = train_decision_knn_regression(x_train, y_train, x_test, y_test)
    elif CURRENT_MODEL == 'svr':
        estimator, params = train_decision_svm_regression(x_train, y_train, x_test, y_test)
    elif CURRENT_MODEL == 'dt':
        estimator, params = train_decision_tree_for_regression(x_train, y_train, x_test, y_test)
    elif CURRENT_MODEL == 'linear_regression':
        estimator = train_linear_regression(x_train, y_train)

    return estimator, x_test, y_test, x_train, y_train, params


def train_neural_net_with_keras(x_train, y_train):
    # evaluate model with standardized dataset
    estimator = KerasRegressor(build_fn=baseline_model, epochs=ITERATION_COUNT, batch_size=5, verbose=2)
    estimator.fit(x_train, y_train)
    return estimator


def train_decision_tree_for_regression(x_train, y_train, x_test, y_test):
    # evaluate model with standardized dataset
    result = None
    params = ''
    min_error = 100

    # if DT_DEPTH is not None:
    #     estimator = DecisionTreeRegressor(max_depth=DT_DEPTH)
    #     return estimator, 'depth=' + str(DT_DEPTH)
    # else:
    for i in range(1, 21):
        estimator = DecisionTreeRegressor(max_depth=i)
        estimator.fit(x_train, y_train)

        y_pred_test = estimator.predict(x_test)
        error = numpy.average(calculate_error_abs(y_test, y_pred_test))
        if error < min_error:
            min_error = error
            result = estimator
            params = 'depth=' + str(i)

    return result, params


def train_decision_svm_regression(x_train, y_train, x_test, y_test):
    result = None
    params = ''
    min_error = 100

    # 2,6,9,2

    for deg in range(5, 16):
        _c = 0.0005
        while _c <= 0.002:
            _c += 0.0005

            # estimator = SVR(kernel='rbf', C=_c, gamma=_g)
            estimator = SVR(kernel='poly', C=_c, degree=deg)
            estimator.fit(x_train, y_train)

            y_pred_test = estimator.predict(x_test)
            error = numpy.average(calculate_error_abs(y_test, y_pred_test))
            if error < min_error:
                min_error = error
                result = estimator
                params = 'deg=' + str(deg) + ", C=" + str(_c)
            # evaluate model with standardized dataset
            # estimator = SVR(kernel='linear', C=1e3)
            # estimator.fit(x_train, y_train)
    return result, params


def train_decision_knn_regression(x_train, y_train, x_test, y_test):
    result = None
    params = ''
    min_error = 100

    # if KNN_N is not None:
    #     estimator = KNeighborsRegressor(n_neighbors=KNN_N)
    #     params = 'N=' + str(KNN_N)
    #
    #     return estimator, params
    # else:
    for i in range(1, 50):
        estimator = KNeighborsRegressor(n_neighbors=i)
        estimator.fit(x_train, y_train)

        y_pred_test = estimator.predict(x_test)
        error = numpy.average(calculate_error_abs(y_test, y_pred_test))
        if error < min_error:
            min_error = error
            result = estimator
            params = 'N=' + str(i)

    return result, params


def train_linear_regression(x_train, y_train):
    estimator = LinearRegression()
    estimator.fit(x_train, y_train)
    return estimator


def calculate_error_abs(truth, prediction):
    result = []

    for t, p in zip(truth, prediction):
        result.append(abs(t - p))

    return result


def main_model_training():
    results = []
    global DATASET_FILE_NAME
    global CURRENT_MODEL
    for model in MODELS:
        for ds in DATA_SETS:
            for position in POSITIONS:
                CURRENT_MODEL = model
                DATASET_FILE_NAME = ds + '-' + position
                if os.path.isfile("../training_data/" + DATASET_FILE_NAME + ".csv") and os.path.isfile(
                        "../test_data/" + DATASET_FILE_NAME + ".csv"):

                    estimator, x_test, y_test, x_train, y_train, params = load_and_train_model()
                    print('Training {} for {} on {}   -> params: {}'.format(model, position, ds, params))

                    y_pred_test = estimator.predict(x_test)
                    error_abs_test = calculate_error_abs(y_test, y_pred_test)

                    y_pred_train = estimator.predict(x_train)
                    error_abs_train = calculate_error_abs(y_train, y_pred_train)

                    data = {'truth': y_test, 'prediction': y_pred_test, 'error_abs': error_abs_test}
                    df = pandas.DataFrame(data=data)
                    df.to_csv("../predictions/" + DATASET_FILE_NAME + "-" + model + ".csv", index=False)

                    avg_train = numpy.average(error_abs_train)
                    avg_test = numpy.average(error_abs_test)
                    drop = 0
                    if avg_train != 0:
                        drop = round((avg_train - avg_test) * 100.0 / avg_train)

                    results.append({
                        'variable': ds,
                        'position': position,
                        'model': model,
                        'error_train_average': avg_train,
                        'error_train_std': numpy.std(error_abs_train),
                        'error_test_average': avg_test,
                        'error_test_std': numpy.std(error_abs_test),
                        'test_drop': '%' + str(drop),
                        'train_size': len(error_abs_train),
                        'test_size': len(error_abs_test),
                        'params': params
                    })

                df = pandas.DataFrame(results, columns=['variable', 'position', 'model', 'error_train_average',
                                                        'error_train_std',
                                                        'error_test_average', 'error_test_std', 'test_drop',
                                                        'train_size', 'test_size', 'params'])
                df.to_csv('../predictions/summary.csv', index=None)
                # print(results)


def knn_hyperpram_optimization():
    results = []
    global KNN_N
    global CURRENT_MODEL
    global DATASET_FILE_NAME
    CURRENT_MODEL = 'knn'
    position = 'WR'
    columns = {}
    order = []

    for i in range(10, 400, 5):
        values = []
        for ds in ['rec_yds']:
            KNN_N = i
            DATASET_FILE_NAME = ds + '-' + position
            if os.path.isfile("../training_data/" + DATASET_FILE_NAME + ".csv"):
                # print('Training {} for {} on {} (K={})'.format(CURRENT_MODEL, position, ds, i))

                estimator, x_test, y_test, x_train, y_train = load_and_train_model()

                y_pred_test = estimator.predict(x_test)
                error_abs_test = calculate_error_abs(y_test, y_pred_test)

                values.append(error_abs_test)
                print(str(i) + "," + str(numpy.average(error_abs_test)))

        # print(values)
        min = numpy.min(values)
        max = numpy.max(values)
        median = numpy.median(values)
        q1 = numpy.percentile(values, 25)
        q3 = numpy.percentile(values, 75)

        cells = [min, q1, median, q3, max]
        columns[str(i)] = cells
        order.append(str(i))

    df = pandas.DataFrame(data=columns)
    df.columns = order

    df.to_csv('/Users/yektaie/Desktop/hp/knn.csv')

    print(results)


def dt_hyperpram_optimization():
    results = []
    global DT_DEPTH
    global CURRENT_MODEL
    global DATASET_FILE_NAME
    CURRENT_MODEL = 'dt'
    position = 'WR'
    columns = {}
    order = []

    for i in range(1, 31):
        values = []
        for ds in ['rec']:
            DT_DEPTH = i
            DATASET_FILE_NAME = ds + '-' + position
            if os.path.isfile("../training_data/" + DATASET_FILE_NAME + ".csv"):
                # print('Training {} for {} on {} (K={})'.format(CURRENT_MODEL, position, ds, i))

                estimator, x_test, y_test, x_train, y_train = load_and_train_model()

                y_pred_test = estimator.predict(x_test)
                error_abs_test = calculate_error_abs(y_test, y_pred_test)

                values.append(error_abs_test)
                print(str(i) + "," + str(numpy.average(error_abs_test)))

        # print(values)
        min = numpy.min(values)
        max = numpy.max(values)
        median = numpy.median(values)
        q1 = numpy.percentile(values, 25)
        q3 = numpy.percentile(values, 75)

        cells = [min, q1, median, q3, max]
        columns[str(i)] = cells
        order.append(str(i))

    df = pandas.DataFrame(data=columns)
    df.columns = order

    df.to_csv('/Users/yektaie/Desktop/hp/knn.csv')

    print(results)


def svr_hyperpram_optimization():
    results = []
    global DT_DEPTH
    global CURRENT_MODEL
    global DATASET_FILE_NAME
    CURRENT_MODEL = 'svr'
    position = 'WR'
    columns = {}
    order = []

    global SVR_RBF_C
    global SVR_GAMMA

    result = ''
    i = 0
    _g = 0.01
    while _g <= 0.15:
        SVR_GAMMA = _g
        _g += 0.005
        _c = 0.00001
        delimiter = ''
        while _c <= 0.0015:
            SVR_RBF_C = _c
            _c += 0.00005
            i += 1
            for ds in ['rec_yds']:
                DT_DEPTH = i
                DATASET_FILE_NAME = ds + '-' + position
                if os.path.isfile("../training_data/" + DATASET_FILE_NAME + ".csv"):
                    # print('Training {} for {} on {} (K={})'.format(CURRENT_MODEL, position, ds, i))

                    estimator, x_test, y_test, x_train, y_train = load_and_train_model()

                    y_pred_test = estimator.predict(x_test)
                    error_abs_test = calculate_error_abs(y_test, y_pred_test)

                    result += (delimiter + str(numpy.average(error_abs_test)))
                    delimiter = ','
                    print(str(_g) + "," + str(_c * 100) + "," + str(numpy.average(error_abs_test)))

        # print(result)
        result = ''


def test_feature_selection():
    global CURRENT_MODEL
    global DATASET_FILE_NAME

    CURRENT_MODEL = 'dt'
    position = 'WR'
    DATASET_FILE_NAME = 'rec_yds' + '-' + position

    estimator, x_test, y_test, x_train, y_train, params = load_and_train_model()

    # a = estimator.coef_
    a = estimator.feature_importances_
    print(a)
    print(a.shape)

    return

    # The "accuracy" scoring is proportional to the number of correct
    # classifications
    rfecv = RFECV(estimator=estimator, step=1, cv=StratifiedKFold(2),
                  scoring='neg_mean_squared_error')
    rfecv.fit(x_train, y_train)

    print("Optimal number of features : %d" % rfecv.n_features_)

    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.show()


def main():
    test_feature_selection()


main()
