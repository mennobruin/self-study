import re
import pandas as pd
import pickle as pk
from tqdm import tqdm
from collections import defaultdict, Counter
from scraper.web_scraper import WebScraper
from database.db_connection import DBConnection


def main():
    scraper = WebScraper()

    start_date = '2022-01-01'
    end_date = '2022-01-01'
    date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range(start_date, end_date, freq='D')]
    all_word_freq = Counter()

    with DBConnection() as dbc:
        for date in tqdm(date_range):
            # scraper.load_articles_into_database(str(date))
            cols = dbc.read(table_name="nos", table_cols=("date", "text"), date=str(date))
            for col in cols:
                date, text = col
                text = text.encode('latin-1').decode('utf-8')
                words = re.findall(r'\b\w+\b', text.lower())
                word_freq = Counter(words)
                all_word_freq += word_freq

    print(all_word_freq)
    with open(f'..\\resources\\data\\word_freq_{start_date}+{end_date}.pickle', 'wb') as f:
        pk.dump(word_freq, f, protocol=pk.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
