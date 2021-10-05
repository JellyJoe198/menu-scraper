## menu scraper for Mines Sodexo website
## Author: Joseph Brownlee (JellyJoe198)
##
## Based on: https://realpython.com/beautiful-soup-web-scraper-python
##
## This program gets the html of the menu from the internet, then parses it
## in a way to extract the relevant info (titles, menu items, etc)

import requests
import time
import datetime as dt
from bs4 import BeautifulSoup

##URL = "https://realpython.github.io/fake-jobs/"
URL = "https://menus.sodexomyway.com/BiteMenu/Menu?menuId=14978&locationId=75204001&whereami=http://minesdining.sodexomyway.com/dining-near-me/mines-market"
print( "getting website data..." )
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

days = soup.find_all("div", class_="bite-day-menu")

while True: ## repeat parsing unless break
    
    today = dt.date.today()        
    weekday = (today.weekday() +1) %7
    while True:
        print("using", weekday, "as today's weekday.")
        today = days[weekday]
        ## todo: day of the month verification
        print( "Today is", today.get("id") ,end='')
        if int('0'+input(". Is this correct? (1/0)") ):
            break ## if user allows, continue program, otherwise change day.
        else:
            ## '0'+input prevents error by making it default to 0
            weekday = int( '0'+input("what day of the week is it? (assuming Sun=0) ") )

    today_time_blocks = today.find_all( "div", class_="accordion-block" )
    for time_block in today_time_blocks:
        print('\n')
        title = time_block.find( "span", class_="accordion-copy" )
        print( title.text ,end="\n--------------------\n" ) # title of this time block, with a line for accent

        locations = time_block.find_all( "h5" )
        for lotion in locations:
            print()
            print( lotion.text )
            sector = lotion.find_next( "ul", class_="bite-menu-item" )
            items = sector( "div", class_="col-xs-9" ) # every menu item is in this same div class
            for item in items:
                print( item.find("a").text )


    if ( int('0'+input("\n\nrun again without reload? (1/0)")) == 0 ):
        break ## if user inputs 0, end program, otherwise restart parsing
    else:
        print ("\n"*5)
        ## go back to start of while loop

