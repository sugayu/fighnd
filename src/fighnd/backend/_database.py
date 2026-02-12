'''Database basics.'''

from __future__ import annotations
import os
from logging import getLogger
from pathlib import Path
import sqlite3

__all__ = ['SQLTable']

logger = getLogger(__name__)


##
DIRECTORY = Path(os.getenv('DIR_FIGHND', ''))


class SQLTable:
    '''Table connection.'''

    types = {
        None: 'NULL',
        int: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BLOB',
    }

    dbname = DIRECTORY / 'development.db'

    def __init__(self, tablename: str) -> None:
        self.tname = tablename

    def open(self) -> None:
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()

    def close(self) -> None:
        self.con.close()

    def __enter__(self) -> SQLTable:
        self.open()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()

    def create_table(self, **kwargs) -> None:
        sql = f'CREATE TABLE {self.tname} ('
        for key, value in kwargs.items():
            sql += f', {key} ' + f'{self.types[type(value)]}'.upper()
            if key.lower() == 'id':
                sql += ' PRIMARY KEY AUTOINCREMENT'
        sql += ')'
        sql = sql.replace(', ', '', 1)

        logger.info(f'SQL: {sql}')
        self.cur.execute(sql)

    def insert(self, **kwargs) -> None:
        sql = f'INSERT INTO {self.tname} VALUES('
        for col in self.collist():
            if col[1] in kwargs.keys():
                v = f'"{kwargs[col[1]]}"' if col[2] == 'TEXT' else kwargs[col[1]]
                sql += f', {v}'
            else:
                sql += ', null'
        sql += ')'
        sql = sql.replace(', ', '', 1)

        logger.info(f'SQL: {sql}')
        self.cur.execute(sql)

    def collist(self) -> list:
        sql = f'PRAGMA table_info({self.tname})'
        self.cur.execute(sql)
        logger.info(f'SQL: {sql}')
        return list(self.cur.fetchall())

    def exist(self) -> bool:
        sql = 'SELECT name FROM sqlite_master WHERE type="table"'
        tables = self.cur.execute(sql).fetchall()
        logger.info(f'SQL: {sql}')
        return self.tname in [t[0] for t in tables]

    def select(self, columns: str | list[str], where: None = None) -> list:
        '''Select data.'''
        colnames = columns if isinstance(columns, str) else ', '.join(columns)
        sql = f'SELECT {colnames} FROM {self.tname}'
        if where is not None:
            sql += f' WHERE {where}'
        logger.info(f'SQL: {sql}')
        return list(self.cur.execute(sql).fetchall())

    def selectall(self) -> list:
        sql = f'SELECT * FROM {self.tname}'
        logger.info(f'SQL: {sql}')
        return list(self.cur.execute(sql).fetchall())

    def delete(self, ID: int) -> None:
        sql = f'DELETE FROM {self.tname} WHERE id = {ID}'
        logger.info(f'SQL: {sql}')
        self.cur.execute(sql)

    def commit(self) -> None:
        self.con.commit()
