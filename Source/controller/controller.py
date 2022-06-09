import sys
from controller.config_reader import ConfigReader
sys.path.append('..')
from connector.wbd_connector import Connector
from core.plotter import Plotter
from formatter.data_formatter import *
from core.least_squares import *


class MainController:
    def __init__(self):
        self.database = Connector()
        self.database.load_data()
        self.config_reader = ConfigReader()

    def set_plotter(self,  figure, canvas):
        self.plotter = Plotter(figure, canvas)

    def load_countries_to_config(self):
        countries = self.database.get_countries_names()
        self.config_reader.add_countries(countries)
        self.config_reader.save_config()

    def load_indicators_to_config(self):
        indicators = self.database.get_indicators()
        self.config_reader.add_indicators(indicators)
        self.config_reader.save_config()

    def load_countries_to_gui(self):
        countries_list = self.config_reader.get_countries_from_config()
        countries_list.sort()
        return countries_list

    def load_indicators_to_gui(self):
        indicators_list = self.config_reader.get_indicators_from_config()
        indicators_list = [indicator['value'] for indicator in indicators_list]
        indicators_list.sort()
        return indicators_list

    def load_methods_to_gui(self):
        return self.config_reader.get_methods_from_config()

    def get_id_from_value(self, indicator_name):
        indicators = self.config_reader.get_indicators_from_config()
        for indicator in indicators:
            if indicator['value'] == indicator_name:
                return indicator['id']

    def get_value_from_id(self, id):
        indicators = self.config_reader.get_indicators_from_config()
        for indicator in indicators:
            if indicator['id'] == id:
                return indicator['value']

    def process_query(self, query_data):
        values_x = []
        values_y = []
        ax = None

        if query_data['indicator2'] == "":
            ax, values_x, values_y = self.process_single_query(query_data)
        else:
            ax, values_x, values_y = self.process_double_query(query_data)

        self.plotter.draw_canvas()

    def process_single_query(self, query_data):
        dataframe = self.database.query_for_one_indicator(query_data['indicator1'], query_data['country'])
        dataframe = fill_nan_inside_dataframe(strip_dataframe_nan(dataframe))
        years = convert_years(dataframe.index)
        values = dataframe.values

        ax = self.plotter.scatter_data(years, values, self.get_value_from_id(query_data['indicator1']), "years", "")

        method = query_data['method']
        renumbered_years = renumber_years(years)

        if len(values) > 2 and not check_if_nan_values_exist(values):
            if method == "Least squares":
                self.apply_least_squares(renumbered_years, values, ax, offset=years[0])
            elif "General Linearised Method" in method:
                degree = int(method.split()[-1])
                self.apply_general_linearised_model(degree, renumbered_years, values, ax, offset=years[0])

        return ax, years, values

    def process_double_query(self, query_data):
        dataframe1, dataframe2 = self.database.query_for_two_indicators(query_data['indicator1'],
                                                                        query_data['indicator2'], query_data['country'])

        dataframe1 = fill_nan_inside_dataframe(strip_dataframe_nan(dataframe1))
        dataframe2 = fill_nan_inside_dataframe(strip_dataframe_nan(dataframe2))


        dataframe1, dataframe2 = strip_and_fit_dataframes(dataframe1, dataframe2)

        values_x = dataframe1.values
        values_y = dataframe2.values

        ax = self.plotter.scatter_data(values_x, values_y, "Comparison", self.get_value_from_id(query_data['indicator1'])
                                       , self.get_value_from_id(query_data['indicator2']))

        method = query_data['method']

        if len(values_x) > 2 and not check_if_nan_values_exist(values_x):
            if method == "Least squares":
                self.apply_least_squares(values_x, values_y, ax, offset=0)
            elif "General Linearised Method" in method:
                degree = int(method.split()[-1])
                self.apply_general_linearised_model(degree, values_x, values_y, ax, offset=0)

        return ax, values_x, values_y


    def apply_least_squares(self, values_x, values_y, ax, offset=0):
        X, Y, description = least_squares_2D_model(values_x, values_y)
        description = description.replace("x", f"(x-{int(offset)})")
        self.plotter.plot_data(X+offset, Y, ax, description)

    def apply_general_linearised_model(self, degree, values_x, values_y, ax, offset=0):
        X, Y, description = generalized_linear_model(values_x, values_y, degree)
        description = description.replace("x", f"(x-{int(offset)})")
        self.plotter.plot_data(X+offset, Y, ax, description)

    def clear_canvas(self):
        self.plotter.clear_canvas()






