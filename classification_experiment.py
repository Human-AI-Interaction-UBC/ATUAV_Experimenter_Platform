import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import RepeatedKFold
from sklearn import svm
import joblib
import pickle
import sklearn

def ten_ten_cv_rf(i):
    print("original experiment, window: " + str(i))
    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    model = RandomForestClassifier(max_features=16, bootstrap=False)
    score = np.zeros((10,10))
    rkf = RepeatedKFold(n_splits=10, n_repeats=10)
    repeat = 0
    fold = 0
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,: ]
        y_train, y_test = y[train_index], y[test_index]
        removeZeros = X_train.apply(lambda x: len(x.unique()) == 1)
        X_train = X_train.loc[:, ~removeZeros]
        X_test = X_test.loc[:, ~removeZeros]
        data_cor = X_train.corr()
        idx = np.abs(np.tril(data_cor, k=-1)) > .85
        idx_drop = np.any(idx, axis=1)
        X_train = X_train.loc[:, ~idx_drop]
        X_test = X_test.loc[:, ~idx_drop]
        clf = model.fit(X_train, y_train)
        score[repeat, fold] = clf.score(X_test, y_test)
        fold += 1
        if fold == 10:
            repeat += 1
            fold = 0
    mean_score = np.mean(score, axis=1)
    return np.mean(mean_score)

def ten_ten_cv_svm(i):
    print("original experiment, window: " + str(i))
    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    model = svm.LinearSVC()
    score = np.zeros((10,10))
    rkf = RepeatedKFold(n_splits=10, n_repeats=10)
    repeat = 0
    fold = 0
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,: ]
        y_train, y_test = y[train_index], y[test_index]
        removeZeros = X_train.apply(lambda x: len(x.unique()) == 1)
        X_train = X_train.loc[:, ~removeZeros]
        X_test = X_test.loc[:, ~removeZeros]
        data_cor = X_train.corr()
        idx = np.abs(np.tril(data_cor, k=-1)) > .85
        idx_drop = np.any(idx, axis=1)
        X_train = X_train.loc[:, ~idx_drop]
        X_test = X_test.loc[:, ~idx_drop]
        clf = model.fit(X_train, y_train)
        score[repeat, fold] = clf.score(X_test, y_test)
        fold += 1
        if fold == 10:
            repeat += 1
            fold = 0
    mean_score = np.mean(score, axis=1)
    return np.mean(mean_score)

def ten_ten_cv_lr(i):
    print("original experiment, window: " + str(i))
    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    model = sklearn.linear_model.LogisticRegression(penalty='l1', tol=0.01, solver='saga')
    score = np.zeros((10,10))
    rkf = RepeatedKFold(n_splits=10, n_repeats=10)
    repeat = 0
    fold = 0
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,: ]
        y_train, y_test = y[train_index], y[test_index]
        removeZeros = X_train.apply(lambda x: len(x.unique()) == 1)
        X_train = X_train.loc[:, ~removeZeros]
        X_test = X_test.loc[:, ~removeZeros]
        data_cor = X_train.corr()
        idx = np.abs(np.tril(data_cor, k=-1)) > .85
        idx_drop = np.any(idx, axis=1)
        X_train = X_train.loc[:, ~idx_drop]
        X_test = X_test.loc[:, ~idx_drop]
        clf = model.fit(X_train, y_train)
        score[repeat, fold] = clf.score(X_test, y_test)
        fold += 1
        if fold == 10:
            repeat += 1
            fold = 0
    mean_score = np.mean(score, axis=1)
    return np.mean(mean_score)

def ten_ten_cv_xgb(i):
    print("original experiment, window: " + str(i))
    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    model = GradientBoostingClassifier(n_estimators=100, max_depth=6, learning_rate=0.3)
    score = np.zeros((10,10))
    rkf = RepeatedKFold(n_splits=10, n_repeats=10)
    repeat = 0
    fold = 0
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,: ]
        y_train, y_test = y[train_index], y[test_index]
        removeZeros = X_train.apply(lambda x: len(x.unique()) == 1)
        X_train = X_train.loc[:, ~removeZeros]
        X_test = X_test.loc[:, ~removeZeros]
        data_cor = X_train.corr()
        idx = np.abs(np.tril(data_cor, k=-1)) > .85
        idx_drop = np.any(idx, axis=1)
        X_train = X_train.loc[:, ~idx_drop]
        X_test = X_test.loc[:, ~idx_drop]
        clf = model.fit(X_train, y_train)
        score[repeat, fold] = clf.score(X_test, y_test)
        fold += 1
        if fold == 10:
            repeat += 1
            fold = 0
    mean_score = np.mean(score, axis=1)
    return np.mean(mean_score)

# replicate ten-runs_ten_fold cv in previous work.
def ten_repeated_ten_fold_cv():
    results = np.zeros((15, 4))
    for i in range(15):
        results[i, 0] = ten_ten_cv_lr(i + 1)
        results[i, 1] = ten_ten_cv_rf(i + 1)
        results[i, 2] = ten_ten_cv_svm(i + 1)
        results[i, 3] = ten_ten_cv_xgb(i + 1)

    pd.DataFrame(results).to_csv("across_accracy.csv")



def cv_rf(i):
    print("start testing with less feature")
    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    to_delete = ['fixationsaccadetimeratio', 'longestsaccadedistance', 'longestsaccadeduration', 'maxsaccadespeed', 'meansaccadedistance', 'meansaccadeduration',
                    'meansaccadespeed', 'minsaccadespeed', 'stddevsaccadedistance', 'stddevsaccadeduration', 'stddevsaccadespeed', 'Relevant bars_timetofirstfixation',
                 'Relevant bars_timetolastfixation', 'Non-relevant bars_timetofirstfixation', 'Text_timetofirstfixation', 'Refs_timetofirstfixation', 'labels_timetofirstfixation',
                 'Viz_timetofirstfixation', 'legend_timetofirstfixation']
    X = X.drop(columns=to_delete)
    model = RandomForestClassifier(max_features=16, bootstrap=False)
    score = np.zeros((10,10))
    rkf = RepeatedKFold(n_splits=10, n_repeats=10)
    repeat = 0
    fold = 0
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index,: ]
        y_train, y_test = y[train_index], y[test_index]
        removeZeros = X_train.apply(lambda x: len(x.unique()) == 1)
        X_train = X_train.loc[:, ~removeZeros]
        X_test = X_test.loc[:, ~removeZeros]
        data_cor = X_train.corr()
        idx = np.abs(np.tril(data_cor, k=-1)) > .85
        idx_drop = np.any(idx, axis=1)
        X_train = X_train.loc[:, ~idx_drop]
        X_test = X_test.loc[:, ~idx_drop]
        clf = model.fit(X_train, y_train)
        score[repeat, fold] = clf.score(X_test, y_test)
        fold += 1
        if fold == 10:
            repeat += 1
            fold = 0
    mean_score = np.mean(score, axis=1)
    #print(np.mean(mean_score))
    return np.mean(mean_score)

# equivalent test if exclude some features
def cv_with_less_feature():
    result = np.zeros(15)
    for i in range(15):
        result[i] = cv_rf(i+1)

    print(result)

# compare svm and rf on test data
def compare_test_performance():
    # rf
    selected_data = pd.read_csv("./classification_dataset/training_data.csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    to_delete = ['fixationsaccadetimeratio', 'longestsaccadedistance', 'longestsaccadeduration', 'maxsaccadespeed',
                 'meansaccadedistance', 'meansaccadeduration',
                 'meansaccadespeed', 'minsaccadespeed', 'stddevsaccadedistance', 'stddevsaccadeduration',
                 'stddevsaccadespeed', 'Relevant bars_timetofirstfixation',
                 'Relevant bars_timetolastfixation', 'Non-relevant bars_timetofirstfixation',
                 'Text_timetofirstfixation', 'Refs_timetofirstfixation', 'labels_timetofirstfixation',
                 'Viz_timetofirstfixation', 'legend_timetofirstfixation']
    X = X.drop(columns=to_delete)
    removeZeros = X.apply(lambda x: len(x.unique()) == 1)
    X = X.loc[:, ~removeZeros]
    data_cor = X.corr()
    idx = np.abs(np.tril(data_cor, k=-1)) > .85
    idx_drop = np.any(idx, axis=1)
    X = X.loc[:, ~idx_drop]
    cols = X.columns

    # rf using 1-3 tasks
    rf3 = RandomForestClassifier(n_estimators=200, min_samples_split=2, max_features=16, max_depth=40,bootstrap=False)

    rf3.fit(X, y)


    score = np.zeros((2, 15))
    for i in range(1, 16):
        test_data = pd.read_csv("./classification_dataset/training_data_before_selection_"+ str(i)+".csv", index_col=False)
        X_test = test_data.iloc[:, :-1]
        y_test = test_data.iloc[:, -1]
        X_test = X_test[cols]
        score[0, i-1] = rf3.score(X_test, y_test)


    selected_data = pd.read_csv("./classification_dataset/training_data_before_selection_2.csv",
                                index_col=False)
    # svm only task 1-2
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    X = X.drop(columns=to_delete)
    removeZeros = X.apply(lambda x: len(x.unique()) == 1)
    X = X.loc[:, ~removeZeros]
    data_cor = X.corr()
    idx = np.abs(np.tril(data_cor, k=-1)) > .85
    idx_drop = np.any(idx, axis=1)
    X = X.loc[:, ~idx_drop]
    cols = X.columns
    svm = sklearn.svm.LinearSVC()
    svm.fit(X, y)

    for i in range(1, 16):
        test_data = pd.read_csv(
            "./classification_dataset/training_data_before_selection_" + str(i) + ".csv",
            index_col=False)
        X_test = test_data.iloc[:, :-1]
        y_test = test_data.iloc[:, -1]
        X_test = X_test[cols]
        score[1, i - 1] = svm.score(X_test, y_test)

    pd.DataFrame(score).to_csv("./classification_dataset/compare_svm_rf.csv", index=False)
# we choose random forest as our final classifier model
def final_model_save():
    selected_data = pd.read_csv("./classification_dataset/raining_data.csv", index_col=False)
    X = selected_data.iloc[:, :-1]
    y = selected_data.iloc[:, -1]
    to_delete = ['fixationsaccadetimeratio', 'longestsaccadedistance', 'longestsaccadeduration', 'maxsaccadespeed',
                 'meansaccadedistance', 'meansaccadeduration',
                 'meansaccadespeed', 'minsaccadespeed', 'stddevsaccadedistance', 'stddevsaccadeduration',
                 'stddevsaccadespeed', 'Relevant bars_timetofirstfixation',
                 'Relevant bars_timetolastfixation', 'Non-relevant bars_timetofirstfixation',
                 'Text_timetofirstfixation', 'Refs_timetofirstfixation', 'labels_timetofirstfixation',
                 'Viz_timetofirstfixation', 'legend_timetofirstfixation']
    X = X.drop(columns=to_delete)
    removeZeros = X.apply(lambda x: len(x.unique()) == 1)
    X = X.loc[:, ~removeZeros]
    data_cor = X.corr()
    idx = np.abs(np.tril(data_cor, k=-1)) > .85
    idx_drop = np.any(idx, axis=1)
    X = X.loc[:, ~idx_drop]
    rf3 = RandomForestClassifier(n_estimators=200, min_samples_split=2, max_features=16, max_depth=40, bootstrap=False)
    rf3.fit(X,y)
    joblib.dump(rf3, "./classifier_final.joblib", protocol=2)
    feature_names = list(X.columns.values)
    joblib.dump(feature_names,"./feature_names.joblib", protocol=2)


if __name__ == '__main__':
    final_model_save()