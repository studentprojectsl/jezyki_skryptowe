import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

number_of_steps = 300

def least_squares_2D_model(X, Y):
    def model(parameters, x):
        a, b = parameters
        return a * x + b

    a_estimated = (len(X) * np.sum(X * Y) - (np.sum(X) * np.sum(Y))) / (len(X) * np.sum(X ** 2) - (np.sum(X)) ** 2)
    b_estimated = (np.sum(Y) * np.sum(X ** 2) - (np.sum(X) * np.sum(Y * X))) / (len(X) * np.sum(X ** 2) - (np.sum(X)) ** 2)

    X_test = np.linspace(start=X.min(), stop=X.max(), num=number_of_steps)
    Y_pred = model(parameters=[a_estimated, b_estimated], x=X_test)

    function_str = f"y = {a_estimated}x + {b_estimated}"

    return X_test, Y_pred, function_str


def generalized_linear_model(X, Y, degree):
    degree_matrix = generate_degree_matrix(degree)
    _X = X[np.newaxis, :] ** degree_matrix
    _Y = Y[np.newaxis, :]

    _T = np.linalg.inv(_X @ _X.transpose()) @ _X @ _Y.transpose()

    X_test = np.linspace(start=X.min(), stop=X.max(), num=300)
    Y_pred = np.zeros_like(X_test)

    function_str = "y = "

    for i, c in enumerate(_T.ravel()[::-1]):
        Y_pred += (X_test ** i) * c
        function_str += f"{round(c, 6)}x^{i} + "

    function_str = function_str[:-2]
    return X_test, Y_pred, function_str


def generate_degree_matrix(degree):
    return [[number] for number in range(degree, -1, -1)]


