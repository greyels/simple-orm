#! /mnt/c/PP/python/simple_orm/venv/bin/python3

import sqlite3

__all__ = ['Model', 'CharCol', 'IntCol']

class SqliteDB():
    database = 'sqlite.db'

class Model():

    def __init__(self, **kwargs):
        conn = self.create_connection(SqliteDB.database)
        cur = conn.cursor()
        columns = ', '.join(kwargs.keys())
        values = str(tuple([(kwargs[key]) for key in kwargs.keys()]))
        sql = 'INSERT INTO ' + self.__class__.__name__ + \
              ' (' + columns + ') VALUES ' + values
        print(sql)
        cur.execute(sql)
        self.rowid = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def create_connection(database):
        try:
            return sqlite3.connect(database)
        except Error as er:
            print(er)
        return None

    @classmethod
    def create_table(cls):
        conn = cls.create_connection(SqliteDB.database)
        cur = conn.cursor()
        attrs = (attr for attr in dir(cls) 
            if not callable(getattr(cls, attr)) and not attr.startswith("__"))
        columns = []
        for attr in attrs:
            columns.append(f'{attr} {getattr(cls, attr).ctype}')
        columns = str(tuple(columns)).replace("'", "")
        sql = 'CREATE TABLE IF NOT EXISTS ' + cls.__name__ + columns
        print(sql)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return

    def db_connect(func):
        def decorated(self, **kwargs):
            conn = self.create_connection(SqliteDB.database)
            cur = conn.cursor()
            result = func(self, cur, conn, **kwargs)
            cur.close()
            conn.close()
            return result
        return decorated

    @db_connect
    def read(self, cur, conn):
        sql = 'SELECT ' + str(self.rowid) + ', * FROM ' + self.__class__.__name__
        print(sql)
        cur.execute(sql)
        row = cur.fetchone()
        col_names = [description[0] for description in cur.description]
        for idx, val in enumerate(col_names[1:]):
            setattr(self, val, row[idx+1])
        return

    @db_connect
    def update(self, cur, conn, **kwargs):
        updates = ', '.join([f'{k} = "{v}"' for k, v in kwargs.items()])
        sql = 'UPDATE ' + self.__class__.__name__ + \
              ' SET ' +  updates + ' WHERE ROWID = ' + str(self.rowid)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return
        
    @db_connect
    def delete(self, cur, conn):
        sql = 'DELETE FROM Client' + \
              ' WHERE ROWID = ' + str(self.rowid)
        print(sql)
        cur.execute(sql)
        conn.commit()
        return


class CharCol():

    def __init__(self):
        self.ctype = 'TEXT'


class IntCol():

    def __init__(self):
        self.ctype = 'INT'
