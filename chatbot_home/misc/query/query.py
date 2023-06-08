# from py2neo import Graph
import datetime
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

# url = 'bolt://localhost:7687'
# graph = Graph(url, name='neo4j', password='123456')
location_key = 'HJJBZ-DXQLS-CNSOY-6YFEL-2U7HJ-2WFA7'
weather_key = '344e70c28d4c454d8888813b30fa085a'


# def query_kb(node, rel, limit=None):
#     res = []
#     query_1 = f'match(n)-[r:relation]->(p) where n.name="{node}" and r.name="{rel}" return n,r,p'
#     query_2 = f'match(n)-[r:relation]->(p) where n.name contains "{node}" and r.name contains "{rel}" return n,r,p'
#     if limit is not None:
#         query_1 += f' limit {limit}'
#         query_2 += f' limit {limit}'
#     answers = graph.run(query_1)
#     answers = list(answers)
#     if len(answers) == 0:
#         answers = graph.query(query_2)
#         answers = list(answers)
#     if len(answers) == 0:
#         return None
#     for ans in answers:
#         n = dict(ans)['n']['name']
#         r = dict(ans)['r']['name']
#         p = dict(ans)['p']['name']
#         p = re.sub('<[^<]+?>', '', p).replace('\n', '').strip()
#         res.append((n, r, p))
#         print(n, r, p)
#     return res


def query_internet(node, rel=None):
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(node)
    respond = requests.get(url)
    text = respond.text
    bs = BeautifulSoup(text, 'html.parser')
    summary = bs.find_all('div', 'lemma-summary')
    summary = summary[0].get_text()
    summary = re.sub('\[[0-9]*\]', '', summary).replace('\n', '').strip()

    relation = bs.find_all('dt', 'basicInfo-item name')
    values = bs.find_all('dd', 'basicInfo-item value')
    result_dict = dict()
    for i in range(len(relation)):
        result_dict[relation[i].get_text().replace('\xa0', '')] = values[i].get_text().replace('\xa0', '').replace('\n',
                                                                                                                   '')
    if rel is None:
        return summary
    res = result_dict.get(rel, None)
    if res is None:
        pass
    return res


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


if __name__ == '__main__':
    # print(datetime.datetime.now())
    # ans = graph.run('match(n)-[r:relation]->(p) where n.name contains "同济大学" and r.name contains "aaa" return n,'
    #           'p limit(20)')
    # print(list(ans))
    # print(datetime.datetime.now())
    print(datetime.datetime.now())
    # print(query_internet('三体','作者'))
    for item in query_time_location_weather():
        print(item)
    print(datetime.datetime.now())
