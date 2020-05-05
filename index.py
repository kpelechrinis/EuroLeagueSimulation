from bokeh.layouts import layout, row, column
from bokeh.plotting import save, figure, output_file, show, Column
from bokeh.models.glyphs import Text, ImageURL
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource,Arrow, OpenHead, NormalHead, VeeHead, HoverTool, Div
from bokeh.models.widgets.buttons import Button
from bokeh.models import Tabs, Panel
from bokeh.models.widgets import Slider,Select,PreText,Dropdown,TextInput,AutocompleteInput,CheckboxGroup,RadioGroup,RangeSlider
from bokeh.transform import cumsum
from scipy.misc import imread
from bokeh.io import curdoc
import pandas as pd
import numpy as np
import a1_rtgs
import a1_preds

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

def sim_callback():
	global status

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

	print("++++++++++++++++Final Standings++++++++++++++++")
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
				print(list(tie_stand.keys())[t],list(ties.keys())[i])
				standings.append(list(tie_stand.keys())[t])
		else:
			print(list(ties.values())[i][0],list(ties.keys())[i])
			standings.append(list(ties.values())[i][0])
	print("++++++++++++++++End Standings++++++++++++++++")
	nsource = ColumnDataSource({
		'Team': list(standings), 'Points': [points[i] for i in standings], 'Status':list(status)
	})
	table_standings.source.data = nsource.data
	# simulate playoffs 
	nresult = []
	nhome_seed = []
	naway_seed = []
	nround = []
	advance_to_second_round = []
	t1 = standings[0]
	t2 = standings[7]
	nhome_seed.append(t1)
	naway_seed.append(t2)
	nround.append("Quarterfinals")
	wins, loses = series_playoff(t1,t2,5,d)
	if wins == 3:
		advance_to_second_round.append(t1)
		print(t1,"wins series against ", t2,": ",wins,"-",loses)
		nresult.append("wins series ("+str(wins)+"-"+str(loses)+") against") 
	else:
		print(t2,"wins series against ", t1,": ",loses,"-",wins)
		advance_to_second_round.append(t2)	
		nresult.append("loses series ("+str(wins)+"-"+str(loses)+") against") 
	
	t1 = standings[1]
	t2 = standings[6]
	nhome_seed.append(t1)
	naway_seed.append(t2)
	nround.append("Quarterfinals")
	wins, loses = series_playoff(t1,t2,5,d)
	if wins == 3:
		advance_to_second_round.append(t1)
		print(t1,"wins series against ", t2,": ",wins,"-",loses)
		nresult.append("wins series ("+str(wins)+"-"+str(loses)+") against") 
	else:
		print(t2,"wins series against ", t1,": ",loses,"-",wins)
		advance_to_second_round.append(t2)
		nresult.append("loses series ("+str(wins)+"-"+str(loses)+") against")
	
	t1 = standings[2]
	t2 = standings[5]
	nhome_seed.append(t1)
	naway_seed.append(t2)
	nround.append("Quarterfinals")
	wins, loses = series_playoff(t1,t2,5,d)
	if wins == 3:
		advance_to_second_round.append(t1)
		print(t1,"wins series against ", t2,": ",wins,"-",loses)
		nresult.append("wins series ("+str(wins)+"-"+str(loses)+") against") 
	else:
		print(t2,"wins series against ", t1,": ",loses,"-",wins)
		advance_to_second_round.append(t2)
		nresult.append("loses series ("+str(wins)+"-"+str(loses)+") against")

	t1 = standings[3]
	t2 = standings[4]
	nhome_seed.append(t1)
	naway_seed.append(t2)
	nround.append("Quarterfinals")
	wins, loses = series_playoff(t1,t2,5,d)
	if wins == 3:
		advance_to_second_round.append(t1)
		print(t1,"wins series against ", t2,": ",wins,"-",loses)
		nresult.append("wins series ("+str(wins)+"-"+str(loses)+") against") 
	else:
		print(t2,"wins series against ", t1,": ",loses,"-",wins)
		advance_to_second_round.append(t2)
		nresult.append("loses series ("+str(wins)+"-"+str(loses)+") against")

	nhome_seed.append("-----")
	naway_seed.append("-----")
	nround.append("-----")
	nresult.append("-----")
	# semis
	advance_to_finals = []
	small_finals = []
	t1 = advance_to_second_round[0]
	t2 = advance_to_second_round[3]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_second_round[3]
		t2 = advance_to_second_round[0]
	nround.append("Semifinals")
	if np.random.normal(d[t1]-d[t2],12) > 0:
		advance_to_finals.append(t1)
		nresult.append("advances to final over")
		print(t1,"advances to final over ", t2)
		nhome_seed.append(t1)
		naway_seed.append(t2)
	else:
		advance_to_finals.append(t2)
		nresult.append("advances to final over")
		print(t2,"advances to final over ", t1)
		naway_seed.append(t1)
		nhome_seed.append(t2)

	t1 = advance_to_second_round[1]
	t2 = advance_to_second_round[2]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_second_round[2]
		t2 = advance_to_second_round[1]
	nround.append("Semifinals")
	if np.random.normal(d[t1]-d[t2],12) > 0:
		advance_to_finals.append(t1)
		nresult.append("advances to final over")
		print(t1,"advances to final over ", t2)
		nhome_seed.append(t1)
		naway_seed.append(t2)
	else:
		advance_to_finals.append(t2)
		nresult.append("advances to final over")
		print(t2,"advances to final over ", t1)
		naway_seed.append(t1)
		nhome_seed.append(t2)

	nhome_seed.append("-----")
	naway_seed.append("-----")
	nround.append("-----")
	nresult.append("-----")
	# finals
	t1 = advance_to_finals[1]
	t2 = advance_to_finals[0]
	if standings.index(t1) > standings.index(t2):
		t1 = advance_to_finals[0]
		t2 = advance_to_finals[1]
	nround.append("Finals")
	if np.random.normal(d[t1]-d[t2],12) > 0:
		print(t1,"wins final ", t2)
		nresult.append("wins EL final against")
		nhome_seed.append(t1)
		naway_seed.append(t2)
	else:
		print(t2,"wins final ", t1)
		nresult.append("wins EL final against")
		nhome_seed.append(t2)
		naway_seed.append(t1)

	nsource_playoffs = ColumnDataSource({
		'Team 1': list(nhome_seed), 'result': list(nresult) ,'Team 2': list(naway_seed), 'Round': list(nround)
        })
	table_playoffs.source.data = nsource_playoffs.data

##### load ##### 

d = a1_rtgs.bball_ratings("results.csv")
print(d)

global status

teams = ['Anadolu Efes','FC Barcelona','Real Madrid','CSKA Moscow','Maccabi FOX Tel Aviv','Panathinaikos OPAP','Fenerbahçe Beko','Khimki','Valencia Basket','AX Armani Exchange Olimpia','Olympiacos','Žalgiris','Kirolbet Baskonia','Crvena zvezda mts','LDLC ASVEL','Alba Berlin','Zenit Saint Petersburg','Bayern Munich']
points = [52,50,50,47,47,42,41,41,40,40,40,40,40,39,38,37,36,36]
status = ['Playoffs' for _ in range(8)] + [' ' for _ in range(10)] 

source = ColumnDataSource({
	'Team': list(teams), 'Points': list(points), 'Status':list(status)
})

columns = [TableColumn(field="Team", title="Team"),
           TableColumn(field="Points",title="Points"),
	   TableColumn(field="Status",title="Status")]

table_standings = DataTable(source=source, columns=columns, editable=True, height=400)

home_seeds = [teams[0],teams[1],teams[2],teams[3],"-----","TBA","TBA","-----","TBA"]
away_seeds = [teams[7],teams[6],teams[5],teams[4],"-----","TBA","TBA","-----","TBA"]
round_play = ["Quarterfinals","Quarterfinals","Quarterfinals","Quarterfinals","-----","Semifinals","Semifinals","-----","Finals"]
result = ["?" for _ in range(len(home_seeds))]

source_playoffs = ColumnDataSource({
	'Team 1': list(home_seeds), 'result': list(result) ,'Team 2': list(away_seeds), 'Round': list(round_play)
})

columns_playoffs = [TableColumn(field="Team 1", title="Team 1"),
		    TableColumn(field="result", title="Result"),
           	    TableColumn(field="Team 2",title="Team 2"),
           	    TableColumn(field="Round",title="Round")]

table_playoffs = DataTable(source=source_playoffs, columns=columns_playoffs, editable=True, height=450)

#############################
logo = imread("el.png")
## there is a bug in bokeh image_rgba to be used later that requires the following flipping
## https://github.com/bokeh/bokeh/issues/1666
logo = logo[::-1]
plogo = figure(x_range=(0,25),y_range=(0,15), tools = [], plot_width=333,plot_height=250)
plogo.xgrid.grid_line_color = None
plogo.ygrid.grid_line_color = None
plogo.image_rgba(image=[logo],x=[0], y=[0], dw = [25], dh = [15])
plogo.xaxis.visible = False
plogo.yaxis.visible = False

div1 = Div(text="""<font size=6><b><h>EuroLeague in a Spreadsheet</b></h></font></br></br><font size=5>With COVID-19 hitting sports hard - just as with everything else - spreadsheets finally get the position they deserve in sports. Euroleague was suspended before the regular season ended. Simulate the rest of the regular season and the playoffs to get your sports fix <br><br>Basketball Guru (@wiseballsguru), K. Pelechrinis (@kpelechrinis). </font><br></br></br><br></br></br>""",width=800, height=250)

button = Button(label="Simulate", button_type = "success", width = 250)
button.on_click(sim_callback)

div2 = Div(text="""""",width = 350)
div3 = Div(text="""""",width = 100)

#layout = layout([[div1,],[button,],[table_standings,table_playoffs]])
layout = (column(row(div1,div3,plogo),row(button),row(table_standings,div2,table_playoffs)))
curdoc().add_root(layout)
