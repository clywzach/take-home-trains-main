import sqlite3

class Database:

    def get(self, key, connection):
        schedule = []
        try:
            connection.isolation_level = 'EXCLUSIVE'
            connection.execute('BEGIN EXCLUSIVE')
            statement = "SELECT * FROM trainschedule WHERE id = ?"
            cur = connection.cursor()
            cur.execute(statement,(key,))
            value = cur.fetchall()
        except sqlite3.Error:
            raise
        else:
            for time in value:
                schedule.append(time[1])

        return schedule

    def set(self, key, val, connection):
        try:
            connection.isolation_level = 'EXCLUSIVE'
            connection.execute('BEGIN EXCLUSIVE')
            statement = "INSERT INTO trainschedule (id,time) VALUES (?, ?)"
            cur = connection.cursor()
            cur.execute(statement,(key, val))
            connection.commit()
        except sqlite3.Error:
            raise

    def keys(self, connection):
        keys = []
        try:
            connection.isolation_level = 'EXCLUSIVE'
            connection.execute('BEGIN EXCLUSIVE')
            statement = "SELECT id FROM trainline"
            cur = connection.cursor()
            cur.execute(statement)
            value = cur.fetchall()
        except sqlite3.Error:
            raise
        else:
            for row in value:
                keys.append(row[0])

        return keys

    def set_trainline(self, key, val, connection):
        try:
            connection.isolation_level = 'EXCLUSIVE'
            connection.execute('BEGIN EXCLUSIVE')
            statement = "INSERT INTO trainline (id,stationid) VALUES (?, ?)"
            cur = connection.cursor()
            cur.execute(statement,
                (key, val))
            connection.commit()
        except sqlite3.Error:
            raise