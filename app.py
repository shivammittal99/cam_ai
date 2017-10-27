from flask import Flask, render_template,jsonify,request
import nltk
from pickle import load,dump
from nltk import word_tokenize,pos_tag
import random
import hashlib
import os
from nltk.stem.snowball import SnowballStemmer
app = Flask(__name__)
rootUrl = "http://52.168.139.241:5000";
dict_file = open('./videos/words_dict_temp1.pkl','rb')
words_dict = load(dict_file)
dict_file.close()
def process(str,name,com):
	str = str.lower()
	tokens = word_tokenize(str)
	tokens = [e.encode('ascii','ignore') for e in tokens]
	print tokens
	output_list = open('mylist.txt', 'w')
	for i in tokens:
    		filename = words_dict.get(i, None)
		if filename:
    			filename.sort()
    			filename = filename[-1][1]
    			if filename:
        			output_list.write('file \''+'./videos/'+filename+'\'\n')
	output_list.close()
	os.system(com)
	return name+'.mp4'
@app.route('/')
def index():
	return jsonify({"url":"https://www.youtube.com/watch?v=EpbjEttizy8"});
@app.route('/magic')
def magic():
	str = request.args.get('str',default="hello")
	alphabets = ['a','b','c','d','e','f','g','h','i']
	name = ''
	for i in range(10):
		name+=random.choice(alphabets)
	com = 'ffmpeg -f concat -safe 0 -i mylist.txt -c copy ./static/'+name+'.mp4'
	vidName = process(str,name,com)
	retUrl = rootUrl + '/static/'+vidName 
	return jsonify({"url":retUrl,"str":str});
@app.route('/done/<path>')
def done(path):
	return app.send_static_file(path)
if __name__ =='__main__':
	app.run('0.0.0.0',debug=False)

