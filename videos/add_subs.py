import os
import pickle as pkl
dict_file = open('./words_dict_temp2.pkl','rb')
words_dict = pkl.load(dict_file)
dict_file.close()
cnt = 0

subs_dict = {}

try:
    subs_dict_fileobj = open('subs_dict.pkl', 'rb')
    subs_dict = pkl.load(subs_dict_fileobj)
    subs_dict_fileobj.close()
except:
    subs_dict = {}

for key in words_dict.keys():
    lst = words_dict[key]
    for e in lst:
        temp = e[-1][7:]
        filename = 'videos2'+temp
        if not subs_dict.get(filename[7:], False):
            subs_dict[filename[7:]] = True
            print filename, cnt
            cnt += 1
            f = open('tempshort.srt','w')
            
            f.write('1\n')
            ti = e[0]
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
            f.write(key+'\n')
            f.close()
            com = "ffmpeg -v 0 -y -i "+filename+" -vf subtitles=tempshort.srt:force_style='Fontsize=30' -strict -2 -qscale:v 3 "+ filename
            os.system(com)		
        
subs_dict_fileobj = open('subs_dict.pkl', 'wb')
pkl.dump(subs_dict, subs_dict_fileobj)
subs_dict_fileobj.close()
