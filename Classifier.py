import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from keras.models import Sequential
import tensorflow as tf
from keras.layers.core import Dense
from tensorflow.keras.utils import to_categorical



class Classifier:

    def __init__(self, model):
        self.model = model
        self.trained = False

    def fit(self, x_train, y_train):
        if isinstance(x_train, pd.DataFrame):
            self.model.fit(x_train.values, y_train)
        else :
            self.model.fit(x_train, y_train)
        self.trained = True

    def is_trained(self):
        return self.trained

    def predict_class(self, x_test):
        """
        Method to compute predict of a classifier
        :return: array of predicted class
        """
        return self.model.predict(x_test)

    def predict_prob(self, x_test):
        """
        Method to compute probabilities of predicted classes
        :return: array of probabilities for each classes
        """
        return self.model.predict_proba(x_test)

    def predict_confidence(self, x_test):
        """
        Method to compute confidence in the predicted class
        :return: -1 as default, value if algorithm is from framework PYOD
        """
        return -1

    def classifier_name(self):
        """
        Returns the name of the classifier (as string)
        """
        pass


class XGB(Classifier):

    def __init__(self, n_trees=None):
        if n_trees is None:
            Classifier.__init__(self, XGBClassifier(use_label_encoder=False))
        else:
            Classifier.__init__(self, XGBClassifier(n_estimators=n_trees, use_label_encoder=False))

    def classifier_name(self):
        return "XGBoost"


class DecisionTree(Classifier):

    def __init__(self, depth):
        Classifier.__init__(self, DecisionTreeClassifier(max_depth=depth))
        self.depth = depth

    def classifier_name(self):
        return "DecisionTree(depth=" + str(self.depth) + ")"


class KNeighbors(Classifier):

    def __init__(self, k):
        Classifier.__init__(self, KNeighborsClassifier(n_neighbors=k, n_jobs=-1, algorithm="kd_tree"))
        self.k = k

    def classifier_name(self):
        return str(self.k) + "NearestNeighbors"


class LDA(Classifier):

    def __init__(self):
        Classifier.__init__(self, LinearDiscriminantAnalysis())

    def classifier_name(self):
        return "LDA"


class LogisticReg(Classifier):

    def __init__(self):
        Classifier.__init__(self, LogisticRegression(solver='sag',
                                                     random_state=0,
                                                     multi_class='ovr',
                                                     max_iter=10000,
                                                     n_jobs=10,
                                                     tol=0.1))

    def classifier_name(self):
        return "LogisticRegression"


class Bayes(Classifier):

    def __init__(self):
        Classifier.__init__(self, GaussianNB())

    def classifier_name(self):
        return "NaiveBayes"


class RandomForest(Classifier):

    def __init__(self, trees):
        Classifier.__init__(self, RandomForestClassifier(n_estimators=trees))
        self.trees = trees

    def classifier_name(self):
        return "RandomForest(trees=" + str(self.trees) + ")"


class SupportVectorMachine(Classifier):

    def __init__(self, kernel, degree):
        Classifier.__init__(self, SVC(kernel=kernel, degree=degree, probability=True, max_iter=10000))
        self.kernel = kernel
        self.degree = degree

    def classifier_name(self):
        return "SupportVectorMachine(kernel=" + str(self.kernel) + ")"


class NeuralNetwork(Classifier):

    def __init__(self, num_input, num_classes):
        self.model = Sequential()
        self.model.add(Dense(num_input, input_shape=(num_input,), activation='relu'))
        self.model.add(Dense(num_input * 10, activation='relu'))
        self.model.add(Dense(num_input * 10, activation='relu'))
        self.model.add(Dense(num_classes, activation='softmax'))

    def fit(self, x_train, y_train):
        self.model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(x_train, to_categorical(y_train), batch_size=64, epochs=10, verbose=0)
        self.model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])

    def predict_class(self, x_test):
        array_proba = np.asarray(self.model.predict(x_test))
        predictions = np.zeros((len(array_proba),), dtype=int)
        for i in range(len(array_proba)):
            predictions[i] = np.argmax(array_proba[i], axis=0)
        return predictions

    def predict_prob(self, X_test):
        return np.asarray(self.model.predict(X_test))

    def classifier_name(self):
        return "NeuralNetwork"
