def prototyper(b):
	a = ['status','trip','mode','belt','fire','gas','smoke'] #this one for ahu 3
	a = ['status','trip','mode']  #this one for ahu 2
	a = ['status','trip']
	a = ['on_status','flow_status','high_temp'] #this one for temp
	a = ['damper_open','damper_close'] #this one for damper and fire damper
	c = ['trigger','latch','common_alarm','status_error','trip_error','dcs_occupied'] #this one for ahu
	c = ['common_alarm','hightemp_error'] #this one for temp
	d = ['status','trip'] #this one for ahu

	for x in a:
		print(b+'_'+x+' AT%I* : BOOL;')
	print()
	for x in c:
		print(b+'_'+x+' : BOOL;') #this one for temp and ahu
	print()
	for x in d:
		print(b+'_'+x+'_Filter : ErrorFilter;') #this one for ahu
	print()
	for x in d:
		if x == 'status':
			print(b+'_'+x+'_Filter(IN:=(NOT '+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu
		else:
			print(b+'_'+x+'_Filter(IN:=('+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu

	for x in d:
		print(b+'_'+x+'_Filter(IN:=('+b+'_'+x+ '),Q=>'+b+'_'+x+'_error);') #this one for ahu no ctrl

	print(b + '_common_alarm := '+b+'_fire OR '+b+'_gas OR '+b+'_smoke OR '+b+'_status_error OR '+b+'_trip_error;')  #this one for ahu 3
	print(b + '_common_alarm := '+b+'_status_error OR '+b+'_trip_error;')  #this one for ahu 2
	print(b + '_hightemp_error := '+b+'_high_temp;') #this one for temp
	print(b + '_common_alarm := '+b+'_hightemp_error;') #this one for temp

	print()


def ahu3(b,item):
	a = ['status','trip','mode','belt','fire','gas','smoke'] #this one for ahu 3
	c = ['trigger','latch','common_alarm','status_error','trip_error','dcs_occupied'] #this one for ahu
	d = ['status','trip'] #this one for ahu

	for x in a:
		print(b+'_'+x+' AT%I* : BOOL;')
	print()
	for x in c:
		print(b+'_'+x+' : BOOL;') #this one for temp and ahu
		item.append(b+'_'+x)
	print()
	for x in d:
		print(b+'_'+x+'_Filter : ErrorFilter;') #this one for ahu
	print()
	for x in d:
		if x == 'status':
			print(b+'_'+x+'_Filter(IN:=(NOT '+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu
		else:
			print(b+'_'+x+'_Filter(IN:=('+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu

	print(b + '_common_alarm := '+b+'_fire OR '+b+'_gas OR '+b+'_smoke OR '+b+'_status_error OR '+b+'_trip_error;')  #this one for ahu 3

	print()

def ahu2(b,item):
	a = ['status','trip','mode']  #this one for ahu 2
	c = ['trigger','latch','common_alarm','status_error','trip_error','dcs_occupied'] #this one for ahu
	d = ['status','trip'] #this one for ahu

	for x in a:
		print(b+'_'+x+' AT%I* : BOOL;')
	print()
	for x in c:
		print(b+'_'+x+' : BOOL;') #this one for temp and ahu
		item.append(b+'_'+x)
	print()
	for x in d:
		print(b+'_'+x+'_Filter : ErrorFilter;') #this one for ahu
	print()
	for x in d:
		if x == 'status':
			print(b+'_'+x+'_Filter(IN:=(NOT '+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu
		else:
			print(b+'_'+x+'_Filter(IN:=('+b+'_'+x+ ' AND ' +b+'_latch),Q=>'+b+'_'+x+'_error);') #this one for ahu


	print(b + '_common_alarm := '+b+'_status_error OR '+b+'_trip_error;')  #this one for ahu 2

	print()


def temperature(b,item):
	a = ['flow_status','high_temp'] #this one for temp
	c = ['common_alarm','hightemp_error'] #this one for temp
	x = 'on_status'
	print(b+'_'+x+' : BOOL;')
	item.append(b+'_'+x)

	for x in a:
		print(b+'_'+x+' AT%I* : BOOL;')
		item.append(b+'_'+x)
	print()
	for x in c:
		print(b+'_'+x+' : BOOL;') #this one for temp and ahu
		item.append(b+'_'+x)
	print()

	print(b + '_hightemp_error := '+b+'_high_temp;') #this one for temp
	print(b + '_common_alarm := '+b+'_hightemp_error;') #this one for temp

	print()


def damper(b,item):
	a = ['damper_open','damper_close'] #this one for damper and fire damper

	for x in a:
		print(b+'_'+x+' AT%I* : BOOL;')
		item.append(b+'_'+x)
	print()



def run_ahu3():
	items = []
	s = ['common_alarm','dcs_occupied']
	for x in s:
		print(name+'_'+x+' : BOOL;')
	print()
	if len(f) == 2:
		print(name+'_dummy '+': BOOL;')
		print('FB_'+name + ': Flowchart_1_2_CTRL_2;')
	else:
		print('FB_'+name + ': Flowchart_1_2_CTRL;')
	print()
	for x in f:
		item = []
		b = name +'_' + str(x)
		ahu3(b,item)
		items.append(item)
	print()
	if len(items) == 3:
		print(name+'_common_alarm := '+ items[0][2] +' OR '+ items[1][2]+' OR '+ items[2][2] + ';')
		print(name+'_dcs_occupied := '+ items[0][5] +' OR '+ items[1][5]+' OR '+ items[2][5] + ';')
	else:
		print(name+'_common_alarm := '+ items[0][2] +' OR '+ items[1][2]+';')
		print(name+'_dcs_occupied := '+ items[0][5] +' OR '+ items[1][5]+';')

	print();

	w = '''	{0}(
	ON1:={1} ,
	ON2:={2} ,
	ON3:={3} ,
	status_error_1:= {4},
	status_error_2:={5} ,
	status_error_3:={6} ,
	trip_error_1:={7} ,
	trip_error_2:={8} ,
	trip_error_3:={9} ,
	Latch1:={10} ,
	Latch2:={11} ,
	Latch3:={12} ,
	DcsOccupied_1=>{13} ,
	DcsOccupied_2=>{14} ,
	DcsOccupied_3=>{15} );'''

	if len(items) == 3:
		print(w.format('FB_'+name,items[0][0],items[1][0],items[2][0],items[0][3],items[1][3],items[2][3],items[0][4],items[1][4],items[2][4],items[0][1],items[1][1],items[2][1],items[0][5],items[1][5],items[2][5]))
	else:
		print(w.format('FB_'+name,items[0][0],items[1][0],'FALSE',items[0][3],items[1][3],'FALSE',items[0][4],items[1][4],'FALSE',items[0][1],items[1][1],(name+'_dummy'),items[0][5],items[1][5],''))


def run_ahu2():
	items = []
	s = ['common_alarm','dcs_occupied']
	for x in s:
		print(name+'_'+x+' : BOOL;')
	print()
	if len(f) == 2:
		print(name+'_dummy '+': BOOL;')
		print('FB_'+name + ': Flowchart_1_2_CTRL_2;')
	else:
		print('FB_'+name + ': Flowchart_1_2_CTRL;')

	print()
	for x in f:
		item = []
		b = name +'_' + str(x)
		ahu2(b,item)
		items.append(item)
	print()
	if len(items) == 3:
		print(name+'_common_alarm := '+ items[0][2] +' OR '+ items[1][2]+' OR '+ items[2][2] + ';')
		print(name+'_dcs_occupied := '+ items[0][5] +' OR '+ items[1][5]+' OR '+ items[2][5] + ';')
	else:
		print(name+'_common_alarm := '+ items[0][2] +' OR '+ items[1][2]+ ';')
		print(name+'_dcs_occupied := '+ items[0][5] +' OR '+ items[1][5]+ ';')


	print();

	w = '''	{0}(
	ON1:={1} ,
	ON2:={2} ,
	ON3:={3} ,
	status_error_1:= {4},
	status_error_2:={5} ,
	status_error_3:={6} ,
	trip_error_1:={7} ,
	trip_error_2:={8} ,
	trip_error_3:={9} ,
	Latch1:={10} ,
	Latch2:={11} ,
	Latch3:={12} ,
	DcsOccupied_1=>{13} ,
	DcsOccupied_2=>{14} ,
	DcsOccupied_3=>{15} );'''

	if len(items) == 3:
		print(w.format('FB_'+name,items[0][0],items[1][0],items[2][0],items[0][3],items[1][3],items[2][3],items[0][4],items[1][4],items[2][4],items[0][1],items[1][1],items[2][1],items[0][5],items[1][5],items[2][5]))
	else:
		print(w.format('FB_'+name,items[0][0],items[1][0],'FALSE',items[0][3],items[1][3],'FALSE',items[0][4],items[1][4],'FALSE',items[0][1],items[1][1],(name+'_dummy'),items[0][5],items[1][5],''))


def run_temperature():
	for x in f:
		item = []
		b = name +'_' + str(x)
		print('FB_'+ b + ': Flowchart_5_6;')
		temperature(b,item)
		w = '''{0}(on_status:= {1} , flow_status:= {2} , high_temp:= {3});'''
		print(w.format('FB_'+b,item[0],item[1],item[2]))
		print()
		print()



def run_damper():
	for x in f:
		item = []
		b = name +'_' + str(x)
		damper(b,item)


def run_fan():
	items = []
	if len(f) != 1:
		s = ['common_alarm','dcs_occupied']
		for x in s:
			print(name+'_'+x+' : BOOL;')
		print()
	for x in f:
		item = []
		b = name +'_' + str(x)
		# s = ['common_alarm','dcs_occupied']
		# for x in s:
		# 	print(b+'_'+x+' : BOOL;')
		print()
		print('FB_'+ b + ': Flowchart_7;')
		print()
		ahu2(b,item)
		items.append(item)
		print()

		w = '''{0}(
Trigger:={1} ,
Latch:={2} ,
DCS_Occupied=>{3} );'''

		print(w.format('FB_'+ b,item[0],item[1],item[5]))
		print()
		print()

	if len(f) != 1:
		alm = (name + '_common_alarm:=')
		for x in items:
			alm = alm + x[2] + ' OR '
		alm = alm[:-4]
		alm = alm + ';'
		print(alm);

		alm = (name + '_dcs_occupied:=')
		for x in items:
			alm = alm + x[5] + ' OR '
		alm = alm[:-4]
		alm = alm + ';'
		print(alm);

	print()





name = 'AHU_MSB'
#f = range(1,2)
#f = ['3A','3B']
#f = ['01E','01F']
f = ['1A','1B','1C']
run_ahu3()

