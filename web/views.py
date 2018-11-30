import sys
sys.path.append('../')
from setting import PROJECT_DIR
sys.path.append('PROJECT_DIR')


from flask import jsonify, render_template, request
from flask import Flask
from os import path
import os
from random import random as rand

from backend.db import dbconn

app = Flask(__name__)
conn = dbconn.getDBConn()

@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/')
def index():
    return render_template('jquery.html')

@app.route('/fresh', methods=['GET'])
def fresh():
	return jsonify(getMacDict())
	return jsonify(getRandJsonDict())

def getMacDict():
	stat = "SELECT mac, COUNT(*) FROM sniffer GROUP BY mac;"
	res = dbconn.executeQuery(conn, stat)
	return dict(row for row in res)

def getRandJsonDict():
	l = ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL', 'MM', 'NN', 'OO', 'PP']
	d = {}
	for dev in l:
		if rand() < 0.3:
			d[dev] = int(rand()*30)
	return d



if __name__ == "__main__":
	extra_dirs = ['directory/to/watch',] 
	extra_files = extra_dirs[:] 
	for extra_dir in extra_dirs: 
	    for dirname, dirs, files in os.walk(extra_dir): 
	     for filename in files: 
	      filename = path.join(dirname, filename) 
	      if path.isfile(filename): 
	       extra_files.append(filename) 
	app.run(extra_files=extra_files) 