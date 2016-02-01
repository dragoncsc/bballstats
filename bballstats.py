'''
	Hari D:
	- Need to install mechanize and cookie lib for program to work
	- trying to take out all urllibs
	- Added recent seasons, gender and error file for names that have to be reformated
		to be found in roster

	To run:
	- add this program you desired directory
	- in that same directory, create folder bball
	- go to terminal (MAC) or command prompt (Windows) and run python bballstats.py

	takes about 23m42.415s with a 1 second delay (and no 404s)
'''


import urllib
import urllib2
import mechanize
import cookielib
import sys
import time


'''
	Hari D:
	Dummy reader class to take in an html page and mimic urllib functionality
	this is so that I don't have to change a bunch of lines of code
	where the readline() functionality is used. it's also marginally faster

	For error checking purposes, I store the current html page. If the program
	errors out and crashes, check the sampleHTML.txt
'''

class reader():

	def __init__(self, html):
		self.str = html
		self.list_o_url = html.split('\n')
		f = open('sampleHTML.txt', 'w')
		f.write(html)

	# Remember to read from the TOP of the webpage
	def readline(self):
		return self.list_o_url.pop(0)

	def close(self):
		return

'''
	Function built to encapsulate all the characteristics of a browser so that
	website doesn't think we're a bot
	it also hides all the annoyance of accessing the webpage
	Script keeps getting banned (403 Access denied error), so I have to introduce
	a delay every time the bot wants to access the site

'''
def build_browser_reader( url ):
	time.sleep( .60 )
	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	# Follows refresh 0 but not hangs on refresh > 0
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	# Debugging messages
	#br.set_debug_http(True)
	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)

	# User-Agent (this entails pretending to be a browser)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	# Go through process of actually opening the webpage
	r = br.open( url )
	html = r.read()

	return reader( html )





name_errors = open( 'name_errors.txt', 'w' )
data = []
databygame = {}
ivies = ['Brown','Columbia','Cornell','Dartmouth','Harvard','Penn','Princeton','Yale']
#seasontouse = '2013'
#folder = '/Users/muneebalam/Desktop/Python/bball/'
folder = "bball/"
d3s = ['Haverford','Swarthmore','MIT','Baruch','Albertus Magnus','Oberlin','Daniel Webster','Old Westbury','New Jersey','Lyndon St.','Lesley','Colby-Sawyer']

def printdata(team, season, gender):
	writer = open(folder+team+' '+season + ' '+gender.lower()+' data.txt','w')
	for entry in data:
		if team in entry:
			writer.write("\t".join(entry)+'\n')
	writer.close()

def getHomeTeam(line):
	return line[0]

def getRoadTeam(line):
	return line[1]

def getTime(line):
	return line[2]

def getActingTeam(line):
	try:
		return line[3]
	except IndexError:
		print line

def getScore(line):
	return line[4]

def getHomeScore(line):
	return int(line[4][line[4].index('-')+1:])

def getRoadScore(line):
	return int(line[4][:line[4].index('-')])

def getActingPlayer(line):
	return line[5]

def getEvent(line):
	return line[6]

def getHomePlayers(line):
	return line[7:12]

def getRoadPlayers(line):
	return line[-5:]

def getIvyPlayers(line):
	if getHomeTeam(line) in ivies:
		return getHomePlayers(line)
	else:
		return getRoadPlayers(line)

def getPlayers(line, team='both'):
	if team == 'both':
		return line[7:]
	elif getHomeTeam(line) == team:
		return getHomePlayers(line)
	else:
		return getRoadPlayers(line)

def hometeamaction(str1,str2,str3,str4):
	if '></td>' not in str2 and len(str2)>1:
		return False
	return True

def getPlayer(stri):
	if ',' in stri:
		comma = stri.index(',')
		if ' ' != stri[comma+1]:
			stri = stri[:comma]+', '+stri[comma+1:]
	descrip = stri.split(" ")
	try:
		descrip[0] = descrip[0][0].upper()+descrip[0][1:-1].lower()
		descrip[1] = descrip[1][0].upper()+descrip[1][1:].lower()
	except IndexError:
		print stri
	attempt = descrip[1]+' '+descrip[0]
	if attempt == 'Tavon Blackman':
		return 'Tavon Blackmon'
	elif attempt == 'Alex Barlow':
		return 'Alexander Barlow'
	elif attempt == 'Dj Newbill':
		return 'D.j. Newbill'
	elif attempt == 'Tj Bray':
		return 'T.j. Bray'
	elif attempt == 'Tj Curry':
		return 'T.j. Curry'
	elif attempt == 'Cj Fair':
		return 'C.j. Fair'
	elif attempt == 'Jj Moore':
		return 'J.j. Moore'
	elif attempt == 'Tj Williams':
		return 'T.j. Williams'
	elif attempt == 'Dj Irving':
		return 'D.j. Irving'
	elif attempt == 'Jakob Gollon':
		return 'Jake Gollon'
	elif attempt == 'Miles Cartwright':
		return 'Miles Jackson-cartwright'
	elif attempt == 'Jr., White':
		return 'Anthony White'
	elif attempt == 'Ii, Moor':
		return 'Yolonzo Moore'
	elif attempt == 'Yolonzo Ii':
		return 'Yolonzo Moore'
	elif attempt == 'Joe Edwards':
		return 'Joseph Edwards'
	elif attempt == 'Iii, Montgomer':
		return 'James Montgomery'
	elif attempt == 'Luke Mccomber':
		return 'Chris Mccomber'
	elif attempt == 'Longji Yiljep':
		return 'Lonji Yiljep'
	elif attempt == 'Branden Frazier':
		return 'Brandon Frazier'
	elif attempt == 'Cj Garner':
		return 'C.j. Garner'
	elif attempt == 'Cj Aike':
		return 'C.j. Aiken'
	elif attempt == 'Dj Stephens':
		return 'D.j. Stephens'
	elif attempt == 'M Carter-williams':
		return 'Michael Carter-williams'
	elif attempt == 'Brtandon Mcdonnell':
		return 'Brandon Mcdonnell'
	elif attempt == 'Iii, Walke':
		return 'James Walker'
	elif attempt == 'Khalif Wyatt':
		return 'Khaliff Wyatt'
	elif attempt == 'Joe Thomas':
		return 'Joseph Thomas'
	elif attempt == 'Iv, Green':
		return 'Phil Greene'
	elif attempt == 'Damo Sherman-newsome':
		return 'Damon Sherman-newsome'
	elif attempt == 'Cj Mccollum':
		return 'C.j. Mccollum'
	elif attempt == 'Alex Klein':
		return 'Alexandria Klein'
	elif attempt == 'Asia Mitchell-owens':
		return 'Asia Mitchell'
	elif attempt == 'Jay Bravo-harriott':
		return 'Jay-ann Bravo-harriott'	
	elif attempt == 'Paulina Korner':
		return 'Paulina K\xc3\xb6rner'	
	elif attempt == 'Shanice Vaughan':
		return 'Shanice Vaughn'
	elif attempt == 'Gunnar Olafsson':
		return 'Gunnar Olaffson'
	elif attempt == 'M Conyers-jordan':
		return 'Maria Conyers-jordan'	


	return attempt

def readSeasonData(season):
	teamids = {}
	teamids['Brown'] = 80
	teamids['Columbia']=158
	teamids['Cornell']=167
	teamids['Dartmouth']=172
	teamids['Harvard']=275
	teamids['Penn']=540
	teamids['Princeton']=554
	teamids['Yale']=813
	print 'Do you want statistics for men or women?'
	gender = raw_input()
	if gender.lower() == 'men':
		seasonid = {'2013':'11540','2012':'11220', '2014': '12020', '2015':'12260'}
	elif gender.lower() == 'women':
		seasonid = {'2013':'11560','2012':'11240', '2014': '12021', '2015':'12280'}
	else:
		print 'Could not identify gender. We don\'t have gender fluid teams. YET.'
		sys.exit()
	if season not in seasonid:
		print 'Given season not found'
		sys.exit()
	for team in teamids:
		if team != 'Columbia':
			continue
		'''
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		reader = opener.open( 'http://stats.ncaa.org/team/index/'+seasonid[season]+'?org_id='+str(teamids[team]) )
		'''
		reader = build_browser_reader( 'http://stats.ncaa.org/team/index/'+seasonid[str(season)]+'?org_id='+str(teamids[team]) )
		print 'accessed site for '+team
		line = reader.readline()


		while 'Opponent' not in line:
			line = reader.readline()
			#print '\nPrinting line: \n'
		#print '\n\n' + line + '\n\n' + str(len(reader.list_o_url)) + '\n\n'
		while True:
			line = reader.readline()
			#print '\nPrinting line: \n'
			#print line
			if '</table>' in line:
				break
			elif '/game/index/' in line:
				pds = 2
				if 'OT)' in line:
					pds += int(line[line.index('OT)')-1])
				line = line[line.index('/game/index/')+6:]
				line = line[line.index('/'):line.index('?')]
				gameurl = 'http://stats.ncaa.org/game/play_by_play'+line
				readGameData(gameurl, pds)
		print 'Done with '+team
		printdata(team, season, gender)

def getHomeStarters(url, half):
	#http://stats.ncaa.org/game/play_by_play/2698673
	#http://stats.ncaa.org/game/box_score/2698673?period_no=1
	
	start = []
	'''
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	print '\n\n '+ url[:27]+'box_score'+url[39:]+'?period_no='+str(half) + '\n\n'
	reader = opener.open( url[:27]+'box_score'+url[39:]+'?period_no='+str(half) )
	line = reader.readline()
	'''
	reader = build_browser_reader( url[:27]+'box_score'+url[39:]+'?period_no='+str(half) )
	line  = reader.readline()

	if url == 'http://stats.ncaa.org/game/play_by_play/1389834':
		if half==1:
			return ['Juhreece Thompson','Travis Payton','Byron Randle','Reggie Fondren','Eric Milam']
		else:
			return ['Juhreece Thompson','Travis Payton','Tanner Hazelbaker','Reggie Fondren','Eric Milam']
	for i in range(2):
		while '>3FG<' not in line:
			line = reader.readline()
		line = reader.readline()

	for i in range(5):
		while '/player?game_sport_year_ctl_id=' not in line:
			line = reader.readline()
		line = line[line.index('>')+1:]
		line = line[:line.index('<')]
		start.append(getPlayer(line))
		line = reader.readline()
	#print start
	reader.close()
	return start

def getRoadStarters(url, half):
	start = []

	'''
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	reader = opener.open( url[:27]+'box_score'+url[39:]+'?period_no='+str(half) )
	'''
	reader = build_browser_reader( url[:27]+'box_score'+url[39:]+'?period_no='+str(half) )

	line = reader.readline()

	if url == 'http://stats.ncaa.org/game/play_by_play/1389834':
		return ['Brian Barbour','Grant Mullins','Alex Rosenberg','Cory Osetkowski','Mark Cisco']
	while '>3FG<' not in line:
		line = reader.readline()
	for i in range(5):
		while '/player?game_sport_year_ctl_id=' not in line:
			line = reader.readline()
		line = line[line.index('>')+1:]
		line = line[:line.index('<')]
		start.append(getPlayer(line))
		line = reader.readline()

	reader.close()
	return start

def readPlayerEvent(line):
	#return player,event
	if ',' in line:
		comma = line.index(',')
		if ' ' != line[comma+1]:
			line = line[:comma]+', '+line[comma+1:]
		while line.index(' ') < comma:
			space = line.index(' ')
			line = line[:space]+line[space+1:]
			comma = line.index(',')
	descrip = line.split(" ")
	try:
		player = descrip[0]+" "+descrip[1]
	except IndexError:
		print 'index error '+str(descrip)+" "+line
		return ['sub','sub']
	if 'Turnover' in line:
		return [getPlayer(player),descrip[-1]]
	elif 'Foul' in line:
		return [getPlayer(player),descrip[-1]]
	elif 'Jumper' in line:
		try:
			return [getPlayer(player),descrip[2]+" "+descrip[-3]]
		except IndexError:
			print line
	elif 'Rebound' in line:
		if 'TEAM' in line or 'TM' in line:
			return [descrip[0], descrip[1]+' '+descrip[2]]
		else:
			try:
				return [getPlayer(player),descrip[2]+' '+descrip[3]]
			except IndexError:
				print 'index error getting player/event for: ' + line
	elif 'Layup' in line:
		return [getPlayer(player),descrip[2]+" "+descrip[3]]
	elif 'Dunk' in line:
		return [getPlayer(player),descrip[2]+" "+descrip[3]]
	elif 'Tip' in line:
		return [getPlayer(player),descrip[2]+" "+descrip[3]+" "+descrip[4]]
	elif 'Steal' in line:
		try:
			return [getPlayer(player),descrip[2]]
		except IndexError:
			print line
	elif 'Assist' in line:
		try:
			return [getPlayer(player),descrip[2]]
		except IndexError:
			print line
	elif 'Blocked Shot' in line:
		return [getPlayer(player),'Block']
	elif 'Free Throw' in line:
		return [getPlayer(player),descrip[2]+' FT']
	elif 'Timeout' in line:
		return ['','Timeout']
	else:
		return ['','']	

def readEvent(str1,str2,str3,str4,homename,roadname):
	data = []
	data.append(str1)
	if hometeamaction(str1,str2,str3,str4):
		data.append(homename)
		event = readPlayerEvent(str4)
	else:
		data.append(roadname)
		event = readPlayerEvent(str2)
	if event == None:
		return None
	data.append(str3)
	data.append(event[0])
	data.append(event[1])
	return data

def readGameData(url, pds):
	#print url
	'''
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	reader = opener.open( url )
	'''
	reader = build_browser_reader( url )
	#sys.exit()
	line = reader.readline()
	while 'Time' not in line:
		line = reader.readline()
		if 'getTime()' in line or 'Time of Game' in line:
			line = reader.readline()
	line = reader.readline()

	try:
		line = line[line.index('>')+1:]
	except:
		print '\n\n Error from here: ', line, '\n\n'
		print url
		sys.exit()
	try:
		roadteam = line[:line.index('<')]
	except:
		print "\n\nError from here (roadteam):\n\n"

		for line in reader.list_o_url[:30]:
			print line
		print '\n\nline 458\n\n'
		sys.exit()
	if roadteam in d3s:
		print roadteam+' is a D-III school. Skipping.'
		return
	
	line = reader.readline()
	line = reader.readline()
	line = line[line.index('>')+1:]
	hometeam = line[:line.index('<')]
	if hometeam in d3s:
		print hometeam+' is a D-III school. Skipping.'
		return

	print 'Reading ' + roadteam + ' at ' + hometeam + ' ' + url
	try:
		homeplayers = getHomeStarters(url,1)
		roadplayers = getRoadStarters(url,1)
	except:
		print '403 Access Denied'
		return
	count = 1

	numlines = 1

	while True:
		if '</table>' in line:
			if count < pds:
				while 'Time' not in line:
					line = reader.readline()
				homeplayers = getHomeStarters(url,2)
				roadplayers = getRoadStarters(url,2)
				count += 1
			else:
				break
		elif '<tr>' in line:
			line = reader.readline()
			line = line[line.index('>')+1:]
			line1 = line[:line.index('<')]

			line = reader.readline()
			line = line[line.index('>')+1:]
			if '<b>' in line:
				line = line[line.index('<b>')+3:]
			line2 = line[:line.index('<')]

			line = reader.readline()
			line = line[line.index('>')+1:]
			line3 = line[:line.index('<')]

			line = reader.readline()
			line = line[line.index('>')+1:]
			if '<b>' in line:
				line = line[line.index('<b>')+3:]
			line4 = line[:line.index('<')]

			numlines += 4

			if 'Enters Game' in line4:
				if hometeamaction(line1,line2,line3,line4):
					#print line4
					#sys.exit()
					homeplayers.append(getPlayer(line4))
				else:
					roadplayers.append(getPlayer(line2))
			elif 'Leaves Game' in line4:
				try:
					if hometeamaction(line1,line2,line3,line4):
						homeplayers.remove(getPlayer(line4))
					else:
						roadplayers.remove(getPlayer(line2))
				except ValueError:
					if roadteam == 'Binghamton' and hometeam=='Brown':
						homeplayers.remove('Tavon Blackmon')
					else:
						print 'Could not find ' + getPlayer(line4)+' in ' + str(homeplayers)
						name_errors.write( 'Could not find ' + getPlayer(line4)+' in ' + str(homeplayers)+'\n' )


			else:
				event = readEvent(line1,line2,line3,line4, hometeam,roadteam)
				if event == None:
					print 'NCAA Website had \'null\' instead of name. Skipping event.'
					continue
				if 'sub' not in event[3] and len(event[3])>1:
					temp = [hometeam,roadteam]
					for pt in event:
						temp.append(pt)
					for p in homeplayers:
						temp.append(p)
					for p in roadplayers:
						temp.append(p)
					data.append(temp)
			
		else:
			line = reader.readline()
			numlines += 1
			if numlines > 10000:
				break
	
	reader.close()
	print 'Done with ' + roadteam + ' at ' + hometeam

def isFGA(event):
	if 'Layup' in event:
		return True
	if 'Two' in event:
		return True
	if 'Three' in event:
		return True
	if 'Dunk' in event:
		return True
	if 'Tip' in event:
		return True
	return False

def getPts(event):
	if 'made' in event:
		if 'Layup' in event:
			return 2
		elif 'Two' in event:
			return 2
		elif 'Dunk' in event:
			return 2
		elif 'Tip' in event:
			return 2
		elif 'Three' in event:
			return 3
		else:
			return 1
	return 0

def possest(fga,orbd,to,fta):
	return fga-orbd+to+.475*fta

def points_per_poss(pts,fga,orbd,to,fta):
	return 100*float(pts)/float(possest(fga,orbd,to,fta))

def load_data(team, season, gender):
	reader = open(folder+team+' '+season+ ' ' +gender+' data.txt','r')
	info = reader.read().split('\n')
	info2 = []
	for line in info[:-1]:
		info2.append(line.split('\t'))
	reader.close()
	return info2

def getPlayerList(info, team):
	plist = []
	for event in info:
		for player in getPlayers(event, team):
			if player not in plist:
				plist.append(player)
	return sorted(plist)

def getPPPData(team, info, players, fora, opps = []):
	fga = 0
	orbd = 0
	to = 0
	fta = 0
	pts = 0
	threes = 0
	twos = 0
	drbdag = 0
	allplayers = False
	if players[0]=='all':
		allplayers = True
	for entry in info:
		cont = (getActingTeam(entry) == team) == (fora == 'for')
		gotallplayers = True
		if not allplayers:
			for pl in players:
				if pl not in entry:
					gotallplayers = False
		for pl in opps:
			if pl in entry:
				gotallplayers = False
		if cont and gotallplayers:
			if isFGA(getEvent(entry)):
				fga += 1
				if 'made Two' in getEvent(entry):
					twos += 1
				elif 'made Dunk' in getEvent(entry):
					twos += 1
				elif 'made Layup' in getEvent(entry):
					twos += 1
				elif 'made Tip' in getEvent(entry):
					twos += 1
				elif 'made Three' in getEvent(entry):
					threes += 1
			elif 'Offensive Rebound' in getEvent(entry):
				orbd += 1
			elif 'Turnover' in getEvent(entry):
				to += 1
			elif 'FT' in getEvent(entry):
				fta += 1
			pts += getPts(getEvent(entry))
		elif gotallplayers and not cont:
			if 'Defensive Rebound' in getEvent(entry):
				drbdag += 1
	return [pts, fga, orbd, to, fta, twos, threes, drbdag]

def printheader():
	print '\tPts\tFGA\tOff Rbd\tTO\tFTA\t2FGM\t3FGM\tOppDRbd\tPoss (est)\teFG%\tTOV%\tFTA/FGA\tORbd%\tPts/poss'

def printteam(inddata,inddata2,woind,woind2,inddataag,inddata2ag,woindag,woind2ag):

	pppind = points_per_poss(float(inddata[0]) , float(inddata[1]) , float(inddata[2]) ,float(inddata[3]) ,float(inddata[4]) )

	pppindag = points_per_poss( float(inddataag[0]) , float(inddataag[1]) ,float(inddataag[2]) , float(inddataag[3]) , float(inddataag[4]) )

	printheader()

	print 'Off\t'+'\t'.join(inddata2)+'\t'+str(round(possest( float(inddata[1]) , float(inddata[2]) , float(inddata[3]), float(inddata[4]) ),1))+'\t\t'+str(round(100*(inddata[5]+1.5*inddata[6])/inddata[1],1))+'\t'+str(round(inddata[3]*100.0/(inddata[1]+inddata[3]+.475*inddata[4]),1))+'\t'+str(round(inddata[4]*100.0/inddata[1],1))+'\t'+str(round(inddata[2]*100.0/(inddata[2]+inddata[7]),1))+'\t'+str(round(pppind,1))

	print 'Def\t'+'\t'.join(inddata2ag)+'\t'+str(round(possest( float(inddataag[1]) , float(inddataag[2]) , float(inddataag[3]) , float(inddataag[4]) ),1))+'\t\t'+str(round(100*(inddataag[5]+1.5*inddataag[6])/inddataag[1],1))+'\t'+str(round(inddataag[3]*100.0/(inddataag[1]+inddataag[3]+.475*inddataag[4]),1))+'\t'+str(round(inddataag[4]*100.0/inddataag[1],1))+'\t'+str(round(inddataag[2]*100.0/(inddataag[2]+inddataag[7]),1))+'\t'+str(round(pppindag,1))

def printind(inddata,inddata2,woind,woind2,inddataag,inddata2ag,woindag,woind2ag):
	
	try:
		pppind = points_per_poss( float( inddata[0] ) , float( inddata[1]) , float(inddata[2]) , float(inddata[3]) , float(inddata[4]) )
	except ZeroDivisionError:
		pppind = 0.0

	try:
		woindppp = points_per_poss(float(woind[0]), float(woind[1]) , float(woind[2]) , float(woind[3]), float(woind[4]))
	except ZeroDivisionError:
		woindppp = 0.0
	
	try:
		pppindag = points_per_poss( float(inddataag[0]) , float(inddataag[1]) , float(inddataag[2]) , float(inddataag[3]) , float(inddataag[4]) )
	except ZeroDivisionError:
		pppindag = 0.0
	
	try:
		woindpppag = points_per_poss( float(woindag[0]) , float(woindag[1]) , float(woindag[2]), float(woindag[3]) , float(woindag[4]) )
	except ZeroDivisionError:
		woindpppag = 0.0

	printheader()

	print 'Off\nW/\t'+'\t'.join(inddata2)+'\t'+str(round(possest(inddata[1],inddata[2],inddata[3],inddata[4]),1))+'\t\t'+str(round(100*(inddata[5]+1.5*inddata[6])/inddata[1],1))+'\t'+str(round(inddata[3]*100.0/(inddata[1]+inddata[3]+.475*inddata[4]),1))+'\t'+str(round(inddata[4]*100.0/inddata[1],1))+'\t'+str(round(inddata[2]*100.0/(inddata[2]+inddata[7]),1))+'\t'+str(round(pppind,1))

	print 'W/o\t'+'\t'.join(woind2)+'\t'+str(round(possest(woind[1],woind[2],woind[3],woind[4]),1))+'\t\t'+str(round(100*(woind[5]+1.5*woind[6])/woind[1],1))+'\t'+str(round(woind[3]*100.0/(woind[1]+woind[3]+.475*woind[4]),1))+'\t'+str(round(woind[4]*100.0/woind[1],1))+'\t'+str(round(woind[2]*100.0/(woind[2]+woind[7]),1))+'\t'+str(round(woindppp,1))

	print '\nDef\nW/\t'+'\t'.join(inddata2ag)+'\t'+str(round(possest(inddataag[1],inddataag[2],inddataag[3],inddataag[4]),1))+'\t\t'+str(round(100*(inddataag[5]+1.5*inddataag[6])/inddataag[1],1))+'\t'+str(round(inddataag[3]*100.0/(inddataag[1]+inddataag[3]+.475*inddataag[4]),1))+'\t'+str(round(inddataag[4]*100.0/inddataag[1],1))+'\t'+str(round(inddataag[2]*100.0/(inddataag[2]+inddataag[7]),1))+'\t'+str(round(pppindag,1))

	print 'W/o\t'+'\t'.join(woind2ag)+'\t'+str(round(possest(woindag[1],woindag[2],woindag[3],woindag[4]),1))+'\t\t'+str(round(100*(woindag[5]+1.5*woindag[6])/woindag[1],1))+'\t'+str(round(woindag[3]*100.0/(woindag[1]+ woindag[3]+.475* woindag[4]),1))+'\t'+str(round(woindag[4]*100.0/woindag[1],1))+'\t'+str(round(woindag[2]*100.0/(woindag[2]+ woindag[7]),1))+'\t'+str(round(woindpppag,1))+'\n'

def showplayerdata(team, info, plist, teampppdata, teampppdataag, opps=[]):
	inddata = getPPPData(team, info, plist, 'for', opps)
	inddata2 = []
	woind = []
	woind2 = []
	for num in range(len(inddata)):
		woind.append(float(teampppdata[num] - inddata[num]))
		woind2.append(str(woind[num]))
		inddata2.append(str(inddata[num]))
			
	inddataag = getPPPData(team, info, plist, 'against', opps)
	inddata2ag = []
	woindag = []
	woind2ag = []
	for num in range(len(inddataag)):
		woindag.append(float(teampppdataag[num] - inddataag[num]))
		woind2ag.append(str(woindag[num]))
		inddata2ag.append(str(inddataag[num]))
	if plist[0]=='all':
		printteam(inddata,inddata2,woind,woind2,inddataag,inddata2ag,woindag,woind2ag)
	else:
		printind(inddata,inddata2,woind,woind2,inddataag,inddata2ag,woindag,woind2ag)

def showteamdata(team, info, teampppdata, teampppdataag):
	showplayerdata(team, info, ['all'], teampppdata, teampppdataag)

def filtergames(info, start, end):

	totgms = 0
	curgame = ''
	gamenum = 0
	gamelist = []
	gamedata = []
	starti = 0
	endi = 0
	for entry in info:
		if entry[0:2] not in gamelist:
			gamelist.append(entry[0:2])
			gamedata.append([])
		gamedata[gamelist.index(entry[0:2])].append(entry)
	if end == 0:
		gamedata = gamedata[start-1:]	
	else:	
		gamedata = gamedata[start-1:end]
	glist2 = []
	for game in gamedata:
		for entry in game:
			glist2.append(entry)
	return glist2

def analysis():
	while True:
		print 'Enter team (e.g. Columbia). Leave blank to exit'
		team = raw_input()
		if len(team) < 4:
			break
		print 'Enter gender:'
		gender = raw_input()
		print gender.lower()
		if gender.lower() != 'men' and gender.lower() != 'women':
			print 'We don\'t have that gender yet, check back in a few years'
			sys.exit()
		team = team[0].upper()+team[1:].lower()
		info = load_data(team, seasontouse, gender)
		playerlist = getPlayerList(info, team)
		print 'Enter span of games separated by space (e.g. 1 3 means first, second, and third games; 1 -1 means first through penultimate, inclusive)'
		span = raw_input().split(' ')
		start = int(span[0])
		end = int(span[1])
		info2 = filtergames(info, start, end)
		teampppdata = getPPPData(team, info2,['all'], 'for')
		teampppdataag = getPPPData(team, info2,['all'], 'against')
		showteamdata(team, info2, teampppdata, teampppdataag)
		while True:
			print 'Which player(s) do you want to get a WOWY for? (Separate with tabs; leave blank to exit)'
			print 'Choose from: '+",".join(playerlist)
			plist = raw_input()
			if len(plist)<2:
				break
			plist = plist.split('\t')
			showplayerdata(team, info2, plist, teampppdata, teampppdataag)
global seasontouse
print 'Enter 1 to update data\nEnter 2 for queries'	
command = int(raw_input())
if command == 1:
	print 'Enter season (only enter the first year of the season, so 2015-2016 would be 2015):'
	seasontouse = raw_input()
	readSeasonData(seasontouse)
else:
	print 'Enter season (only enter the first year of the season, so 2015-2016 would be 2015):'
	seasontouse = raw_input()
	analysis()
	name_errors.close()



