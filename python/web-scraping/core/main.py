import pandas as pd
from tqdm import tqdm
from scraper.web_scraper import WebScraper
from database.db_connection import DBConnection


def main():
    scraper = WebScraper()

    date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2022-01-31', '2022-01-01', freq='D')]

    # for date in tqdm(date_range):
    #     scraper.load_articles_into_database(str(date))

    with DBConnection() as dbc:
        cols = dbc.read(table_name="nos", table_cols=("date", "text"), date='2022-01-01')
        for col in cols:
            print(col)


if __name__ == '__main__':
    main()
