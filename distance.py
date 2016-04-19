import numpy as np 
import pandas as pd 
import os, pickle
from sklearn.metrics.pairwise import (
    euclidean_distances, cosine_similarity, pairwise_distances
)


from application import load_data




def pull_data(cluster_dict,user_file):
	f = open(cluster_dict,'r')
	cluster_dict  = pickle.load(f)

	f =user_file
	cols=range(1,4096)
	feats =np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=(cols))
	asins = np.loadtxt(open(f,"rb"),delimiter=",",skiprows=1,usecols=([0]),dtype=str)

	return cluster_dict, feats, asins 

def dist_pd(shoes_df,method):
	dists = method(shoes_df)
	dists_df = pd.DataFrame(dists,columns=shoes_df.columns)
	dists_df.index = dists_df.columns
	return dists_df


def get_sims(products_like,method,dists_df,larger_is_closer=False):
	dists = method(shoes_df,products_like)
	dists_df = pd.DataFrame(dists,)
	p = dists_df[products_like].apply(lambda row: np.sum(row),axis=1)
	p = p.order(ascending=larger_is_closer)
	return p.index[p.index.isin(products)==False]

def dist_main(shoes_df,method,products_like):
	dists_df = dist_pd(shoes_df,method)
	closest = get_sum(products_like,dists_df)
	return closest

def distance_rec(shoes_df,method,products_like):
	closest = dist_main(shoes_df,method,products_like)
	closest_cluster = closest.index[closest.index.isin(cluster_asins


if __name__ == "__main__":
	