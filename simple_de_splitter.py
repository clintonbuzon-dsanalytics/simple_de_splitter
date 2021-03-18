import PySimpleGUI as sg
import csv
import time
import pandas as pd
import os
import platform
from subprocess import call
import traceback

def open_path(path):
	    if platform.system() == "Windows":
	        os.startfile(path)
	    elif platform.system() == "Darwin":
	        call(["open", path])
	    else:
	        subprocess.Popen(["xdg-open", path])

def read_pandas_csv(filename):
	layout = [[sg.Text('Reading DE file. Please wait for a few seconds.', size=(40, 1), font=("Helvetica", 12))]]
	window = sg.Window('Reading file', layout)
	event, values = window.read(timeout=100)
	window.refresh()

	iteration_count = 0
	with open(filename) as f:
		line_count = 0
		for line in f:
			line_count += 1

	if line_count < 1000000:
		iteration_count = 1
	else:
		iteration_count=int(line_count/1000000)+1

	data = pd.DataFrame()
	reader = pd.read_csv(filename, chunksize=1000000, low_memory=False)
	i=0
	for chunk in reader:
		sg.OneLineProgressMeter('Reading DE file...' , i + 1, iteration_count, 'key')
		data = pd.concat([data,chunk])
		i+=1

	window.close()
	return data

def de_splitter_by_solution_capex(filename,base_dir,file_base_name,output_dir,data):
		
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	data.columns = map(str.upper, data.columns)

	data['CAPEX'] = data['CAPEX'].astype('int64')

	data_capex_range = data['CAPEX'].unique()
	data_capex_range = data_capex_range.tolist()

	data_solution_range = data['SOLUTION'].unique()
	data_solution_range = data_solution_range.tolist()


	for x,solution in enumerate(data_solution_range):
		solution_dir=os.path.join(output_dir,'solution_' + str(solution))
		
		if not os.path.exists(solution_dir):
			os.mkdir(solution_dir)

		for i,value in enumerate(data_capex_range):
		    sg.OneLineProgressMeter('Processing for solution: ' + str(solution), i + 1, len(data_capex_range), 'key')
		    data[(data['CAPEX'] == value) & (data['SOLUTION'] == solution)].to_csv(os.path.join(solution_dir, file_base_name + '_solution' + str(int(solution)) + '_' + str(int(value)) + '.csv'),index = False)

	sg.popup('Successfully processed. Files located at ', output_dir)
	open_path(output_dir)

def de_splitter_by_capex_only(filename,base_dir,file_base_name,output_dir,data):
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	data.columns = map(str.upper, data.columns)

	data['CAPEX'] = data['CAPEX'].astype('int64')

	data_capex_range = data['CAPEX'].unique()
	data_capex_range = data_capex_range.tolist()

	for i,value in enumerate(data_capex_range):
	    sg.OneLineProgressMeter('Processing...', i + 1, len(data_capex_range), 'key')
	    data[(data['CAPEX'] == value)].to_csv(os.path.join(output_dir, file_base_name + '_' + str(int(value)) + '.csv'),index = False)

	sg.popup('Successfully processed. Files located at ', output_dir)
	open_path(output_dir)


def de_splitter_custom(filename,base_dir,file_base_name,output_dir,data):
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	# data = pd.read_csv(filename)
	data.columns = map(str.upper, data.columns)
	data['CAPEX'] = data['CAPEX'].astype('int64')
	data_capex_range = data['CAPEX'].unique().tolist()
	data_solution_range = data['SOLUTION'].unique().tolist()

	data_capex_range.sort()
	data_solution_range.sort()

	data_capex_range_formatted = []
	for capex in data_capex_range:
		data_capex_range_formatted.append("{:,}".format(capex))

	layout = [	[sg.Text('Please select options below')],
				[sg.Text('Choose Capex:', size=(20, 1)),sg.Combo(values=data_capex_range_formatted, size=(20, 1))],
				[sg.Text('Choose Solution:', size=(20, 1)),sg.Combo(values=data_solution_range, size=(20, 1))],
            	[sg.Button('Ok')]]

	window = sg.Window('Custom splitter', layout, font=("Helvetica", 12))
	event, values = window.read()
	
	capex_val = int(str(values[0]).replace(",",""))
	sol_val = values[1]

	data[(data['CAPEX'] == capex_val) & (data['SOLUTION'] == sol_val)].to_csv(os.path.join(output_dir, file_base_name + '_solution' + str(int(sol_val)) + '_' + str(int(capex_val)) + '.csv'),index = False)
	sg.popup('Successfully processed. Files located at ', output_dir)
	open_path(output_dir)

def main():
	try:
		filename = sg.popup_get_file('Enter the file you wish to process', font=("Helvetica", 12))

		data = read_pandas_csv(filename)

		base_dir = os.path.dirname(filename)
		file_base_name = os.path.splitext(os.path.basename(filename))[0].replace(" ","_")

		layout = [[sg.Button('Split by capex',key='_SCAP_'),sg.Button('Split by solution + capex',key='_SSOLCAP_'), sg.Button('Custom split',key='_CS_'), sg.Cancel()]]

		window = sg.Window('Please select type of DE split', layout, font=("Helvetica", 12))

		while True:
		    event, values = window.read()
		    if event in (sg.WIN_CLOSED, 'Cancel'):
		        break
		        window.close()
		    elif event == '_SCAP_':
		    	output_dir = os.path.join(base_dir,file_base_name + "_split_by_capex")
		    	window.close()
		    	de_splitter_by_capex_only(filename,base_dir,file_base_name,output_dir,data)
		    elif event == '_SSOLCAP_':
		    	output_dir = os.path.join(base_dir,file_base_name + "_split_by_sol_capex")
		    	window.close()
		    	de_splitter_by_solution_capex(filename,base_dir,file_base_name,output_dir,data)
		    elif event == '_CS_':
		    	output_dir = os.path.join(base_dir,file_base_name + "_split_custom")
		    	window.close()
		    	de_splitter_custom(filename,base_dir,file_base_name,output_dir,data)
		window.close()
	except Exception as e:
		tb = traceback.format_exc()
		sg.Print(f'An error happened.  Here is the info:', e, tb)
		sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

if __name__ == "__main__":
    main()