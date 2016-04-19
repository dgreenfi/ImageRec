import sklearn
from pandas import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import VBGMM, DPGMM
from sklearn import cluster
from sklearn import mixture
import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy


MAKE_GRAPH=1

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

def main(method,cluster_num=30,alpha=.5):
    f ='/Users/davidgreenfield/Downloads/features_csv_tmp.csv'
    #f ='/Users/davidgreenfield/Downloads/features_f500.csv'
    cols=range(1,4096)
    feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
    asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)
    if method == 'kmeans':
        k_means=cluster.KMeans(n_clusters=cluster_num)
        k_means.fit(feats)
        y = k_means.labels_
        if MAKE_GRAPH==1:
            print "hello 1"
        create_graph(k_means)
    elif method == 'GMM_VB':
        gmm_vb = VBGMM.fit(feats,n_components=50,alpha=.5)
        y = gmm_vb.predict(feats)
        cluster_no = len(np.unique(y))
    elif method == 'GMM_DP':
        gmm_dp = DPGMM(n_components=50,alpha=alpha)
        gmm_dp.fit(feats)
        y = gmm_dp.predict(feats)
        cluster_no = len(np.unique(y))


    clusters=[]
    groups={}
    data=load_data('./data/boots_aws.csv')

    for i in range(0,cluster_num):
        groups[i]=np.where(y==i)
        ids=asins[groups[i]]
        clusters.append(ids)
        links=[data[x]['url'] for x in ids]
        create_html(links,"templates/groups/group"+str(i)+".html")

    output_clusters(clusters,"outputs/clusters.csv")


def create_graph(k_means):
    """
    could be used with an object with a .cluster_centers_ attribute that returns the center features of each cluster
    """
    centers=k_means.cluster_centers_
    G=nx.Graph()
    labels={}
    dist_mat=np.zeros((len(centers),len(centers)))
    dist_mat_cos=np.zeros((len(centers),len(centers)))
    all_dist=[]
    for i,clust in enumerate(centers):
        for y in range(0,len(centers)):
            dist=scipy.spatial.distance.euclidean(centers[i],centers[y])
            dist_cos=scipy.spatial.distance.cosine(centers[i],centers[y])
            if i==y:
                dist=10000000
            dist_mat[i][y]=dist
            dist_mat_cos[i][y]=dist_cos
            all_dist.append(dist_cos)


    for i,row in enumerate(dist_mat):
        for neighbor in row.argsort()[:0]:
            G.add_edge(i,neighbor)

    for i,row in enumerate(dist_mat_cos):
        for neighbor in row.argsort()[:4]:
            if row[neighbor]>0:
                G.add_edge(i,neighbor,weight=1/row[neighbor])

    #for i,row in enumerate(dist_mat_cos):
    #    for y,pt in enumerate(row):
    #        if pt>np.percentile(all_dist,90):
    #            G.add_edge(i,y)

    print G.nodes()
    pos = nx.spring_layout(G,scale=4)
    for lab in G.nodes():
        labels[lab]=lab
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),label=True)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='r', arrows=False)
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.savefig('graph.png')
    #plt.show()
    return
    #create a graph in networkX


if __name__ == '__main__':
    main('kmeans')