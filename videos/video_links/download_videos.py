import os

f = open('links.txt')

links = f.readlines()
for i in links:
	os.system('youtube-dl --write-auto-sub --convert-subs srt --format mp4 '+i)
f.close()
