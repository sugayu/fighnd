'''Database basics.'''

from __future__ import annotations
from typing import Any, Sequence, TypeVar
import os
from logging import getLogger
from pathlib import Path
import sqlite3
from .. import config

__all__ = ['SQLTable']

logger = getLogger(__name__)


##
class SQLTable:
    '''Table connection.'''

    types = {
        None: 'NULL',
        int: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BLOB',
    }

    dbname = config.homepath / 'development.db'

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

        logger.info(f'sql> {sql}')
        self.cur.execute(sql)

    def insert(self, **kwargs) -> int:
        collist = [c[1] for c in self.collist()]
        cols = '(' + ','.join(collist[1:]) + ')'
        sql = f'INSERT INTO {self.tname} {cols} VALUES('
        values: list[Any] = []
        for col in collist[1:]:
            sql += ', ?'
            if col in kwargs.keys():
                values.append(kwargs[col])
            else:
                values.append(None)
            # if col[1] in kwargs.keys():
            #     if col[2] == 'TEXT':
            #         v = f'"{kwargs[col[1]]}"'
            #     elif col[2] == 'BLOB':
            #         v = 'null'
            #     else:
            #         v = kwargs[col[1]]
            #     sql += f', {v}'
            # else:
            #     sql += ', null'
        sql += ') RETURNING id'
        sql = sql.replace(', ', '', 1)

        _values = [v if not isinstance(v, bytes) else b'...' for v in values]
        logger.info(f'sql> {sql}')
        logger.info(f'values: {_values}')
        self.cur.execute(sql, values)
        return self.cur.fetchone()[0]

    def collist(self) -> Sequence:
        sql = f'PRAGMA table_info({self.tname})'
        self.cur.execute(sql)
        logger.info(f'sql> {sql}')
        return list(self.cur.fetchall())

    def exist(self) -> bool:
        sql = 'SELECT name FROM sqlite_master WHERE type="table"'
        tables = self.cur.execute(sql).fetchall()
        logger.info(f'sql> {sql}')
        return self.tname in [t[0] for t in tables]

    def select(self, columns: str | list[str], where: None | str = None) -> list:
        '''Select data.'''
        colnames = columns if isinstance(columns, str) else ', '.join(columns)
        sql = f'SELECT {colnames} FROM {self.tname}'
        if where is not None:
            sql += f' WHERE {where}'
        logger.info(f'sql> {sql}')
        return list(self.cur.execute(sql).fetchall())

    def selectall(self) -> list:
        sql = f'SELECT * FROM {self.tname}'
        logger.info(f'sql> {sql}')
        return list(self.cur.execute(sql).fetchall())

    def delete(self, ID: int) -> None:
        sql = f'DELETE FROM {self.tname} WHERE id = {ID}'
        logger.info(f'sql> {sql}')
        self.cur.execute(sql)

    def update(self, ID: int, columns: dict) -> None:
        sql = f'UPDATE {self.tname}'
        kw, values = '', []
        collist = [c[1] for c in self.collist()]
        for k, v in columns.items():
            if k.upper() == 'ID':
                continue
            if not v:
                continue
            if k.lower() not in collist:
                msg = (
                    'No input colname in table: '
                    f'Input: {k.lower()}, but Schema: {collist}.'
                )
                logger.warning(msg)
                continue
            kw += f',{k} = ?'
            values.append(v)
        sql += ' SET ' + kw[1:]
        sql += f' WHERE id = {ID}'

        _values = [v if not isinstance(v, bytes) else b'...' for v in values]
        logger.info(f'sql> {sql}')
        logger.info(f'values={_values}')
        self.cur.execute(sql, values)

    def commit(self) -> None:
        self.con.commit()
