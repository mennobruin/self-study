import sqlite3

from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm

from core.database.db_connection import DBConnection


class WebScraper:

    BASE_URL = "https://nos.nl"
    ARCHIEF_URL = BASE_URL + "/nieuws/archief/"

    DB_TABLE_NAME = "nos"
    DB_TABLE_COLUMN_NAMES = ["date", "link", "headline", "text"]

    def __init__(self):
        self.html_content = None
        self.soup = None

    @staticmethod
    def _get_response(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise ConnectionError(f'Failed to connect to {url}: {response}.')

    def load_articles_into_database(self, date=''):
        self.html_content = self._get_response(url=self.ARCHIEF_URL + date)
        self.soup = BeautifulSoup(self.html_content, 'lxml')

        articles = self.soup.find_all('li', class_='list-time__item')
        for article in articles:
            headline = article.find('div', class_='list-time__title link-hover').text
            link = article.find('a')['href']
            date = article.find('time')['datetime']
            text = self._get_text(url=self.BASE_URL + link)
            with DBConnection() as dbc:
                try:
                    dbc.write(table_name=self.DB_TABLE_NAME,
                              table_cols=self.DB_TABLE_COLUMN_NAMES,
                              data=(date, link, headline, text))
                except sqlite3.IntegrityError as e:
                    print(e)
                    continue

    def _get_text(self, url):
        html = str(self._get_response(url))
        article_body_matches = re.findall(r'"articleBody"\s*:\s*"(.*?)"', html)
        return article_body_matches[0] if article_body_matches else None


if __name__ == '__main__':
    scraper = WebScraper()
    scraper.load_articles_into_database()
