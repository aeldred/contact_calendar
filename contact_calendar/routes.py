import requests
import json
import re
from flask import render_template, request
from contact_calendar import app


@app.route('/')
@app.route('/contact_calendar/')
def main():
    return contact_calendar('minneapolis')

@app.route('/contact_calendar/<city>/')
@app.route('/contact_calendar/<city>/<state>/')
def contact_calendar(city, state=''):
    """Display the contact calendar based on API data."""

    # define parameters for get request
    # note: if the api doesn't find the city in the
    # requested state, it returns a some city with the
    # same name. i.e. portland,mn,us returns values for
    # portland,or,us
    params = {
        'q': f"{city},{state},us",
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
    # The API doesn't return a state, so the state that's output
    # will be the state that's input. So if no state is given
    # no state is output - without looking up latitude and longitude
    # we're left to guess which precise city's weather this is
    return render_template('contact_calendar.html',
                           city=city,
                           state=state.upper(),
                           calendar=calendar,
                           error_msg=error_msg,
                           title='ACME Contact Calendar'
    )


def parse_data(data):
    """Parse json data from api into values needed for calendar."""
    calendar = []

    if (data['cod'] == '200'):
        curr_date = ''
        curr_weather = ''
        temp_total = 0
        temp_cnt = 0

        # Assumptions for daily forecast:
        #     1. if it rains/snows at any point in the day then
        #        weather='precipitation' for entire day
        #     2. the average daily temperature is used for daily temp
        for forecast in data['list']:

            # get only the date portion of dt_txt
            dt_part = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',
                           forecast['dt_txt']
                 ).group().split('-')
            forecast_date = f"{dt_part[1]}-{dt_part[2]}-{dt_part[0]}"


            # handle end of curr_date
            if (forecast_date != curr_date):
                # skip calculating avg temp if no data has been parsed yet
                # otherwise calculate the avg temp for the curr_date
                if (curr_date != ''):
                    avg_temp = round((temp_total / temp_cnt), 2)
                    temp_total = 0
                    temp_cnt = 0

                    # store previous date's data
                    calendar.append({
                        'date': curr_date,
                        'weather': curr_weather,
                        'avg_temp': avg_temp,
                        'contact_method': get_contact_method(avg_temp, curr_weather)
                    })

                # get values for the current forecast
                curr_date = forecast_date
                curr_weather = get_weather(forecast)
                temp_total = forecast['main']['temp']
                temp_cnt += 1
            else:
                temp_total += forecast['main']['temp']
                temp_cnt += 1

                # no need to check weather if precipitation already forecasted
                # (see forecast assumption 1)
                if (curr_weather != 'precipitation'):
                    curr_weather = get_weather(forecast)

    # handle error returned from api
    else:
        calendar.append({'error_msg': 'Error: ' + data['message']})

    return calendar


def get_contact_method(temp, weather):
    """Determine the contact method (email, phone, or text)
       based on the weather (precipitation or clear).
    """

    # Assumptions for contact method:
    #     1. rain and snow are generalized to mean precipitation
    #     2. weather will only ever be 'precipitation' or 'clear'
    #        (see Assumptions for get_weather function for
    #         definition of precipitation and clear)
    #     3. in problem statement, "between 55 - 75" is inclusive
    if (weather == 'precipitation' or temp < 55):
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
        return 'precipitation'
    elif ('snow' in forecast):
        return 'precipitation'
    elif ('clouds' in forecast):
        if (forecast['clouds']['all'] >= 50):
            return 'precipitation'
        else:
            return 'clear'

