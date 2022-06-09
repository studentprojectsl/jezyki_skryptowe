import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, figure, canvas):
        self.figure = figure
        self.canvas = canvas

    def scatter_data(self, X, Y, title, x_description, y_description):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.scatter(X,Y)
        ax.set_title(title)
        ax.set_xlabel(x_description)
        ax.set_ylabel(y_description)
        # ax.plot(data, '*-')
        return ax

    def plot_data(self, X, Y, ax, description=""):
        ax.plot(X, Y, color='y', label=description)
        ax.legend(loc="upper right")

    def draw_canvas(self):
        self.canvas.draw()

    def plot_2D_with_data(X, Y, X_test, Y_pred, x_description, y_description, font_size=14):
        plt.scatter(X,Y)
        plt.plot(X_test, Y_pred, color='tab:orange')

        plt.xlabel(x_description, fontsize=font_size)
        plt.ylabel(y_description, fontsize=font_size)

    def add_error_bar(X,Y_p, Q):
        plt.errorbar(X,Y_p,Q)

    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()
