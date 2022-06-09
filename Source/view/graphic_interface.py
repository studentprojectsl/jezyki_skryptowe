import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget, QMainWindow, QToolBar, \
    QStatusBar, QGridLayout, QHBoxLayout, QSplitter, QSizePolicy, QMessageBox, QInputDialog
from PyQt5 import QtGui
import PyQt5.QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------
# add  ../../venv/site-packages/PyQt5/Qt5/plugins to PATHS as QT_PLUGIN_PATH
# ------------------------------------------------------------------------
_app_name = "World Bank Data Analyzer"


class MainWindow(QMainWindow):

    def __init__(self, controller):
        super(MainWindow, self).__init__()

        self.controller = controller
        # --------Basic settings----------------------
        self.setWindowTitle(_app_name)
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QtGui.QIcon('images/logo.svg'))
        # ---------------------------------------------

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.generalLayout = QGridLayout()

        self.dashboard_left = QVBoxLayout()
        self.monitor = QGridLayout()
        self.dashboard_down = QSplitter()

        self.set_layout()

        self.generalLayout.addLayout(self.monitor, 0, 1, 6, 5)
        self.generalLayout.addLayout(self.dashboard_left, 0, 0, 6, 1)
        self.generalLayout.addWidget(self.dashboard_down, 6, 0, 2, 6)
        self.generalLayout.setColumnStretch(0, 1)
        self.generalLayout.setColumnStretch(1, 1)
        self.generalLayout.setColumnStretch(2, 1)
        self.generalLayout.setColumnStretch(3, 1)
        self.generalLayout.setColumnStretch(4, 1)
        self.generalLayout.setColumnStretch(5, 1)
        self._centralWidget.setLayout(self.generalLayout)

    def set_layout(self):
        self.create_menu()
        self.createToolBar()
        self.createStatusBar()
        self.set_dashboard_left()
        self.set_monitor()
        self.set_dashboard_down()

    def create_menu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)
        tools.addAction('Clear monitor', self.clear_canvas)

    def createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Ready to use")
        self.setStatusBar(status)
        self.status_bar = status

    def set_loading_status_bar(self):
        self.status_bar.showMessage("Loading...")

    def unset_loading_status_bar(self):
        self.status_bar.showMessage("")

    def set_dashboard_down(self):
        self.set_indicators_list()
        self.set_countries_list()
        self.set_method_list()

    def set_monitor(self):
        self.set_canvas()

    def set_dashboard_left(self):
        countries_box = QWidget()
        countries_box_layout = QVBoxLayout()
        countries_box.setLayout(countries_box_layout)
        countries_label = QLabel("Selected country")
        countries_box.setStyleSheet('background-color: white;')
        country_choice = QLabel("")
        self.country_choice = country_choice
        countries_box_layout.addWidget(countries_label)
        countries_box_layout.addWidget(country_choice)
        countries_choice_clear_button = QPushButton("Clear")
        countries_choice_clear_button.clicked.connect(self.clear_countries_choice)
        countries_box_layout.addWidget(countries_choice_clear_button)

        indicators_box = QWidget()
        indicators_box_layout = QVBoxLayout()
        indicators_box.setLayout(indicators_box_layout)
        indicators_label = QLabel("Selected indicators")
        indicators_box.setStyleSheet('background-color: white')
        indicator_1_choice = QLabel("")
        indicator_1_choice.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        indicator_2_choice = QLabel("")
        self.indicators_choice = []
        self.indicators_choice.append(indicator_1_choice)
        self.indicators_choice.append(indicator_2_choice)
        indicators_box_layout.addWidget(indicators_label)
        indicators_box_layout.addWidget(indicator_1_choice)
        indicators_box_layout.addWidget(indicator_2_choice)
        indicators_choice_clear_button = QPushButton("Clear")
        indicators_choice_clear_button.clicked.connect(self.clear_indicators_choice)
        indicators_box_layout.addWidget(indicators_choice_clear_button)

        method_box = QWidget()
        method_box_layout = QVBoxLayout()
        method_box.setLayout(method_box_layout)
        method_label = QLabel("Selected method")
        method_box.setStyleSheet('background-color: white')
        method_choice = QLabel("")
        self.method_choice = method_choice
        method_box_layout.addWidget(method_label)
        method_box_layout.addWidget(method_choice)
        method_choice_clear_button = QPushButton("Clear")
        method_choice_clear_button.clicked.connect(self.clear_method_choice)
        method_box_layout.addWidget(method_choice_clear_button)

        self.dashboard_left.addWidget(countries_box)
        self.dashboard_left.addWidget(indicators_box)
        self.dashboard_left.addWidget(method_box)

        query_button = QPushButton("Plot")
        query_button.clicked.connect(self.send_query)
        self.dashboard_left.addWidget(query_button)

    def clear_countries_choice(self):
        self.country_choice.setText("")

    def clear_indicators_choice(self):
        self.indicators_choice[0].setText("")
        self.indicators_choice[1].setText("")

    def clear_method_choice(self):
        self.method_choice.setText("")

    def set_canvas(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.monitor.addWidget(self.canvas, 0, 0, 1, 1)
        self.controller.set_plotter(self.figure, self.canvas)

    def set_countries_list(self):
        layout = QVBoxLayout()
        package = QWidget()
        package.setLayout(layout)

        countries_list = QListWidget()
        title = QLabel("Countries")

        countries = self.controller.load_countries_to_gui()
        for country in countries:
            countries_list.addItem(str(country))

        countries_list.clicked.connect(self.select_country)
        layout.addWidget(title)
        layout.addWidget(countries_list)

        self.countries_list = countries_list
        self.dashboard_down.addWidget(package)

    def set_indicators_list(self):
        layout = QVBoxLayout()
        package = QWidget()
        package.setLayout(layout)

        indicators_list = QListWidget()
        title = QLabel("Indicators")

        indicators = self.controller.load_indicators_to_gui()
        for indicator in indicators:
            indicators_list.addItem(str(indicator))

        indicators_list.clicked.connect(self.select_indicator)
        layout.addWidget(title)
        layout.addWidget(indicators_list)

        self.indicators_list = indicators_list
        self.selected_indicators = 0
        self.dashboard_down.addWidget(package)

    def set_method_list(self):
        layout = QVBoxLayout()
        package = QWidget()
        package.setLayout(layout)

        methods_list = QListWidget()
        title = QLabel("Methods")

        methods = self.controller.load_methods_to_gui()
        for method in methods:
            methods_list.addItem(str(method))

        methods_list.clicked.connect(self.select_method)
        layout.addWidget(title)
        layout.addWidget(methods_list)

        self.methods_list = methods_list
        self.dashboard_down.addWidget(package)

    def select_country(self):
        item = self.countries_list.currentItem()
        self.country_choice.setText(item.text())


    def select_indicator(self):
        indicator_choice_slot = None
        if self.indicators_choice[0].text() == "":
            indicator_choice_slot = 0
        elif self.indicators_choice[1].text() == "":
            indicator_choice_slot = 1

        if indicator_choice_slot is not None:
            item = self.indicators_list.currentItem()
            item_text = item.text()
            indicator_id = self.controller.get_id_from_value(item_text)
            self.indicators_choice[indicator_choice_slot].setText(indicator_id)

    def select_method(self):
        item = self.methods_list.currentItem()

        if item.text() == "General Linearised Method":
            number, status = QInputDialog.getInt(self, "Input", "Enter polynomial degree:")

            while not status or not (0 < number <= 5):
                number, status = QInputDialog.getInt(self, "Input", "Enter polynomial degree:")

            self.method_choice.setText(f"{item.text()}\ndegree: {number}")
            return

        self.method_choice.setText(item.text())

    def clear_canvas(self):
        self.controller.clear_canvas()

    def send_query(self):
        country = self.country_choice.text()
        indicator_1_choice = self.indicators_choice[0].text()
        indicator_2_choice = self.indicators_choice[1].text()
        method = self.method_choice.text()

        if country == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Country must be selected.")
            msg.setWindowTitle("Incorrect query")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            return

        if indicator_1_choice == "" and indicator_2_choice == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("At least one indicator must be selected.")
            msg.setWindowTitle("Incorrect query")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            return

        if method == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Method must be selected.")
            msg.setWindowTitle("Incorrect query")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            return

        query_data = {
            "country": country,
            "indicator1": indicator_1_choice,
            "indicator2": indicator_2_choice,
            "method": method
        }

        self.set_loading_status_bar()
        self.controller.process_query(query_data)
        self.unset_loading_status_bar()
