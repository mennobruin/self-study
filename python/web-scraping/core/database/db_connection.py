import sqlite3


class DBConnection:

    DB_NAME = '..\\..\\resources\\data\\scrape_data.db'
    INSERT_QUERY = 'INSERT INTO {0} ({1}) VALUES ({2})'

    def __init__(self):
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def write(self, table_name, table_cols, data):
        cols = ""
        values = ""

        for col in table_cols:
            cols += f"{col},"
            values += "?,"

        query = self.INSERT_QUERY.format(table_name, cols[:-1], values[:-1])
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (date TEXT, headline TEXT, link TEXT, text TEXT)')
        self.cursor.executemany(query, (data,))


if __name__ == '__main__':
    connection = DBConnection()

    with connection as db:
        print(connection.connection)
