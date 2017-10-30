import os
import shutil
import glob
import srt2txt
import update_videos_temp
import remove_space

remove_space.remove_space()
filenames = glob.glob('./temp/*.mp4')

for i in filenames:
	filename = i[:-4]
	srt2txt.convert_srt2txt(filename)
	os.system('ffmpeg -threads 4 -v 0 -y -i '+filename+'.mp4 '+filename+'.mp3')

os.system('mv ./temp/* ./source_temp/')
update_videos_temp.update_videos()
