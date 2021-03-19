## What is it?

**simple_de_splitter** is a Python package that provides fast and flexible way to split large decision engine files. Already packaged as an executable binary file for both Mac and Windows for easy distribution, especially for non technical people.

Package is build on **pandas** and **pysimplegui**, thus we can add more features related to pandas, especially since most of our data scientists use jupyter and pandas.

Tested on Python 3.9.2 but should work on python 3.7 - 3.9

Compatible OS:
  - Mac: Mojave (would need someone with Catalina to test and probably build Catalina version)
  - Windows: Windows 10

## Main Features
Here are just a few of the things that simple_de_splitter does:

  - Split by capex
  - Split by solution and capex
  - Custom split
  	- Select one capex and one solution

The program creates a directory where the original DE file resides at and opens finder/explorer window after processing to immediately show you where the files are.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/clintonbuzon-dsanalytics/simple_de_splitter

Main code is on one python file: `simple_de_splitter.py` and then built as an executable binary package using pyinstaller

## Dependencies
Before building executable file using pyinstaller, we need to install a few python packages on our machine, ideally within a virtual environment

```sh
pip install pysimplegui
pip install pandas
pip install pyinstaller
```



## Build instructions

To build packages using pyinstaller, we need both Mac and windows machine to do the build.

### Mac
On a mac machine, after installing all dependencies, we execute the following code
```python
pyinstaller --onefile --hidden-import=cmath --windowed --icon=simple_de_splitter.icns simple_de_splitter.py
```
This should create an app file under dist folder

### Windows
On a windows machine, after installing all dependencies, we execute the following code
```python
pyinstaller -wF --icon=simple_de_splitter.ico simple_de_splitter.py
```

## Getting Help

For usage questions, you may contact me at johnclinton.buzon@dsanalytics.com

