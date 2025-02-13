How to build :

- make sure pyinstaller is installed by running `pip install pyinstaller`
- if there is no dist directory, or no build directory / main.spec file, run `pyinstaller --onefile main.py`
- make sur you include your img / data folders in the "datas" of main.spec file
- if these instructions are done, run `pyinstaller main.spec` and it will build the exe file in the dist directory

Modifying the app :

- it's a small python app, only one file (main.py), so if you want to modify/add anything, just read the code
- if you only want to add commands add them to the commands list in the ShellApp class, respect the typo, like this:
  ("command name", "your powershell command")

secure build command : pyinstaller --onefile --noconsole --icon=./img/ico.ico --clean main.py 

signing exe command :
SignTool sign /f "C:\Users\Theo\Desktop\certs\certs\bill01.pfx" /p "orange" /fd SHA256 /t "http://timestamp.comodoca.com/authenticode" "C:\Users\Theo\PycharmProjects\ITSTools\dist\main.exe"