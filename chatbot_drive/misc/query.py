import datetime
import json
import requests

location_key = 'HJJBZ-DXQLS-CNSOY-6YFEL-2U7HJ-2WFA7'
weather_key = '344e70c28d4c454d8888813b30fa085a'


def query_time_location_weather():
    now = datetime.datetime.now()
    today_date = f'{now.year}年{now.month}月{now.day}日'

    location_service = f'https://apis.map.qq.com/ws/location/v1/ip?key={location_key}'
    respond_loc = requests.get(location_service)
    loc_json = json.loads(respond_loc.text)
    city = loc_json['result']['ad_info']['city']
    district = loc_json['result']['ad_info'].get('district', '')
    adcode = loc_json['result']['ad_info']['adcode']
    location = f'{city}{district}'

    city_search_service = f'https://geoapi.qweather.com/v2/city/lookup?location={adcode}&key={weather_key}'
    respond_city = requests.get(city_search_service)
    city_json = json.loads(respond_city.text)
    city_id = city_json['location'][0]['id']

    daily_weather_service = f'https://devapi.qweather.com/v7/weather/3d?location={city_id}&key={weather_key}'
    respond_daily_weather = requests.get(daily_weather_service)
    daily_weather_json = json.loads(respond_daily_weather.text)
    weather = daily_weather_json['daily'][0]['textDay']
    min_temp = daily_weather_json['daily'][0]['tempMin']
    max_temp = daily_weather_json['daily'][0]['tempMax']

    now_weather_service = f'https://devapi.qweather.com/v7/weather/now?location={city_id}&key={weather_key}'
    respond_now_weather = requests.get(now_weather_service)
    respond_now_weather_json = json.loads(respond_now_weather.text)
    now_temp = respond_now_weather_json['now']['temp']
    now_feel = respond_now_weather_json['now']['feelsLike']

    return today_date, now.hour, location, weather, min_temp, max_temp, now_temp, now_feel

