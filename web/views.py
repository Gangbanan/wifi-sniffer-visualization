import sys
sys.path.append('../')
from setting import PROJECT_DIR
sys.path.append('PROJECT_DIR')


from flask import jsonify, render_template, request
from flask import Flask
import time
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
	#return jsonify(getRandJsonDict())

@app.route('/js/d3.v3.min.js')
def d3():
    return render_template('d3.v3.min.js')

@app.route('/js/jquery-3.3.1.min.js')
def jquery():
    return render_template("jquery-3.3.1.min.js")

def getMacDict():
        t = time.time()
	stat = """SELECT * FROM ( SELECT mac, COUNT(*) as times FROM sniff where time > {time1} and time < {time2} GROUP BY mac ) as frequency WHERE times < 60 ORDER BY times DESC limit 10;"""
        param = {"time1":t-10, "time2":t}
	res = dbconn.executeQuery(conn, stat.format(**param))
	re = dict(row for row in res)
        newre = {}
        for mac in re:
            newre["MAC" + "".join(mac.split(":"))] = re[mac]
        print(newre)
        return newre

def getRandJsonDict():
	l = ['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK', 'LL', 'MM', 'NN', 'OO', 'PP']
	d = {}
        for dev in l:
		if rand() < 0.3:
                        d[dev] ={}
			d[dev]['r'] = int(rand()*30)
                        d[dev]['manu'] = "Apple Inc."
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
