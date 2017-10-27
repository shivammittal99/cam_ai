import json
import pickle as pkl
import glob
import os
import ffmpeg_split
words_dict = {}
def align_time(filename):
    os.system('python gentle/align.py '+filename+'.mp4 '+filename+'.txt -o align_time.json')

def create_manifest(filename):
    filename = filename.split('/')[-1]
    f = open('align_time.json', 'r')
    data = json.load(f)
    m = open('manifest.json', 'w')

    cnt = 0
    manifest = []

    for i in data['words']:
        if(i['case'] == 'success'):
            start = i['start']
            end = i['end']
            duration = end-start
            word = i['word'].lower()
            name = 'videos/video_'+filename+'_'+str(cnt)+'.mp4'
            words_dict[word] = words_dict.get(word, [])
            words_dict[word].append((duration, name))
            cnt += 1
            dic = {'start_time':start, 'length':duration, 'rename_to':name}
            manifest.append(dic)

    json.dump(manifest, m)
    m.close()

def split_files(filename):
        ffmpeg_split.split_by_manifest(filename+'.mp4', 'manifest.json', vcodec='h264')

def update_videos():
	for _ in range(6):
		try:
		    file_dict_fileobj = open('file_dict.pkl', 'rb')
		    file_dict = pkl.load(file_dict_fileobj)
		    file_dict_fileobj.close()
		except:
		    file_dict = {}

		try:
		    dict_file = open('words_dict.pkl', 'rb')
		    words_dict = pkl.load(dict_file)
		    dict_file.close()
		except:
		    words_dict = {}

		filenames = glob.glob('./source/*.mp4')
		count = 0
		for i in filenames:
		    if count>5: 
			break
		    if not file_dict.get(i, False):
		    	count+=1
		        file_dict[i] = True
		        align_time(i[:-4])
		        create_manifest(i[:-4])
		        split_files(i[:-4])
	
		file_dict_fileobj = open('file_dict.pkl', 'wb')
		pkl.dump(file_dict, file_dict_fileobj)
		file_dict_fileobj.close()


		dict_file = open('words_dict.pkl', 'wb')
		pkl.dump(words_dict, dict_file)
		dict_file.close()
