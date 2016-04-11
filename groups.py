import pandas as pd 
import numpy as np 


class cluster_eval:
	def __init__(self,data):
		self.data = data
		self.dups = self.remove_dups()



def splitter(self,value,empty_type):
	if type(value) == str:
		new_value = eval(value.replace("'",""))
	elif type(value) == float:
		new_value = empty_type
	assert type(new_value) == type(empty_type)
	return new_value

def remove_dups(self):
	dups = {}
	n = len(self.data)
	for d in self.data.index:
		salesRank = self.data['salesRank'][d]
		try:
			dups[salesRank].append(d)
		except KeyError:
			dups[salesRank] = [d]
	self.dups = {k:v for k,v in dups.items() if len(v) > 1}

# def clean_data(self):
# 	n = len(self.data)
# 	for i in range(n):
		


			

def calc_each(self,sub):
	n = len(data)
	total_in = 0
	total_both = 0
	total_out = 0
	in_zero = 0
	sub_mat = {}
	for i in range(n):
		shoe = self.data.iloc[i]
		viewed = self.splitter(shoe[sub],list())
		in_data = 0
		in_both = 0
		out_data = 0
		sub_mat[shoe.name] = []
		for v in viewed: 
			try: 
				self.data.loc[v]
				in_data += 1
				sub_mat[shoe.name].append(v)
				try:
					if shoe.name in self.data.loc[v][sub]:
						in_both +=1
				except TypeError:
					pass
			except KeyError:
				out_data +=1
		assert len(sub_mat[shoe.name]) == in_data
		#print('in_data: '+str(in_data)+', out_data: '+str(out_data)+', both_data: '+str(in_both))
		total_in += in_data
		total_both += in_both
		total_out += out_data
		if in_data == 0:
			in_zero += 1
	sub_mat = {k:v for k,v in sub_mat.items() if v != []}
	assert len(sub_mat) == n - in_zero
	return sub_mat

def metrics(clusters,sub_mat):
	results = {}
	n = len(clusters)
	same_cluster_all = 0
	diff_cluster_all = 0
	for c in range(n):
		same_cluster = 0
		dif_cluster = 0 
		avg_ = 0
		for i in clusters[c]:
			try:
				for j in sub_mat[i]:
					if j in c:
						same_cluster += 1
						same_cluster_all += 1
					else:
						dif_cluster += 1 
						dif_cluster_all += 1
			except KeyError:
				pass
		avg_ = same_cluster/len(cluster[c])
		results[str(c)+'_avg'] = avg_
		#results[c] = same_cluster/(same_cluster+dif_cluster)
	results['avg'] = np.mean([v for k,v in results.items()])
	results['all'] = same_cluster_all/(same_cluster_all+diff_cluster_all)
	return results 









if __name__ == "__main__":
	data = pd.read_csv('./data/boots_aws_metadata.csv',index_col='asin')
	CE = cluster_eval(data)
	sub_mat = CE.calc_each('also_viewed')
	results = metrics(clusters,sub_mat)


