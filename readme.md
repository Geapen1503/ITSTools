How to build :

- make sure pyinstaller is installed by running `pip install pyinstaller`
- if there is no dist directory, or no build directory / main.spec file, run `pyinstaller --onefile main.py`
- make sur you include your img / data folders in the "datas" of main.spec file
- if these instructions are done, run `pyinstaller main.spec` and it will build the exe file in the dist directory

Modifying the app :

- it's a small python app, only one file (main.py), so if you want to modify/add anything, just read the code

