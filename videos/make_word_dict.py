import json
import pickle as pkl
import glob
import os
import ffmpeg_split

def align_time(filename):
	temp = filename.split('/')[-1]
	os.system('python gentle/align.py '+filename+'.mp4 '+filename+'.txt -o ./source_temp/align_'+temp+'.json')

def create_manifest(filename, words_dict):
	filename = filename.split('/')[-1]
	f = open('./source_temp/align_'+filename+'.json', 'r')
	data = json.load(f)

	cnt = 0

	for i in data['words']:
	 	if(i['case'] == 'success'):
			start = i['start']
			end = i['end']
			duration = end-start
			word = i['word'].lower()
			name = 'videos1/video_'+filename+'_'+str(cnt)+'.mp4'
			words_dict[word] = words_dict.get(word, [])
			words_dict[word].append((duration, name))
			cnt += 1

def update_videos():
    words_dict = {}
    try:
        file_dict_fileobj = open('file_dict_temp1.pkl', 'rb')
        file_dict = pkl.load(file_dict_fileobj)
        file_dict_fileobj.close()
    except:
        file_dict = {}

    try:
        dict_file = open('words_dict_temp1.pkl', 'rb')
        words_dict = pkl.load(dict_file)
        dict_file.close()
    except:
        words_dict = {}

    filenames = glob.glob('./source_temp/*.mp4')

    for i in filenames:
        print i
        if not file_dict.get(i, False):
            file_dict[i] = True
        	align_time(i[:-4])
            create_manifest(i[:-4], words_dict)

        file_dict_fileobj = open('file_dict_temp1.pkl', 'wb')
        pkl.dump(file_dict, file_dict_fileobj)
        file_dict_fileobj.close()


        dict_file = open('words_dict_temp1.pkl', 'wb')
        pkl.dump(words_dict, dict_file)
        dict_file.close()

update_videos()
