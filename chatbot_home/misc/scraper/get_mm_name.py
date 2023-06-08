from bs4 import BeautifulSoup
import requests
import re
import zhconv


def get_urls_movie(n=10):
    urls = []
    num = (n - 1) * 25 + 1
    for i in range(0, num, 25):
        url = f'https://movie.douban.com/top250?start={i}&filter='
        urls.append(url)
    return urls


def get_urls_series(n=10):
    urls = []
    num = (n - 1) * 25 + 1
    for i in range(0, num, 25):
        url = f'https://www.douban.com/doulist/110585733/?start={i}&sort=seq&playable=0&sub_type='
        urls.append(url)
    return urls


def get_urls_music(n=10):
    urls = []
    num = (n - 1) * 25 + 1
    for i in range(0, num, 25):
        url = f'https://music.douban.com/top250?start={i}'
        urls.append(url)
    return urls


def login():
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36'}

    cookies = 'bid=3VcqwK5N-QU; douban-fav-remind=1; __yadk_uid=5Vq7rBwv1wvCHf9fZdDJ0dC5Uhnopk37; ' \
              '__gads=ID=b6dff46c79f89b4a-225b7ac455d500f3:T=1658803421:RT=1658803421:S' \
              '=ALNI_Maj72R0vErqDIluaMOntY9xRFvo9g; ll="118376"; push_noty_num=0; push_doumail_num=0; ' \
              'dbcl2="267162139:nnI7P6hRjCY"; __utmv=30149280.26716; ck=HlT4; _pk_ref.100001.8cb4=["","",1675133546,' \
              '"https://cn.bing.com/"]; ap_v=0,6.0; ' \
              '__gpi=UID=00000815e8792f7c:T=1658803421:RT=1675133546:S=ALNI_MY5UKrupNNav6XUWBCDjDbpjcfclA; ' \
              '__utma=30149280.819979838.1658803423.1675068840.1675133550.4; __utmc=30149280; ' \
              '__utmz=30149280.1675133550.4.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ct=y; ' \
              '_pk_id.100001.8cb4=96a729d11894bb64.1658803419.4.1675133679.1675069070.; ' \
              '__utmb=30149280.10.10.1675133550; _ga=GA1.2.819979838.1658803423; _gid=GA1.2.703943066.1675134607; ' \
              'frodotk_db="cd90c11db783bb9268b24359268b32b6" '

    cookies = cookies.split('; ')
    cookies_dict = {}
    for i in cookies:
        cookies_dict[i.split('=')[0]] = i.split('=')[1]

    return user_agent, cookies_dict


def get_movies_info(url, user_agent, cookies):
    html = requests.get(url,
                        headers=user_agent,
                        cookies=cookies)

    html.encoding = html.apparent_encoding

    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('ol', class_='grid_view').find_all('li')
    movies_info = []

    for item in items:
        movie_name = item.find('div', class_='hd').find('a').find(class_='title').text
        movies_info.append(movie_name)
    return movies_info


def get_series_info(url, user_agent, cookies):
    series_info = []
    html = requests.get(url,
                        headers=user_agent,
                        cookies=cookies)

    html.encoding = html.apparent_encoding

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        items = soup.find('div', class_='article').find_all('div', class_='doulist-item')

        for item in items:
            series_name = item.find('div', class_='title').find('a').text
            zh_name = series_name.split()[0]
            # print(zh_name)
            series_info.append(zh_name)
        return series_info
    except Exception as e:
        return series_info


def get_music_info(url, user_agent, cookies):
    cn_pattern = re.compile('^[\u4e00-\u9fa5]+(?:[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+)?')
    music_info = []
    html = requests.get(url,
                        headers=user_agent,
                        cookies=cookies)

    html.encoding = html.apparent_encoding

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        items = soup.find('div', class_='indent').find_all('tr', class_='item')

        for item in items:
            music_name = item.find('td', valign='top').find('a')['title']
            name = music_name.split(' - ')[1]
            if cn_pattern.match(name):
                name = zhconv.convert(name, 'zh-hans')
                print(name)
                music_info.append(name)
        return music_info
    except Exception as e:
        print(e)
        return music_info


if __name__ == '__main__':
    information = []
    # urls_movie = get_urls_movie()
    # urls_series = get_urls_series()
    # ua, cookies = login()
    # for url in urls_movie:
    #     info = get_movies_info(url, ua, cookies)
    #     information.extend(info)
    # for url in urls_series:
    #     info = get_series_info(url, ua, cookies)
    #     information.extend(set(info))
    urls_music = get_urls_music()
    ua, cookies = login()
    for url in urls_music:
        info = get_music_info(url, ua, cookies)
        information.extend(info)

    with open('../../data/lookup/lookup_mm_name.yml', 'a', encoding='utf-8') as f:
        for info in information:
            f.write(f'\n  - {info}')
