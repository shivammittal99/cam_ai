import json
import pickle as pkl
import glob
import os
import ffmpeg_split

def align_time(filename):
    temp = filename.split('/')[-1]
    os.system('python gentle/align.py '+filename+'.mp4 '+filename+'.txt -o ./source_temp/align_'+temp+'.json')

def create_manifest(filename, words_dict):
    f = open(filename, 'r')
    filename = filename[20:-5]
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
    #try:
    #    file_dict_fileobj = open('file_dict_temp1.pkl', 'rb')
    #    file_dict = pkl.load(file_dict_fileobj)
    #    file_dict_fileobj.close()
    #except:
    #    file_dict = {}

    filenames = glob.glob('./source_temp/align_*.json')
    #filenames = pkl.load(open('file_dict_temp.pkl', 'rb')).keys()
    #print ("hello", filenames, len(filenames))
    cnt = 1
    for i in filenames:
    	print i, cnt
	cnt += 1
    	create_manifest(i, words_dict)

    #file_dict_fileobj = open('file_dict_temp1.pkl', 'wb')
    #pkl.dump(file_dict, file_dict_fileobj)
    #file_dict_fileobj.close()

    dict_file = open('words_dict_temp2.pkl', 'wb')
    pkl.dump(words_dict, dict_file)
    dict_file.close()

update_videos()
