import PySimpleGUI as sg
import csv
import time
import pandas as pd
import os
import webbrowser

filename = sg.popup_get_file('Enter the file you wish to process')
#filename = str(r'C:\Users\Clinton\Downloads\DecisionEngineOutputs_combined.csv')

output_dir = os.path.splitext(filename)[0].replace(" ","_") + "_split_by_capex"
print(output_dir)

file_base_name = os.path.splitext(os.path.basename(filename))[0].replace(" ","_")
print(file_base_name)

os.mkdir(output_dir)

data = pd.read_csv(filename)
capex_column_name=data.columns[0]

data[capex_column_name] = data[capex_column_name].astype('int64')

data_capex_range = data[capex_column_name].unique()
data_capex_range = data_capex_range.tolist()

for i,value in enumerate(data_capex_range):
    sg.OneLineProgressMeter('One Line Meter Example', i + 1, len(data_capex_range), 'key')
    data[data[capex_column_name] == value].to_csv(os.path.join(output_dir, file_base_name + '_' + str(int(value)) + '.csv'),index = False)

sg.popup('Successfully processed. Files located at ', output_dir)

webbrowser.open(output_dir)
