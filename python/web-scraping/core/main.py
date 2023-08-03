import pandas as pd
from tqdm import tqdm
from scraper.web_scraper import WebScraper


def main():
    scraper = WebScraper()

    date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2022-01-01', '2022-12-31', freq='D')]

    for date in tqdm(date_range):
        scraper.load_articles_into_database(str(date))


if __name__ == '__main__':
    main()
