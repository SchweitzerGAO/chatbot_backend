import requests
from bs4 import BeautifulSoup

def get_urls():
    base_url = 'https://ielts.koolearn.com/20140411/785955.html'
    html = requests.get(base_url)
    html.encoding = html.apparent_encoding
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('table').find_all('td')

    urls = None
    return urls


def get_verbs():
    urls = get_urls()


if __name__ == '__main__':
    get_urls()
