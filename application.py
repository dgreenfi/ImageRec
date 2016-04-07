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
LABS=['Fuzzy','Leather','Suede','Cowboy','Brown','Black','Red','Blue','Pink','Grey','Shiny',\
      'Cowboy','Checkered','Ruffled','Bootie','Thick Outsole','Hiking','Spotted',\
      'Zebra','Clasps','High Heel','Glossy',"Rain Boots","Sneaker Boot","Crazy Color","Crazy Pattern","Knee High","Moon Boot"]

@application.route('/')
def homepage():
    #requires local version of csv and images
    data=load_data('./data/boots_aws.csv')
    args=request.args
    if 'user' not in args:
        return redirect("?user="+USERS[0], code=302)
    testfolder='/Users/davidgreenfield/Downloads/pics_boots/'
    rand = random.choice(list(data.keys()))
    impath=data[rand]

    return render_template('index.html',string=impath['url'],asin=rand,users=USERS,activeuser=args['user'])


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
    print likes
    links=[data[x]['url'] for x in likes]

    return render_template('choices.html',vals=links,users=USERS,activeuser=args['user'])

@application.route('/groupview')
def groupview():
    args=request.args
    if 'user' not in args:
        return redirect("groupview?user="+USERS[0]+"&groupnum=1", code=302)
    if 'groupnum' not in args:
        return redirect("groupview?user="+USERS[0]+"&groupnum=1", code=302)
    num=args['groupnum']
    groups=["Group "+ str(x) for x in range(1,25)]
    return render_template('./groups/group'+str(num)+'.html',users=USERS,activeuser=args['user'],showgroups="Yes",groups=groups)

@application.route('/suggestions')
def suggestions():
    args=request.args
    if 'user' not in args:
        return redirect("suggestions?user="+USERS[0], code=302)
    return render_template('suggestions.html',users=USERS,activeuser=args['user'])


@application.route('/labeler')
def labeler():
    args=request.args
    if 'user' not in args:
        return redirect("labeler?user="+USERS[0], code=302)

    data=load_data('./data/boots_aws.csv')
    rand = random.choice(list(data.keys()))
    impath=data[rand]

    return render_template('labeler.html',users=USERS,activeuser=args['user'],string=impath['url'],asin=rand,labels=LABS)

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

@application.route('/submitLabel')
def submit_label():
    args=request.args
    label=args['label']
    asin=args['asin']
    f=open('./data/labels.txt','a+')
    f.write('{"'+asin+'":"'+label+'"}\n')
    return json.dumps({"stored":True})


if __name__ == '__main__':

    application.run(debug=True)