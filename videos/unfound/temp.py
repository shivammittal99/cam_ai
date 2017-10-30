import json
import pickle as pkl
import glob
import os
import ffmpeg_split

def create_manifest(filename):
    filename = filename.split('/')[-1]
    f = open('./source_temp/align_'+filename+'.json', 'r')
    data = json.load(f)
    m = open('manifest_temp.json', 'w')
    
    cnt = 0
    manifest = []

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
            dic = {'start_time':start, 'length':duration, 'rename_to':name}
            manifest.append(dic)

    json.dump(manifest, m)
    m.close()

def split_files(filename):
    ffmpeg_split.split_by_manifest(filename+'.mp4', 'manifest_temp.json', vcodec='h264')

def update_videos():
    filenames = glob.glob('./*.mp4')
    for f in filenames:
        try:
            dict_fileobj = open('unfound_dict.pkl', 'rb')
            unfound_dict = pkl.load(dict_fileobj)
            dict_fileobj.close()
        except:
            unfound_dict = {}
        manifest = []
        cnt = 0
        for i in range(1, 7):
            m = open('manifest_temp.json', 'w')
            for j in range(48/i):
                duration = i*0.25
                name = f[:-4] + str(cnt) + '_' + str(duration) + '.mp4'
                dic = {'start_time':0.25*j*i, 'length':duration, 'rename_to':name}
                unfound_dict[duration] = unfound_dict.get(duration, [])
                unfound_dict[duration].append(name)
                manifest.append(dic)
                cnt += 1
        json.dump(manifest, m)
        m.close()

        split_files(f[:-4])
    
        dict_fileobj = open('unfound_dict.pkl', 'wb')
        pkl.dump(unfound_dict, dict_fileobj)
        dict_fileobj.close()

update_videos()
