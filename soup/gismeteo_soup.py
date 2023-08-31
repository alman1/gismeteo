from bs4 import BeautifulSoup
import datetime
import requests
import pandas as pd
import time

# setting city ID (Warsaw = 3196)
cityid = 3196

# setting start and finish date to crawl
startdate = datetime.datetime(1997, 4, 1) # april 1997
finishdate = datetime.datetime(2023, 8, 30) # august 2023

# start counting time for scraper performance
start_time = time.time()

pickyear = startdate.year
pickmonth = startdate.month


# creating a structure of the future dataset
columns = {'Date':[], 'D Temperature':[], 'D Pressure':[], 'D Cloudiness':[],
       'D Weather Conditions':[], 'D Wind Direction':[], 'D Wind Speed':[], 'N Temperature':[], 'N Pressure':[], 'N Cloudiness':[],
       'N Weather Conditions':[], 'N Wind Direction':[], 'N Wind Speed':[]}
wedata = pd.DataFrame(columns)

# creating limiting parameter
limit = True

# creating list of urls with month and year parameters
urls = []
scraped_pages = 0
while pickyear != finishdate.year or pickmonth != finishdate.month:

    url = f'https://gismeteo.ru/diary/{cityid}/{pickyear}/{pickmonth}'
    urls.append((pickmonth, pickyear, url))

    scraped_pages += 1
    if scraped_pages == 100 and limit:
        break

    pickmonth += 1
    if pickmonth == 13:
        pickmonth = 1
        pickyear += 1

# parsing urls from the list
for pickmonth, pickyear, url in urls:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content.decode('utf-8','ignore'), 'html5lib')
    print(url)

    # getting all the rows from the table
    for tablerowtag in soup.find_all('tr', {'align': 'center'}):

        ### day weather###

        # getting data from every column
        date = tablerowtag.td.get_text()

        # day temperature
        dtemperature = tablerowtag.td.find_next_sibling()
        if dtemperature.img == None:
            dtemperature = dtemperature.get_text()
        else:
            dtemperature = ''

        # day pressure
        dpressure = tablerowtag.td.find_next_sibling().find_next_sibling()
        if dpressure.img == None:
            dpressure = dpressure.get_text()
        else:
            dpressure = ''

        # transforming cloudiness
        dcloudiness = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling()

        if dcloudiness.get_text() == '—':
            dcloudiness = ''
        else:
            if 'sun.png' in dcloudiness.img['src']:
                dcloudiness = 'Sun'
            elif 'sunc.png' in dcloudiness.img['src']:
                dcloudiness = 'Sun/Clouds'
            elif 'suncl.png' in dcloudiness.img['src']:
                dcloudiness = 'Mostly Clouds'
            elif 'dull.png' in dcloudiness.img['src']:
                dcloudiness = 'Dull'
            else:
                dcloudiness = ''

        # transforming weather conditions
        dwconditions = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()

        if dwconditions.img == None:
            dwconditions = ''
        else:
            if 'rain.png' in dwconditions.img['src']:
                dwconditions = 'Rain'
            elif 'snow.png' in dwconditions.img['src']:
                dwconditions = "Snow"
            elif 'storm.png' in dwconditions.img['src']:
                dwconditions = 'Storm'
            else:
                dwconditions = ''

        # transforming wind to direction and speed
        dwind = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()

        if dwind.img == None:
            if dwind.span.get_text() == 'Ш':
                dwinddirection = 'No wind'
                dwindspeed = 'No wind'
            else:
                dwinddirection = ''
                dwindspeed = ''
        else:
            if 'still.gif' in dwind.img['src']:
                dwinddirection = ''
                dwindspeed = ''
            else:
                dwind = dwind.span.get_text().split()
                dwinddirection = dwind[0]
                dwindspeed = dwind[1]

        ### evening weather###

        # night temperature
        ntemperature = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
        if ntemperature.img == None:
            ntemperature = ntemperature.get_text()
        else:
            ntemperature = ''

        # night pressure
        npressure = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
        if npressure.img == None:
            npressure = npressure.get_text()
        else:
            npressure = ''

        # transforming cloudiness
        ncloudiness = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()

        if ncloudiness.get_text() == '—':
            ncloudiness = ''
        else:
            if 'sun.png' in ncloudiness.img['src']:
                ncloudiness = 'Sun'
            elif 'sunc.png' in ncloudiness.img['src']:
                ncloudiness = 'Sun/Clouds'
            elif 'suncl.png' in ncloudiness.img['src']:
                ncloudiness = 'Mostly Clouds'
            elif 'dull.png' in ncloudiness.img['src']:
                ncloudiness = 'Dull'
            else:
                ncloudiness = ''

        # transforming weather conditions
        nwconditions = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()

        if nwconditions.img == None:
            nwconditions = ''
        else:
            if 'rain.png' in nwconditions.img['src']:
                nwconditions = 'Rain'
            elif 'snow.png' in nwconditions.img['src']:
                nwconditions = "Snow"
            elif 'storm.png' in nwconditions.img['src']:
                nwconditions = 'Storm'
            else:
                nwconditions = ''

        # transforming wind to direction and speed
        nwind = tablerowtag.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()

        if nwind.img == None:
            if nwind.span.get_text() == 'Ш':
                nwinddirection = 'No wind'
                nwindspeed = 'No wind'
            else:
                nwinddirection = ''
                nwindspeed = ''
        else:
            if 'still.gif' in nwind.img['src']:
                nwinddirection = ''
                nwindspeed = ''
            else:
                nwind = nwind.span.get_text().split()
                nwinddirection = nwind[0]
                nwindspeed = nwind[1]

        wedatarow = [f"{date}.{pickmonth}.{pickyear}", dtemperature, dpressure, dcloudiness, dwconditions, dwinddirection, dwindspeed, ntemperature,
                     npressure,
                     ncloudiness, nwconditions, nwinddirection, nwindspeed]

        # appending new list to the dataframe
        wedata.loc[len(wedata)] = wedatarow


wedata.to_csv(f'diary_{cityid}.csv', encoding='utf-8', index=False)

# performance of the scraper
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Algorithm took {elapsed_time:.6f} seconds to run.")