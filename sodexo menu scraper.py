## menu scraper for Mines Sodexo website
## Author: Joseph Brownlee (JellyJoe198)
##
## Based on: https://realpython.com/beautiful-soup-web-scraper-python
##
## This program gets the html of the menu from the internet, then parses it
## in a way to extract the relevant info (titles, menu items, etc)
##
## Parsing: if doFilter: print items in `sortingOrder`,then print others except blacklisted items

## BUG: Choosing different days breaks if program is started 3/7/23 and reran 3/8/23.
##  Removed date choice as a temporary fix.

import requests
import time
import datetime as dt
from bs4 import BeautifulSoup

import sys

true = True
false = False

def intAsk(query, inadd = " (1/0)"):
    ## ask user and return integer value of the response
    ## '0'+input prevents error by making default 0
    return  int('0'+input(query + inadd) )


foodBlacklist = ["Have A Nice Day!"]
def printFood(lotion):
    print('\n', lotion.text ) ## location TITLE
    sector = lotion.find_next( "ul", class_="bite-menu-item" )
    items = sector( "div", class_="col-xs-9" )
    for item in items:
        text = item.find("a").text
        if text in foodBlacklist:
            continue
        print( text )

## main ##

# read args from cmd activation
SKIP_ASK = ("-skip" in sys.argv)
ARG_FILTER = ("-filter" in sys.argv)


URL = "https://menus.sodexomyway.com/BiteMenu/Menu?menuId=14978&locationId=75204001&whereami=http://minesdining.sodexomyway.com/dining-near-me/mines-market" ##URL = "https://realpython.github.io/fake-jobs/"
while true:
    print( "getting website data from: "+URL )
    try:
        page = requests.get(URL)
    except requests.exceptions.ConnectionError as e:
        if intAsk("connection error. Try again?"):
            pass
        else:
            break
        
    except:
        print ("undefined error:\n")
        print (sys.exc_info()[:2])
        break
    else:
        break

soup = BeautifulSoup(page.content, "html.parser")
days = soup.find_all("div", class_="bite-day-menu")

skip_janky = false

## level definitions:
##  Time block {lunch, dinner, etc}
##  Location {grillworks, Simple Servings, noodles, etc}
##  Item {french fries, grilled cheese; chicken, rice, broccoli}


while true: ## repeat parsing unless break
    
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
        print( "Today is", today.get("id") ,end=". \n")
    ##        break ##BUG: can remove date choice as a temporary fix.
        if SKIP_ASK or intAsk("Is this correct?"):
            break ## if user allows, continue program. otherwise change day.
        else:
            ## set day of week to user set value
            weekday = intAsk("what day of the week is it? (assuming Sun=0) ", '') # %7

    doFilter = true
    if skip_janky:
        doFilter = false
    #allowedLocations = ["GRILL", "SIMPLE", "NOOD", "SOUP","VEGETARIAN"] ## TITLES whitelisted in filter. must be ALLCAPS
    blockedLocations = ["DELI","BRICKOVEN","SALAD BAR","MISCELLANEOUS"] ## TITLES blacklisted/disallowed in filter. must be ALLCAPS
    sortingOrder = ["GRILL", "SIMPLE", "NOODL", "SOUP", "GLOBAL", "VEGETARIAN", "BAKE"]
    if not ARG_FILTER and not skip_janky:
        print("default blacklist is ", blockedLocations)
        doFilter = intAsk("Filter out these locations?")

    ## all times blocks in today's menu (lunch, dinner, etc.)
    today_time_blocks = today.find_all( "div", class_="accordion-block" )
    for time_block in today_time_blocks:
        print("\n"*2)
        title = time_block.find( "span", class_="accordion-copy" )
        if doFilter and title.text.find( "AFTERNOON SNACK" ) != -1 :
            continue
        print( title.text ,end="\n--------------------\n" ) # title of this time block, with a line for accent

        ## print each location in this time block
        locations = time_block.find_all( "h5" )

        ## print places in sortingOrder
        if doFilter:
            for place in sortingOrder:
                for lotion in locations:
                    if (lotion.text.find( place ) != -1):
                        printFood(lotion)

        ## print other places not in blacklist
        for lotion in locations:
            
            ## verify that location is allowed (not blacklisted and not already found)
            if doFilter:
                class Found(Exception): pass # https://stackoverflow.com/a/4553525
                try:
                    for place in blockedLocations + sortingOrder:
                        if (lotion.text.find( place ) != -1):
                            raise Found
                except Found:
                    continue

            ## only print if it is allowed.
            printFood(lotion)
                
    result = intAsk("\n\nrun again without reload?")
    if ( result == 0 ):
        break ## if user inputs 0, end program, otherwise restart parsing
    elif result == 1:
        ARG_FILTER = false
        SKIP_ASK = false
        print ("\n"*5) ## whitespace for staying pretty
    elif result == 3:
        skip_janky = true
        SKIP_ASK = true
        print ("\n"*5) ## whitespace for staying pretty
    else:
        print ("\n"*5)

