import pandas
import pandas as pd
import numpy
import math

def strip_dataframe_nan(dataframe):
    first_idx = dataframe.first_valid_index()
    last_idx = dataframe.last_valid_index()

    if first_idx is None or last_idx is None:
        return dataframe

    return dataframe.loc[first_idx:last_idx]


def get_dataframe_valid_indexes(dataframe):
    first_index = dataframe.first_valid_index()
    last_index = dataframe.last_valid_index()

    first_index = first_index if first_index else dataframe.index[0]
    last_index = last_index if last_index else dataframe.index[-1]

    return first_index, last_index


def fill_nan_inside_dataframe(dataframe):
    return dataframe.fillna(dataframe.mean(axis=0))


def strip_and_fit_dataframes(dataframe_a, dataframe_b):
    first_a_index, last_a_index = get_dataframe_valid_indexes(dataframe_a)
    first_b_index, last_b_index = get_dataframe_valid_indexes(dataframe_b)

    first_index = first_b_index if first_a_index < first_b_index else first_a_index
    last_index = last_b_index if last_b_index < last_a_index else last_a_index

    dataframe_a = dataframe_a.loc[first_index:last_index]
    dataframe_b = dataframe_b.loc[first_index:last_index]

    dataframe_a = fill_nan_inside_dataframe(dataframe_a)
    dataframe_b = fill_nan_inside_dataframe(dataframe_b)

    # for debug purposes
    # print(first_a_index, last_a_index)
    # print(first_b_index, last_b_index)
    # print(first_index, last_index)

    return dataframe_a, dataframe_b


def create_dataframe(dataframe_a, dataframe_b, column_a, column_b):
    dataframe_a, dataframe_b = strip_and_fit_dataframes(dataframe_a, dataframe_b)

    list_of_series = [dataframe_a, dataframe_b]
    list_of_columns = [column_a, column_b]

    dataframe = pd.DataFrame(list_of_series, list_of_columns)

    return dataframe


def convert_years(years_list):
    return numpy.array([float(year[2:]) for year in years_list])


def renumber_years(years):
    number_of_years = len(years)
    return numpy.array([number for number in range(number_of_years)])

def check_if_nan_values_exist(values):
    for value in values:
        if math.isnan(value):
            return True
    return False
