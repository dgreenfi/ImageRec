import numpy as np 
import pandas as pd 
import os, pickle
from sklearn.metrics.pairwise import (
    euclidean_distances, cosine_similarity, pairwise_distances
)


#from application import load_data
from random import random
import redis
"""
Creates similarity matrix for application to load
"""


def pull_data(user_file):
	f = user_file
	cols=range(1,4096)
	feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
	asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)
	return feats, asins 

def dist_pd(user_file,method):
	feats, asins = pull_data(user_file)
	shoes_df = pd.DataFrame(feats,index=asins)
	dists = method(shoes_df)
	dists_df = pd.DataFrame(dists,index=shoes_df.index)
	dists_df.columns = dists_df.index
	return dists_df
	

def get_sims(products_like,products_dislike,dists_df,n=0,larger_is_closer=True):
	dist_cluster = dists_df.loc[:, [c for c in dists_df.columns if c in products_like]]
	p = dist_cluster.sum(axis=1)
	print larger_is_closer
	p = p.order(ascending=larger_is_closer)
	p = p[p.index.isin(products_dislike)==False]
	return p.index[p.index.isin(products_like)==False]

# def dist_main(shoes_df,method,products_like):
# 	dists_df = dist_pd(shoes_df,method)
# 	closest = get_sims(products_like,dists_df)
# 	return closest

# def distance_rec(shoes_df,method,products_like):
# 	closest = dist_main(shoes_df,method,products_like)
# 	closest_cluster = closest.index[closest.index.isin(cluster_asins)]
# 	return 

def calc_sim(dist_df,likes,dislikes,cluster_dict=None,cluster_no=None,n=0):
	if likes == []:
		return random.choice(cluster_dict[cluster_no])
	else:
		if cluster_dict != None and cluster_no != None:
			dists_df = dist_df[dist_df.index.isin(cluster_dict[cluster_no])]
		p = get_sims(list(likes),list(dislikes),dists_df,larger_is_closer=True)
		return p[n]

def calc_sim_rec(dist_df,likes,dislikes,n=0,larger_is_closer=True):
	if likes == []:
		return random.choice(dist_df.index)
	else:
		#dists_df = dist_df[dist_df.index.isin(cluster_dict)]
		p = get_sims(list(likes),list(dislikes),dist_df,n,larger_is_closer)
		return p[0:n]


if __name__ == "__main__":
	#dists_df = dist_pd('/Users/davidgreenfield/Downloads/features_women.csv',cosine_similarity)
	#print(dists_df)
	#pickle.dump(dists_df,open('./data/dist_df.txt','w+'))
	#quit()
	f = open('./outputs/clusters.txt','r')
	cluster_dict  = pickle.load(f)
	f = open('./data/dist_df.txt','r')
	dist_df  = pickle.load(f)
	conn = redis.Redis(db=1)
	likes = conn.smembers('Erin')
	cluster_no = 8
	dists_df = dist_df[dist_df.index.isin(cluster_dict[cluster_no])]
	
	#assert len(p) == len(cluster_dict[cluster_no])
	




