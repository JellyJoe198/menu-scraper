# menu-scraper
Extracts relevant data from online food menu. 

Based on: https://realpython.com/beautiful-soup-web-scraper-python

This program gets the html of the menu from the internet, then parses it in a way to extract the relevant info (titles, menu items, etc) and print that to std out.

It is still a proof of concept. Features such as nutrition facts, dates other than in this week, and pretty UI are not yet implemented. See `example interaction.txt` for the 10/05/21 menu.

## Known issues
bug: fails when the month changes in the middle of the week and you try to look at items in a different month. This is hard to debug because it can only be seen at specific times in the year.
