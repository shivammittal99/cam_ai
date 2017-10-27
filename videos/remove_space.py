import os
import glob
import shutil

filenames = glob.glob('./temp/*')
for i in filenames:
	count = 0
	new_filename = i[:]
	for j in range(len(i)):
		if i[j] >= 'A' and i[j] <= 'Z':
			continue
		elif i[j] >= 'a' and i[j] <= 'z':
			continue
		elif i[j] >= '0' and i[j] <= '9':
			continue
		elif i[j] == '.' or i[j] == '/':
			continue
		else:
			new_filename = new_filename[:j-count] + new_filename[j+1-count:]
			count += 1
	new_filename = new_filename.replace('_', '')
	print i, " ==> ", new_filename
	shutil.move(i, new_filename)
