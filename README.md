# menu-scraper
Extracts relevant data from online food menu. 

Based on: https://realpython.com/beautiful-soup-web-scraper-python

This program gets the html of the menu from the internet, then parses it in a way to extract the relevant info (titles, menu items, etc) and print that to std out.

It is still a proof of concept. Features such as nutrition facts, dates other than in this week, and pretty UI are not yet implemented. See `example interaction.txt` for the 10/05/21 menu.

## How to use
`sodexo menu scraper.py` can be run in cmd on its own without arguments, which would run the default behavior:  
1. collect the [full menu](https://menus.sodexomyway.com/BiteMenu/Menu?menuId=14978&locationId=75204001&whereami=http://minesdining.sodexomyway.com/dining-near-me/mines-market) into the `soup` variable
2. check date by asking user
3. ask user if they want to apply the blacklist (filters out less commonly used locations)
4. display today's menu, with the blacklisted locations filtered out if chosen.
5. ask user to run again (ignoring any arguments)

Alternatively, you can run the program with arguments which would skip certain prompts:  
-skip: skips step 2, assuming `dt.date.today().weekday()` is correct  
-filter: skips step 3, and applies the blacklist  

To use these arguments, add them to the end of the line in your terminal, e.g. in Windows cmd: `py "sodexo menu scraper.py" -skip -filter`   
These can be added to a shortcut for easier use. In Windows shortcuts, the Target is the file (including location) in quotes with arguments after the quotes.  

## Libraries
standard libraries:
- time
- datetime
- sys

pip libraries:
- requests
- beautifulsoup4

## Known issues
bug: fails when the month changes in the middle of the week and you try to look at items in a different month. This is hard to debug because it can only be seen at specific times in the year.
