from operator import le
import requests
from datetime import datetime, timedelta

from app.modules.kqxs.errors import IncorrectResultException

# define constant for the URL
URL = 'https://www.xosobinhduong.com.vn/get-lottery-mn?mask=getResultLoteryMn&skip=true&flagNumber=-1&lotdate='

class XSBD:
    def __init__(self):
        # Initialize any variables you need here
        pass

    def craw(self, prize_date: datetime):
        # request URL will be the URL with the processing date in the format yyyy-MM-dd
        request_url = URL + prize_date.strftime('%Y-%m-%d')

        # Make a request to the URL with the payload in the POST method
        r = requests.post(request_url)

        # the response is the text in json format, so we need to convert it to object
        if r.status_code != 200:
            prize_date += timedelta(days=1)
            return None

        # convert the response to object
        jsonStr = r.json()

        # check the status of the response
        status = jsonStr['status']
        if status != 1:
            prize_date += timedelta(days=1)
            return None

        # Extract data from the JSON response
        data = jsonStr.get('data', {})
        headers = data.get('header', [])
        body = data.get('body', [])

        # Initialize a map to store the prize results for each city
        prize_map = {header['city_code']: {} for header in headers}

        # Process the body to map prizes to cities
        for prize in body:
            prize_code = prize['code']  # e.g., "giai-tam", "giai-dac-biet"
            prize_data = prize['data']  # List of prize results for each city
            for city_results in prize_data:
                for result in city_results:
                    city_code = result['city_code']
                    value = result['value']

                    if city_code in prize_map:
                        # Initialize the prize_code as a list if not already present
                        if prize_code not in prize_map[city_code]:
                            prize_map[city_code][prize_code] = []
                        # Append the value to the list
                        prize_map[city_code][prize_code].append(value)

        return prize_map
