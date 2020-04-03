import os
import math 
from tabulate import tabulate

def avg(lst): # returns the average of a list
    return sum(lst) / len(lst) 
   
def print_cool(lst, name): # print the list like a tabular row
	print 						name + '\t' + \
		str(lst[0]).replace('.',',') + '\t' + \
		str(lst[1]).replace('.',',') + '\t' + \
		str(lst[2]).replace('.',',') + '\t' + \
		str(lst[3]).replace('.',',') + '\t' + \
		str(round(avg(lst),3)).replace('.',',')

# check if there are all the test files
def check_if_all_files(files):
	if len(files) < 44: # 4 runs for each of the 11 test
		return False
	return True
		
		
		
# initialize the lists
specificity = [0,0,0,0]
recall = [0,0,0,0]
precision = [0,0,0,0]
f_measure = [0,0,0,0]
g_mean = [0,0,0,0]

# index used to knowing in which of the 4 files we are working on 
i = 0

folder = "raw_data_ReliefF"

files = os.listdir(folder)

if not check_if_all_files(files):
	exit("Exit: not enough files in folder. There are missing tests.")

files.sort()

for file_name in files: 
	# print file_name
	
	with open(folder + '/' + file_name) as f:
		
		''' line example
		=== Detailed Accuracy By Class ===

			         TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
			         0,997    0,815    0,933      0,997    0,964      0,379    0,932     0,991     Other
			         0,185    0,003    0,852      0,185    0,305      0,379    0,932     0,613     Uterus
		'''

		line = f.readline()
		while '=== Detailed Accuracy By Class ===' not in line: # find this line
			line = f.readline()

		# go to the first line with numbers
		line = f.readline()
		line = f.readline()
		line = f.readline()
		specificity[i] = float(line.split()[3].replace(',','.'))
	
		line = f.readline()
		recall[i]    = float(line.split()[3].replace(',','.'))
		precision[i] = float(line.split()[2].replace(',','.'))
		f_measure[i] = float(line.split()[4].replace(',','.'))
		g_mean[i] 	 = round (math.sqrt(specificity[i] * recall[i]), 3)
	

	if i == 3: # print the summary
		print (file_name[0:2] + ') ' + file_name[3:-6].replace('_',' + '))

		print '\t' + '#' + '\t' + ' 1' + '\t' + ' 2' + '\t' + ' 3' + '\t' + ' 4' + '\t' + 'Average'
		print_cool(specificity, 'Specificity')
		print_cool(recall, 		'Recall     ')
		print_cool(precision, 	'Precision  ')
		print_cool(f_measure, 	'F-measure  ')
		print_cool(g_mean, 		'G-mean     ')
		
		print("\n\n")

	i = (i + 1) % 4 
	

	





	
