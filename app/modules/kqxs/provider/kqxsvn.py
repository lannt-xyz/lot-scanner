import requests
from unidecode import unidecode
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# define constant for the URL
URL = 'https://www.kqxs.vn/mien-nam?date='

class KQXSVN:
    def __init__(self):
        # Initialize any variables you need here
        pass

    def craw(self, prize_date: datetime):
        # request URL will be the URL with the processing date in the format yyyy-MM-dd
        request_url = URL + prize_date.strftime('%d-%m-%Y')

        # Make a request to the URL with the payload in the POST method
        r = requests.get(request_url)

        # the response is the text in json format, so we need to convert it to object
        if r.status_code != 200:
            return None

        # convert the response to BeautifulSoup object
        response = BeautifulSoup(r.text, 'html.parser')
        # find the table with class `table-result-lottery`
        table = response.find('table', class_='table-result-lottery')
        # process next date if the table is not exist
        if table is None:
            xsbd = self.tryingXSBD(prize_date)
            prize_date += timedelta(days=1)
            return xsbd

        # find the tbody in the table
        tbody = table.find('tbody')

        # find the channelWrapper which is the first row all rows in the tbody
        rows = tbody.find_all('tr')
        # get the first row
        channel_wrapper = rows[0]
        # get the channelWrapper's cells which is the td tag has class `results`
        channel_wrapper = channel_wrapper.find('td', class_='results')
        # channel is the span tags in the channelWrapper
        channels = channel_wrapper.find_all('span')
        # get the channel name by getting text inside the span tags
        channels = [x.text for x in channels]
        # get the channel code by convert vietnamese to non-vietnamese
        channels = [unidecode(x).lower().replace(' ', '-') for x in channels]
        # if the channel is `ho-chi-minh`, then replace it with `tp-hcm`
        channels = ['tp-hcm' if x == 'ho-chi-minh' else x for x in channels]

        # define a map to store the prizzeValue and cityCode
        prize_map = {channel: {} for channel in channels}
        # loop through all rows in the tbody ignoring the first row
        for row in rows[1:]:
            # get the results
            cells = row.find('td', class_='results')
            # get the numberWrapper
            number_wrapper = cells.find('div', class_='quantity-of-number')
            # get the numbers
            numbers = number_wrapper.find_all('span', class_='number')
            numbers = [x['data-value'] for x in numbers]

            # find quantity of the numbers is the div tag has class `quantity-of-number`
            quantity = row.find('div', class_='quantity-of-number')
            # get the quantity of the numbers is the property `data-quantity`, then convert it to integer
            quantity = quantity['data-quantity']
            quantity = int(quantity)
            
            prize_code = row.find('td', class_='prize').text
            prize_code = unidecode(prize_code).lower().replace(' ', '-')
            # replace special prize code
            prize_code = 'giai-dac-biet' if prize_code == 'dac-biet' else prize_code

            # loop through all the numbers
            index = 0
            for number in numbers:
                # get the city code by getting the index of the number
                city_code = channels[index % (quantity)]

                # Initialize the prize_code as a list if not already present
                if prize_code not in prize_map[city_code]:
                    prize_map[city_code][prize_code] = []
                # Append the value to the list
                prize_map[city_code][prize_code].append(number)

                index += 1

        return prize_map
