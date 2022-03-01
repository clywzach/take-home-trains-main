import sqlite3

class Connection:
    def get_db_connection():
        conn = sqlite3.connect('database/traindatabase.db')
        conn.row_factory = sqlite3.Row
        return conn