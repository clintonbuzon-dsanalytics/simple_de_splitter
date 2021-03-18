import PySimpleGUI as sg
import csv
import time
import pandas as pd
import os
import platform
from subprocess import call
import traceback

def de_splitter():
	filename = sg.popup_get_file('Enter the file you wish to process')
	#filename = str(r'C:\Users\Clinton\Downloads\DecisionEngineOutputs_combined.csv')
	#filename = str(r'/Users/clintonbuzon/RDP/test folder/DecisionEngineOutputs_combined_ioc_optimiser.csv')

	base_dir = os.path.dirname(filename)
	file_base_name = os.path.splitext(os.path.basename(filename))[0].replace(" ","_")
	output_dir = os.path.join(base_dir,file_base_name + "_split_by_capex")
	
	print(base_dir)	
	print(file_base_name)
	print(output_dir)

	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	data = pd.read_csv(filename)
	sg.popup_animated(None) 

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

	def open_file(path):
	    if platform.system() == "Windows":
	        os.startfile(path)
	    elif platform.system() == "Darwin":
	        call(["open", path])
	    else:
	        subprocess.Popen(["xdg-open", path])

	# call(["open", output_dir])
	open_file(output_dir)

def main():
	try:
		de_splitter()
	except Exception as e:
		tb = traceback.format_exc()
		sg.Print(f'An error happened.  Here is the info:', e, tb)
		sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

if __name__ == "__main__":
    main()