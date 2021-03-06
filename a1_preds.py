from scipy.stats import norm
import sys
import pandas as pd
import numpy as np
from scipy import optimize

def predictions(f,rtgs):
	games = pd.read_csv(f)
	pts_diff = [np.random.normal(rtgs['Home']+rtgs[games['home'][i]]-rtgs[games['away'][i]],12) for i in range(len(games))]		
	games['ptsDiff'] = pts_diff

	return games

#print("Home edge points: {:.3f}".format(res.x[ghome]))
#print()

##print("                          Team   Rating")

#for i, t in enumerate(teams):
#    print("{:s},{:.3f}".format(t, (res.x[i])))

'''
print "========================"
print "PREDICTIONS"
print "========================"

#sns.set_style('ticks')
#plt.scatter(res.x[n_teams:n_teams*2], res.x[:n_teams]); plt.ylabel("Offensive Rating"); plt.xlabel("Defensive Rating")
#plt.xlim(0.25, 2); plt.ylim(0.5, 1.7);
#sns.despine()

f_pred = open("next-games.csv","r")

home_edge = res.x[ghome]

for line in f_pred:
	linef = line.rstrip().rsplit(" , ")
	home = linef[2]
	away = linef[3]
	homeindex = teams.index(home)
	awayindex = teams.index(away)
	hrtg = res.x[homeindex]
	artg = res.x[awayindex]
	home_wp = 1 - norm.cdf(0,(home_edge+hrtg-artg),12)	
	print home,",",home_wp,",",1-home_wp,",",away
'''
