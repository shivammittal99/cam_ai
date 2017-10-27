import os
import pickle as pkl

input_file = open('input.txt', 'r')
input_text = input_file.read()
input_text = input_text.strip().split()
input_file.close()

dict_file = open('words_dict_temp1.pkl', 'rb')
words_dict = pkl.load(dict_file)
dict_file.close()

output_list = open('mylist.txt', 'w')

#command = './mmcat'

for i in input_text:
    filename = words_dict.get(i.lower(), None)
    if filename:
        filename.sort()
        for j in range(len(filename)):
            if os.path.isfile(filename[j][1]):
                print filename[j][1]
                #command += ' ' + filename[j][1]
                output_list.write('file \''+filename[j][1]+'\'\n')
                break
#command += ' output.mp4'
#print command

#os.system(command)
output_list.close()

os.system('ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4')
#os.system('ffmpeg -i output.mp4 -filter_complex \"[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]\" -map \"[v]\" -map \"[a]\" -strict -2 output1.mp4')
