import pandas as pd 
import numpy as np 


def splitter(value,empty_type):
	if type(value) == str:
		new_value = eval(value.replace("'",""))
	elif type(value) == float:
		new_value = empty_type
	assert type(new_value) == type(empty_type)
	return new_value


def calc_each(data,subst=True):
	n = len(data)
	total_in = 0
	total_both = 0
	total_out = 0
	in_zero = 0
	viewed_dict = {}
	for i in range(n):
		shoe = data.iloc[i]
		viewed = splitter(shoe['also_viewed'],list())
		in_data = 0
		in_both = 0
		out_data = 0
		viewed_dict[shoe.name] = []
		for v in viewed: 
			try: 
				data.loc[v]
				in_data += 1
				viewed_dict[shoe.name].append(v)
				try:
					if shoe.name in data.loc[v]['also_viewed']:
						in_both +=1
				except TypeError:
					pass
			except KeyError:
				out_data +=1
		assert len(viewed_dict[shoe.name]) == in_data
		#print('in_data: '+str(in_data)+', out_data: '+str(out_data)+', both_data: '+str(in_both))
		total_in += in_data
		total_both += in_both
		total_out += out_data
		if in_data == 0:
			in_zero += 1
	print(total_in)
	print(total_both)
	print(total_out)
	print(in_zero)






if __name__ == "__main__":
	data = pd.read_csv('./data/boots_aws_metadata.csv',index_col='asin')
	del data['#']
	calc_each(data)


