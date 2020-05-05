from scipy.stats import norm
from matplotlib import pyplot as plt
import sys
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import optimize

def standings(f_res,games):
	df = pd.read_csv(f_res)
	df['ptsDiff'] = df['GH']-df['GA']
	df = df.drop(['Date','Nothing','Overtimes','Notes','GA','GH'],axis=1)
	final_df = pd.concat([df,games],sort=False).reset_index()	
	teams = list(set(df.home.unique()) & set(df.away.unique()))
	points = { i : 0 for i in teams }

	for i in range(len(final_df)):
		if final_df['ptsDiff'][i] > 0:
			points[final_df['home'][i]] += 2
			points[final_df['away'][i]] += 1
		else:
			points[final_df['home'][i]] += 1
			points[final_df['away'][i]] += 2
	points = {k: v for k, v in sorted(points.items(), key=lambda item: item[1],reverse=True)}
	ties = {}
	for pair in points.items():
		if pair[1] not in ties.keys():
			ties[pair[1]] = []
		ties[pair[1]].append(pair[0])
	print(len(ties))
	for i in range(len(ties)):
		if len(list(ties.values())[i]) != 1:
			tie_dict = {i: [0,0] for i in list(ties.values())[i]}
			for g in range(len(final_df)):
				if final_df['home'][g] in tie_dict.keys() and final_df['away'][g] in tie_dict.keys():
					if final_df['ptsDiff'][g] > 0:
						tie_dict[final_df['home'][g]][0] += 1
					else:
						tie_dict[final_df['away'][g]][0] += 1
					tie_dict[final_df['home'][g]][1] += final_df['ptsDiff'][g]
					tie_dict[final_df['away'][g]][1] -= final_df['ptsDiff'][g]
			tie_stand = {k: v for k, v in sorted(tie_dict.items(), key=lambda item: item[1],reverse=True)}
			for t in range(len(tie_stand.keys())):
				print(list(tie_stand.keys())[t],list(ties.keys())[i])
		else:
			print(list(ties.values())[i][0],list(ties.keys())[i])

