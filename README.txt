Scraper built by Muneeb Alam in 2012 for Columbia Daily Spectator

Upadated by Hari D.
Restored funcationality, added 2014-2016 seasons and womens teams

Currently only grabs data for Columbia Men's and Women's basketball teams
If you want to restore functionality for all Ivys, ctrl+f the line "for team in teamids:" and delete the two lines below it that should say:
"
if team != 'Columbia':
	continue
"
Then run the program for your desired year and gender.
Note: I did this because NCAA has multiple ways of writing some people's names, which causes an error to be thrown. To save myself time and the program some memory, I only hard coded the names of the students from Columbia so their stats would be accurate.


	Before running:
	- Make sure python is installed
	- Make sure mechanize, cookielib, urlib and urllib2 are installed

	To run:
	- add this program you desired directory
	- in that same directory, create folder bball
	- go to terminal (MAC) or command prompt (Windows) and run python bballstats.py