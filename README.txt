World Bank Data Analyzer app
Author: Mateusz Smigielski

This app is accessible only by GUI nowadays.

SETUP
1.Go to your project directory
2.Copy Source directory and requirements.txt into that directory
3. python -m venv env
4. env\Scripts\activate.bat activate (environment directory name should be 'env')
5. python -m pip install -r requirements.txt

RUN
1. Go to Source directory
2. Run python main.py

There can be some problems with PyQT5 plugins
Try adding  env/site-packages/PyQt5/Qt5/plugins to PATHS as QT_PLUGIN_PATH