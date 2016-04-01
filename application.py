from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from os import walk
import csv
import random
import redis
import json
application = Flask(__name__)

USERS=['Erin','Dave','Josh','Priya']

@application.route('/')
def homepage():
    #requires local version of csv and images
    data=load_data('./data/boots_aws.csv')
    args=request.args
    if 'user' not in args:
        return redirect("?user="+USERS[0], code=302)
    testfolder='/Users/davidgreenfield/Downloads/pics_boots/'
    randimage=get_image(testfolder)

    impath=data[randimage]
    return render_template('index.html',string=impath['url'],asin=randimage,users=USERS,activeuser=args['user'])


def get_image(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
    impath=random.choice(f)
    return impath[0:-4]

def load_data(path):
    lookup_dict={}
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            lookup_dict[row[4]]={"url":row[6]}
    return lookup_dict

@application.route('/userchoices')
def choices():
    data=load_data('./data/boots_aws.csv')
    args=request.args
    if 'user' not in args:
        return redirect("userchoices?user="+USERS[0], code=302)
    conn = redis.Redis(db=1)

    likes = conn.smembers(args['user'])

    links=[data[x]['url'] for x in likes]

    return render_template('choices.html',vals=links,users=USERS,activeuser=args['user'])


@application.route('/submit')
def submit():
    args=request.args
    if float(args['like'])==0:
        conn = redis.Redis(db=0)
        conn.sadd(args['user'],args['asin'])

    if float(args['like'])==1:
        conn = redis.Redis(db=1)
        conn.sadd(args['user'],args['asin'])


    return json.dumps({"stored":True})

if __name__ == '__main__':

    application.run(debug=True)