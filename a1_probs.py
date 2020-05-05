import pandas as pd
import pickle
import numpy as np
import a1_rtgs
import a1_preds

def series_playoff_8(t1,t2,best_of,rtgs):
	W = 1
	wins = 0
	loses = 0
	if np.random.normal(d[t1]-d[t2],12) > 0:
		wins = 1
	else:
		loses = 1
	return wins, loses

def series_playoff(t1,t2,best_of, rtgs):
    if best_of == 5:
        W = 3
    else:
        if best_of == 3:
            W = 2
        else:
            print("Best of 3 or 5 series")
            return 
    wins = 0
    loses = 0
    for i in list(range(1,best_of+1)):
        if (i % 2) != 0:
            if np.random.normal(d['Home']+d[t1]-d[t2],12) > 0:
                wins+=1
            else:
                loses+=1
        else:
            if np.random.normal(d['Home']+d[t2]-d[t1],12) > 0:
                loses += 1
            else:
                wins += 1
        if wins == W or loses == W:
            break
    return wins, loses

########### Simulation callback ###########

def sim_callback(res):

	preds = a1_preds.predictions("remaining_regular_season.csv",d)
	f_res = "results.csv"
	df = pd.read_csv(f_res)
	games = preds
	df['ptsDiff'] = df['GH']-df['GA']
	df = df.drop(['Date','Nothing','Overtimes','Notes','GA','GH'],axis=1)
	final_df = pd.concat([df,games],sort=False).reset_index()
	teams = list(set(df.home.unique()) & set(df.away.unique()))
	points = { i : 0 for i in teams }
	standings = []

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
				standings.append(list(tie_stand.keys())[t])
		else:
			standings.append(list(ties.values())[i][0])
	
	for s in range(len(standings)):
		res[standings[s]][s]+=1
	# simulate playoffs 
	advance_to_second_round = []
	t1 = standings[0]
	t2 = standings[7]
	wins, loses = series_playoff_8(t1,t2,3,d)
	if wins == 1:
		advance_to_second_round.append(t1)
	else:
		advance_to_second_round.append(t2)	
	
	t1 = standings[1]
	t2 = standings[6]
	wins, loses = series_playoff_8(t1,t2,3,d)
	if wins == 1:
		advance_to_second_round.append(t1)
	else:
		advance_to_second_round.append(t2)
	
	t1 = standings[2]
	t2 = standings[5]
	wins, loses = series_playoff_8(t1,t2,3,d)
	if wins == 1:
		advance_to_second_round.append(t1)
	else:
		advance_to_second_round.append(t2)

	t1 = standings[3]
	t2 = standings[4]
	wins, loses = series_playoff_8(t1,t2,3,d)
	if wins == 1:
		advance_to_second_round.append(t1)
	else:
		advance_to_second_round.append(t2)

	# semis
	for s in advance_to_second_round:
		res[s][14] += 1
	advance_to_finals = []
	small_finals = []
	t1 = advance_to_second_round[0]
	t2 = advance_to_second_round[3]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_second_round[3]
		t2 = advance_to_second_round[0]
	wins, loses = series_playoff_8(t1,t2,5,d)
	if wins == 1:
		advance_to_finals.append(t1)
		small_finals.append(t2)
	else:
		advance_to_finals.append(t2)
		small_finals.append(t1)

	t1 = advance_to_second_round[1]
	t2 = advance_to_second_round[2]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_second_round[2]
		t2 = advance_to_second_round[1]
	wins, loses = series_playoff_8(t1,t2,5,d)
	if wins == 1:
		advance_to_finals.append(t1)
		small_finals.append(t2)
	else:
		advance_to_finals.append(t2)
		small_finals.append(t1)


	# finals
	for s in advance_to_finals:
		res[s][15]+=1
	t1 = advance_to_finals[1]
	t2 = advance_to_finals[0]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_finals[0]
		t2 = advance_to_finals[1]
	wins, loses = series_playoff_8(t1,t2,5,d)
	if wins == 1:
		res[t1][-1] += 1
	else:
		res[t2][-1] += 1


##### load ##### 

d = a1_rtgs.bball_ratings("results.csv")

global status

teams = ['Panathinaikos OPAP', 'AEK Athens', 'Peristeri', 'Promitheas Patras', 'Ifaistos Limnou','Lavrio B.C.', 'Iraklis B.C.', 'Larisa', 'Kolossos Rodou', 'Ionikos Nikaias', 'Rethymno Aegean', 'Panionios','Aris','P.A.O.K.']
points = [38,36,33,31,31,31,29,28,28,28,27,26,26,25]


sim_res = dict()

for team in teams:
	sim_res[team] = [0 for _ in range(17)]

for _ in range(10000):
	sim_callback(sim_res)

print(sim_res)

pickle.dump( sim_res, open( "probs_final8.pkl", "wb" ) )

