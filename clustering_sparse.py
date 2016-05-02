from pandas import *
import redis
from sklearn.mixture import VBGMM
from sklearn.mixture import DPGMM
from sklearn.cluster import KMeans
import sys

from beta_bandit import BetaBandit

class ClusteringImages:
    def __init__(self, df, coef, model_name, alpha, k):
        self.generate_model(model_name, alpha, k)
        self.features_df = df.iloc[:, np.nonzero(coef)[0]]
        self.fit_model()
        self.cluster()
        
    def generate_model(self, model_name, alpha, k):
        if model_name == 'VBGMM':
            self.model = VBGMM(n_components=k, covariance_type='diag', alpha=alpha, random_state=None, 
              thresh=None, tol=0.001, verbose=0, min_covar=None, n_iter=10, 
              params='wmc', init_params='wmc')
        elif model_name == 'DPGMM':
            self.model = DPGMM(n_components=k, covariance_type='diag', alpha=alpha, random_state=None, 
                  thresh=None, tol=0.001, verbose=0, min_covar=None, n_iter=10, 
                  params='wmc', init_params='wmc')        
        elif model_name == 'K-Means':
            self.model = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, 
                                tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, 
                                copy_x=True, n_jobs=1)
        else:
            print 'enter valid cluster'
            sys.exit(0)
        
    def fit_model(self):
        self.model.fit(self.features_df)
    
    def cluster(self):
	if 'cluster' in self.features_df.columns:
		self.features_df.drop('cluster', axis = 1, inplace = True)

        self.cluster_dict = {}
        pred = self.model.predict(self.features_df)
        self.features_df.loc[:, 'cluster'] = pred
	
	self.cluster_map = {}

        for i, cluster in enumerate(np.unique(pred)):
	    self.cluster_map[cluster] = i
            self.cluster_dict[i] = list(self.features_df[self.features_df.loc[:, 'cluster'] == cluster]\
                                   .drop('cluster', axis = 1)\
                                   .index)

    def count_votes_by_cluster(self, likes, dislikes):
        self.bb = BetaBandit(self.features_df.cluster.unique().shape[0])
	print 'clusters', self.features_df.cluster.unique().shape[0]
        for l in likes:
            self.bb.add_result(self.cluster_map[self.features_df.loc[l, 'cluster']], 1)
        for d in dislikes:
            self.bb.add_result(self.cluster_map[self.features_df.loc[d, 'cluster']], 0)

