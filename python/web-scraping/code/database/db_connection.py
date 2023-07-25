import sqlite3


class DBConnection:

    DB_NAME = '..\\..\\resources\\data\\nos_data.db'

    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.DB_NAME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    connection = DBConnection()

    with connection as db:
        print(connection.connection)
