# gismeteo
Parsing of Gismeteo weather archive using Beautiful Soup, Scrapy and Selenium

Here you'll find detailed help on how to run each of Gismeteo weather diary scrapers. Enjoy!

## Important! If the scraper doesn’t work please turn on VPN (any of CIS countries, better Russia). Sometimes Gismeteo doesn’t work at all or work very slowly if     you are in the EU, USA or any other country.

Beautiful Soup (gismeteo_soup.py)

- Install Beautiful Soup using command: pip install beautifulsoup4
- Set the {cityid} parameter in line 8. For Warsaw it’s 3196
- Set {startdate} and {finishdate} in lines 11 and 12 to crawl diary between this dates
- In line 28 set True if you want to limit the quantity of scraped pages to 100 and False to run scraper without limits. In line 31 you can change the limit from     100 to any quantity of pages you want
- Run spider
- After parsing is complete the data will appear in the file “diary_{cityid}.csv”

Scrapy (gismeteo_scrapy.py)

- Install Scrapy using command: pip install scrapy
- Create a project using command: scrapy startproject gismeteo
- Set the {cityid} parameter in line 12. For Warsaw it’s 3196
- Set {startdate} and {finishdate} in lines 14 and 15 to crawl diary between this dates
- In line 10 set True if you want to limit the quantity of scraped pages to 100 and False to run scraper without limits. In line 31 you can change the limit from     100 to any quantity of pages you want
- Copy file gismeteo_scrapy.py to the folder gismeteo/spiders (if it’s not there at this moment)
- Open Terminal and run command from the scrapy/gismeteo folder:
  scrapy crawl gismeteo -O diary_3196.csv:csv

P.S. A few days ago Scrapy update was launched with the bug that shows AttributeError. Read more: https://stackoverflow.com/questions/77002835/im-learning-python-web-scraping-it-shows-attributeerror-when-i-scrapy-crawl-a
So if you have latest version of Scrapy and your spider doesn't work, first try command: pip install Twisted==22.10.0


Selenium 

- Install Selenium using command: pip install selenium
- Install Chromedriver. The installation for Windows and MacOS is differs so google how to do that for your system
- Set the {cityid} parameter in line 97. For Warsaw it’s 3196
- Set {startdate} and {finishdate} in lines 100 and 101 to crawl diary between this dates
- In line 86 set True if you want to limit the quantity of scraped pages to 100 and False to run scraper without limits. In line 117 you can change the limit from    100 to any quantity of pages you want
- Run spider
- After parsing is complete the data will appear in the file “diary_{cityid}.csv”

P.S. Please be careful using this scrapers and respect the law

