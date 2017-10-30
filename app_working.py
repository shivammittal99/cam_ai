from flask import Flask, render_template, jsonify, request
import nltk
from pickle import load, dump
from nltk import word_tokenize, pos_tag
import random
import hashlib
import os
from random import shuffle
from nltk.stem.snowball import SnowballStemmer
import math

app = Flask(__name__)
rootUrl = "http://40.71.87.18:5000"
dict_file = open('./videos/words_dict_temp1.pkl', 'rb')
words_dict = load(dict_file)
dict_file.close()
unfound_dict_file = open('./videos/unfound/unfound_dict.pkl', 'rb')
unfound_dict = load(unfound_dict_file)
unfound_dict_file.close()

def write_subs(sub_text, audio_time, filename):
    f = open('tempshort.srt', 'w')
    f.write('1\n')
    ti = audio_time
    ms = (ti%1)
    ms = int(ms*1000)
    ti = ti - ti%1
    seconds = int(ti%60)
    ti = ti/60
    minutes = int(ti%60)
    ms_str = ('000'+str(ms))[-3:]
    second_str = ('000'+str(seconds))[-2:]
    minutes_str = ('000'+str(minutes))[-2:]
    f.write('00:00:00,000 --> 00:'+minutes_str+':'+second_str+','+ms_str+"\n")
    f.write(sub_text+'\n')
    f.close()
    com = "ffmpeg -y -i "+filename+" -vf subtitles=tempshort.srt:force_style='Fontsize=30' -strict -2 -qscale:v 3 "+ filename
    os.system(com)		

def process(string1, name, com):
    os.system('rm ./waste/*')
    string1 = string1.lower()
    tokens = word_tokenize(string1)
    tokens = [e.encode('ascii', 'ignore') for e in tokens]
    print tokens
    #output_list = open('mylist.txt', 'w')
    comm = 'cat'
    
    file_no_var = 1
    
    for i in tokens:
        filenames = words_dict.get(i, None)
        if filenames:
            #filenames.sort(reverse=True)
            shuffle(filenames)
            max_pos = filenames[filenames.index(max(filenames))]
            temp = 0
            while temp < len(filenames):
                if filenames[temp][0] > 0.3 * len(i) or filenames[temp][0] < 0.8 * max_pos[0]:
                    temp += 1;
                    continue
                else: 
                    filename = 'videos4' + filenames[temp][1][7:]
                    #output_list.write('file \'' + './videos/' + filename + '\'\n')
                    os.system('ffmpeg -y -i ' + './videos/'+filename+' ./waste/' + filename[7:-1] + 'g')
                    comm += ' ./waste/' + filename[7:-1] + 'g'
                    break
            
            if temp == len(filenames):
                os.system('espeak ' + '\"'+i+'\" --stdout > out.mp3')
                print('espeak ' + '\"'+i+'\" --stdout > out.mp3')
                os.system('ffprobe -show_entries format=duration -i out.mp3 > temp.txt')
                haha = open('temp.txt', 'r')
                audio_time = float(haha.readlines()[1][9:])
                haha.close()
                #audio_time -= audio_time%0.25
                audio_time = math.ceil(audio_time * 4) / 4.0
                unfound_filename = random.choice(unfound_dict[audio_time])
                unfound_filename = './videos/unfound' + unfound_filename[1:]
                str1 = ('ffmpeg -y -i ' + unfound_filename + ' -i out.mp3 -map 0:0 -map 1:0 -c:v copy -c:a aac -shortest -strict -2 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
                #str1 = ('ffmpeg -y -i ' + unfound_filename + ' -i out.mp3 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
                print str1
                os.system(str1)
                write_subs(i, audio_time, './waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
                os.system('ffmpeg -y -i ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mpg')
                comm += ' ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mpg'
                file_no_var += 1
        else:
            os.system('espeak ' + '\"'+i+'\" --stdout > out.mp3')
            print('espeak ' + '\"'+i+'\" --stdout > out.mp3')
            os.system('ffprobe -show_entries format=duration -i out.mp3 > temp.txt')
            haha = open('temp.txt', 'r')
            audio_time = float(haha.readlines()[1][9:])
            haha.close()
            #audio_time -= audio_time%0.25
            audio_time = math.ceil(audio_time * 4) / 4.0
            unfound_filename = random.choice(unfound_dict[audio_time])
            unfound_filename = './videos/unfound' + unfound_filename[1:]
            str1 = ('ffmpeg -y -i ' + unfound_filename + ' -i out.mp3 -map 0:0 -map 1:0 -c:v copy -c:a aac -shortest -strict -2 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
            #str1 = ('ffmpeg -y -i ' + unfound_filename + ' -i out.mp3 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
            print str1
            os.system(str1)
            write_subs(i, audio_time, './waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4')
            os.system('ffmpeg -y -i ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mp4 ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mpg')
            comm += ' ./waste/' + unfound_filename[17:-4] + str(file_no_var) + '.mpg'
            file_no_var += 1
                     
            #temp = 0
            #filename = 'gibberish'
            #while temp < len(filenames):
            #    if filenames[temp][0] >= len(i) * 0.1:
            #        print (i, temp, filenames[temp][0], len(i))
            #        filename = filenames[temp][1]
            #        break
            #    else:
            #        temp += 1
            #if filename != 'gibberish':
            #    print (i, 'natural')
            #    filename = 'videos2' + filename[7:]
            #    #output_list.write('file \''+'./videos/'+filename+'\'\n')
            #    os.system('ffmpeg -i ' + './videos/'+filename+' ./waste/' + filename[7:-1]+'g')
            #    comm += ' ./waste/' + filename[7:-1] + 'g'
            #else:
            #    print (i, 'artificial')
            #    filename = 'videos2' + filenames[0][1][7:]
            #    #os.system('ffmpeg -y -v 0 -i ./videos/' + filename + ' -filter_complex "[0:v]setpts=1.5*PTS[v];[0:a]atempo=0.66[a]" -map "[v]" -map "[a]" -strict -2 ./videos/temp'+filename)
            #    #output_list.write('file \''+'./videos/temp'+filename+'\'\n')
            #    os.system('ffmpeg -i ' + './videos/'+filename+' ./waste/' + filename[7:-1] + 'g')
            #    comm += ' ./waste/' + filename[7:-1] + 'g'
    #output_list.close()
    #os.system(com)
    #print 'normalizing sound'
    #os.system('ffmpeg-normalize --merge ./static/'+name+'.mp4')
    os.system(comm + ' > ./waste/out.mpg')
    os.system('ffmpeg -y -i ./waste/out.mpg -qscale:v 2 -strict -2 ./static/'+name+'.mp4')
    return name+'.mp4'
@app.route('/')
def index():
    return jsonify({"url":"https://www.youtube.com/watch?v=EpbjEttizy8"});
@app.route('/magic')
def magic():
    string1 = request.args.get('str',default="hello")
    alphabets = ['a','b','c','d','e','f','g','h','i']
    name = ''
    for i in range(10):
        name+=random.choice(alphabets)
    com = 'ffmpeg -f concat -safe 0 -i mylist.txt -c copy ./static/'+name+'.mp4'
    vidName = process(string1,name,com)
    retUrl = rootUrl + '/static/'+vidName 
    return jsonify({"url":retUrl,"str":string1});
@app.route('/done/<path>')
def done(path):
    return app.send_static_file(path)
if __name__ =='__main__':
    app.run('0.0.0.0',debug=False)

