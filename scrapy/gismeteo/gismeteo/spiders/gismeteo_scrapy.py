import scrapy
import datetime
import pandas as pd


# general spider class, following scrapy interface
class GismeteoSpider(scrapy.Spider):
    name = "gismeteo"

    limit = True

    city_id = 3196

    startdate = datetime.datetime(1997, 4, 1)
    finishdate = datetime.datetime(2023, 8, 30)

    # storage for parsing results
    rows = []

    # method for initializing scrapy spider
    # in our case, yields urls for all required dates
    def start_requests(self):
        urls = []

        pickyear = self.startdate.year
        pickmonth = self.startdate.month
        while pickyear != self.finishdate.year or pickmonth != self.finishdate.month:
            url = f'https://www.gismeteo.ru/diary/{self.city_id}/{pickyear}/{pickmonth}/'
            urls.append(url)

            if len(urls) == 100 and self.limit:
                break

            pickmonth += 1
            if pickmonth > 12:
                pickmonth -= 12
                pickyear += 1
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # three methods for proper parsing of images, integers and wind cells
    def parse_image(self, selector, name_mapping):
        if not selector.css('img'):
            return ''
        for indicator, name in name_mapping.items():
            if indicator in selector.css('img')[0].get():
                return name
        return ''

    def parse_int(self, selector):
        value = selector.css('::text').get()
        if not value:
            return ''
        return int(selector.css('::text').get())

    def parse_wind(self, selector):
        value = selector.css('::text').get()
        if value is None:
            value = ''
        result = value.strip().split()
        if len(result) < 2:
            return ['', '']
        return result

    # method for extracting information from single table row
    def extract_line(self, data, date):
        # mapping from image names to appropriate names
        cloud_names = {
            'sun.png': 'Sun',
            'sunc.png': 'Sun/Clouds',
            'suncl.png': 'Mostly Clouds',
            'dull.png': 'Dull'
        }
        weather_names = {
            'rain.png': 'Rain',
            'snow.png': 'Snow',
            'storm.png': 'Storm'
        }

        day_wind = self.parse_wind(data[5])
        night_wind = self.parse_wind(data[10])

        # each key corresponds to a column in resulting csv file
        return {
            'Date': date.strftime('%d.%m.%Y'),
            'D Temperature': self.parse_int(data[1]),
            'D Pressure': self.parse_int(data[2]),
            'D Cloudiness': self.parse_image(data[3], cloud_names),
            'D Weather Conditions': self.parse_image(data[4], weather_names),
            'D Wind Direction': day_wind[0],
            'D Wind Speed': day_wind[1],
            'N Temperature': self.parse_int(data[6]),
            'N Pressure': self.parse_int(data[7]),
            'N Cloudiness': self.parse_image(data[8], cloud_names),
            'N Weather Conditions': self.parse_image(data[9], weather_names),
            'N Wind Direction': night_wind[0],
            'N Wind Speed': night_wind[1]
        }
    
    # method for parsing single http response, required by scrapy.Spider
    # yields data, scrapped from response
    def parse(self, response):
        table = response.css('tr')[2:]
        parts = response.url.strip().split('/')
        month = int(parts[-2])
        year = int(parts[-3])
        
        for i, row in enumerate(table):
            data = row.css('td')
            day = i + 1
            date = datetime.datetime(year, month, day)
            result = self.extract_line(data, date)
            self.rows.append(result)
            yield

    def closed(self, reason):
        print('Hello')
        df = pd.DataFrame(self.rows)
        print('Was there')
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
        print('OK')
        df.sort_values('Date').to_csv(f'diary_{self.city_id}.csv', index=False)