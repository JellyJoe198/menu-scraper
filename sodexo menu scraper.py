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

import sys

true = True
false = False

print(sys.argv)
SKIP_ASK = ("-skip" in sys.argv)
ARG_FILTER = ("-filter" in sys.argv)

##URL = "https://realpython.github.io/fake-jobs/"
URL = "https://menus.sodexomyway.com/BiteMenu/Menu?menuId=14978&locationId=75204001&whereami=http://minesdining.sodexomyway.com/dining-near-me/mines-market"
print( "getting website data..." )
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

days = soup.find_all("div", class_="bite-day-menu")


## level definitions:
##  Time block {lunch, dinner, etc}
##  Location {grillworks, Simple Servings, noodles, etc}
##  Item {french fries, grilled cheese; chicken, rice, broccoli}

def intAsk(query, inadd = " (1/0)"):
    ## ask user and return integer value of the response
    ## '0'+input prevents error by making it default to 0
    return  int('0'+input(query + inadd) )

while True: ## repeat parsing unless break
    
    today = dt.date.today()        
    weekday = (today.weekday() +1) %7 #today.isocalendar( int(now +1) % 7 ) ##day of week, sunday = 0
    while True:
        print("using", weekday, "as today's weekday.")

        try:
            today = days[weekday] ##10/4/21: today (monday) is the second day of week shown.
        except:
            print("failed to get today's weekday.")
        ## todo: day of the month verification
        ## bug: month changes midweek? "IndexError: list index out of range"
        print( "Today is", today.get("id") ,end=". ")
        if SKIP_ASK or intAsk("Is this correct?"):
            break ## if user allows, continue program, otherwise change day.
        else:
            ## set day of week to user set value
            weekday = intAsk("what day of the week is it? (assuming Sun=0) ", '') # %7

    doFilter = true
    allowedLocations = ["GRILL", "SIMPLE", "NOOD", "SOUP"] ## TITLES allowed in filter. must be ALLCAPS
    if not ARG_FILTER:
        print("default locations are ", allowedLocations)
        doFilter = intAsk("Filter to only these locations?")

    ## all times blocks in today's menu
    today_time_blocks = today.find_all( "div", class_="accordion-block" )
    for time_block in today_time_blocks:
        print('\n')
        title = time_block.find( "span", class_="accordion-copy" )
        print( title.text ,end="\n--------------------\n" ) # title of this time block, with a line for accent

        ## for each location header in this time block
        locations = time_block.find_all( "h5" )
        for lotion in locations:
            ## verify that location is allowed
            if doFilter:
                found = False;
                for allowedLocation in allowedLocations:
##                    print( allowedLocation, lotion.text )
                    if (lotion.text.find( allowedLocation ) != -1):
                        found = True
##                        print("found")
                        break #stop checking, we already found a match
                
                if not found:
##                    print ("not allowed")
                    continue ## stop running this location ## don't print things that aren't in allowed list

            ## print items
            print('\n', lotion.text ) ## location TITLE
            sector = lotion.find_next( "ul", class_="bite-menu-item" )
            items = sector( "div", class_="col-xs-9" ) # every menu item is in this same div class
            for item in items:
                print( item.find("a").text )

    result = intAsk("\n\nrun again without reload?")
    if ( result == 0 ):
        break ## if user inputs 0, end program, otherwise restart parsing
    elif result == 1:
        ARG_FILTER = false
        SKIP_ASK = false
        print ("\n"*5) ## whitespace for staying pretty
    else:
        print ("\n"*5)

