import sqlite3


class DBConnection:

    DB_NAME = '..\\..\\resources\\data\\nos_data.db'
    INSERT_QUERY = 'INSERT INTO {0} ({1}) VALUES ({2})'

    def __init__(self):
        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def write(self, db_name, db_cols, data):
        cols = ""
        values = ""

        for col in db_cols:
            cols += f"{col}, "
            values += "?, "

        query = self.INSERT_QUERY.format(db_name, cols, values)
        print(query)

        self.cursor.executemany(query, data)


if __name__ == '__main__':
    connection = DBConnection()

    with connection as db:
        print(connection.connection)
