import os
import glob

filenames = glob.glob('./*.txt')

print filenames

for i in filenames:
	print i	
	os.system('ffmpeg -f concat -safe 0 -i '+i+' -c copy '+i[:-3]+'.mp4')
