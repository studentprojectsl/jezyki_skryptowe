import sys
import os
os.environ['QT_PLUGIN_PATH'] = '../env/Lib/site-packages/PyQt5/Qt5/plugins'
from controller.controller import MainController
from view.graphic_interface import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    Controller = MainController()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow(Controller)
    window.show()
    sys.exit(app.exec_())










