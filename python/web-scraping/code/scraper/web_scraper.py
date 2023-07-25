from bs4 import BeautifulSoup
import requests


class WebScraper:

    BASE_URL = "https://nos.nl/"
    ARCHIEF_URL = BASE_URL + "nieuws/archief/"

    def __init__(self):
        self.html_content = None
        self.soup = None

    def _get_response(self, date):
        response = requests.get(self.ARCHIEF_URL)
        if response.status_code == 200:
            return response.content
        else:
            raise ConnectionError(f'Failed to connect to {self.ARCHIEF_URL}: {response}.')

    def get_articles(self, date=''):
        self.html_content = self._get_response(date)
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

        articles = self.soup.find_all('li', class_='list-time__item')
        for article in articles:
            headline = article.find('div', class_='list-time__title link-hover').text
            link = article.find('a')['href']
            date = article.find('time')['datetime']


if __name__ == '__main__':
    scraper = WebScraper()
