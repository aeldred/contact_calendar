import requests
import json
import re
from flask import render_template, request
from contact_calendar import app

@app.route('/contact_calendar')
def contact_calendar():
    """Display the contact calendar based on API data."""

    # get city from request or use minneapolis as default
    city = request.args.get('city') or 'minneapolis'
    
    # define parameters for get request
    params = {
        'q': city + ',us',
        'units': 'imperial',
        'APPID': '09110e603c1d5c272f94f64305c09436'
    }

    # get data from api
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                     params=params)

    # parse the data returned from api
    calendar = parse_data(json.loads(r.text))

    error_msg = ''
    if ('error_msg' in calendar[0]):
        error_msg = calendar[0]['error_msg']
    
    # display the results
    return render_template('contact_calendar.html', 
                           calendar=calendar, 
                           error_msg=error_msg,
                           title='ACME Contact Calendar'
    )


def parse_data(data):
    """Parse json data from api into values needed for calendar."""
    contact_method = []

    if (data['cod'] == '200'):
        curr_date = ''
        curr_weather = ''
        temp_total = 0
        temp_cnt = 0

        # Assumptions for daily forecast:
        #     1. if it rains/snows at any point in the day then
        #        weather='precip' for entire day
        #     2. the average daily temperature is used for daily temp
        for forecast in data['list']:
            
            # get only the date portion of dt_txt
            dt_part = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', 
                           forecast['dt_txt']
                 ).group().split('-')
            dt = dt_part[1] + '-' + dt_part[2] + '-' + dt_part[0]
           
           
            # handle end of curr_date 
            if (dt != curr_date):
                # skip storing data if this is first forecast
                if (curr_date != ''):
                    avg_temp = round((temp_total / temp_cnt), 2)
                    temp_total = 0
                    temp_cnt = 0

                    # store previous date's data
                    contact_method.append({
                        'date': curr_date,
                        'contact_method': get_contact_method(avg_temp, curr_weather)
                    })
               
                # get values for the current forecast
                curr_date = dt
                curr_weather = get_weather(forecast)
                temp_total = forecast['main']['temp']
                temp_cnt += 1
            else:
                temp_total += forecast['main']['temp']
                temp_cnt += 1

                # no need to check weather if precip already forecasted
                # (see forecast assumption 1)  
                if (curr_weather != 'precip'):
                    curr_weather = get_weather(forecast)

    # handle error returned from api
    else:
        contact_method.append({'error_msg': 'Error: ' + data['message']})

    return contact_method
   

def get_contact_method(temp, weather):
    """Determine the contact method (email, phone, or text)
       based on the weather (precipitation or clear).
    """

    # Assumptions for contact method:
    #     1. rain and snow are generalized to mean precipitation
    #     2. weather will only ever be 'precip' or 'clear'
    #        (see Assumptions for get_weather function for
    #         definition of precip and clear)
    if (weather == 'precip' or temp < 55):
        return 'phone'
    elif (temp > 75 and weather == 'clear'):
        return 'text'
    elif (temp >= 55 and temp <= 75):
        return 'email'
    else:
        return 'unknown'

    
def get_weather(forecast):
    """Get the weather conditions based on the current forecast."""

    # Assumptions for weather:
    #     1. if cloud cover is >= 50% it's likely there will be precipitation
    #     2. if cloud cover is < 50% it's sunny enough to be 'clear'
    if ('rain' in forecast):
        return 'precip'
    elif ('snow' in forecast):
        return 'precip'
    elif ('clouds' in forecast):
        if (forecast['clouds']['all'] >= 50):
            return 'precip'
        else:
            return 'clear'

