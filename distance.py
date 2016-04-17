import numpy as np 
import pandas as pd 
from sklearn.metrics.pairwise import (
    euclidean_distances, cosine_similarity, pairwise_distances
)


def dist_pd(shoes_df,method):
	dists = method(shoes_df)
	dists_df = pd.DataFrame(dists,columns=shoes_df.columns)
	dists_df.index = dists_df.columns
	return dists_df

def get_sims(products,dists_df,larger_is_closer=False):
	p = dists_df[products].apply(lambda row: np.sum(row),axis=1)
	p = p.order(ascending=larger_is_closer)
	return p.index[p.index.isin(products)==False]

def dist_main(shoes_df,method,products):
	dists_df = dist_pd(shoes_df,method)
	closest = get_sum(products,dists_df)
	return closest


