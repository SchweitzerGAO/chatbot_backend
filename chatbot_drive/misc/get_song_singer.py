from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


def get_urls(base):
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    browser.get(base)
    browser.switch_to.frame('g_iframe')
    page_text = browser.execute_script("return document.documentElement.outerHTML")
    browser.quit()
    urls = []
    soup = BeautifulSoup(page_text, 'html.parser')
    l = soup.find('ul', id='m-pl-container')
    lis = l.find_all('li')
    for item in lis:
        url = 'https://music.163.com/#/' + item.find_all('div')[0].find('a')['href']
        urls.append(url)
    return urls


def get_doc(url):
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    page_text = browser.execute_script("return document.documentElement.outerHTML")
    browser.quit()
    return page_text


def get_song_names(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    table = soup.find('table', class_='m-table')
    items = table.find_all('b')
    song_names = [item['title'].split(' - ')[0] for item in items]
    with open('../data/lookup/lookup_song.yml', 'a', encoding='utf-8') as f:
        for item in song_names:
            f.write(f'    - {item}\n')


def get_singers(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    table = soup.find('table', class_='m-table')
    trs = table.find_all('tr')
    items = [tr.find('div', class_='text') for tr in trs]
    singers = []
    for item in items[1:]:
        for i in item['title'].split('/'):
            singers.append(i)
    singers = set(singers)
    with open('../data/lookup/lookup_singer.yml', 'a', encoding='utf-8') as f:
        for item in singers:
            f.write(f'    - {item}\n')


if __name__ == '__main__':
    base = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=0'
    urls = get_urls(base)
    for url in urls:
        doc = get_doc(url)
        get_singers(doc)
