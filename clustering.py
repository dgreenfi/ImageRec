import sklearn
from pandas import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn import mixture
import csv
import pickle

def load_data(path):
    lookup_dict={}
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            lookup_dict[row[4]]={"url":row[6]}
    return lookup_dict

def create_html(links,fname):
    file=open(fname,"w+")
    file.write("{% extends 'basetemp.html' %}\n \
        {% block head %}\n \
        {{ super() }}\n \
        {% endblock %}\n \
        {% block content %}\n")
    for item in links:
        file.write("<img src="+item+" height='100' width='100'>\n")
    file.write("{% endblock %}\n")

def output_clusters(clusters,fname):
    file=open(fname,"w+")
    for item in clusters:
        file.write(','.join(item)+'\n')

def main():
    f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
    #f ='/Users/davidgreenfield/Downloads/features_f500.csv'
    cols=range(1,4096)
    feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
    asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)
    cluster_num=25
    k_means=cluster.KMeans(n_clusters=cluster_num)
    k_means.fit(feats)
    clusters=[]
    groups={}
    data=load_data('./data/boots_aws.csv')

    for i in range(0,cluster_num):
        groups[i]=np.where(k_means.labels_==i)
        ids=asins[groups[i]]
        clusters.append(ids)
        links=[data[x]['url'] for x in ids]
        create_html(links,"templates/groups/group"+str(i)+".html")
    clust_dict={}
    for i,c in enumerate(clusters):
        clust_dict[i]=c


    f=open("outputs/clusters.txt",'w+')
    pickle.dump(clust_dict,f)
    f.close()
    #f2=open("outputs/clusters.txt",'r')
    #new=pickle.load(f2)
    #print new


if __name__ == '__main__':
    main()