'''Database backend.'''

from __future__ import annotations
import os
from typing import Generator
from typing import NamedTuple
from logging import getLogger
from pathlib import Path

from ._database import SQLTable

__all__ = [
    'MainSchema',
    'get_imagepaths',
    'initialize_database',
    'insert_data',
    'exist_database',
]

logger = getLogger(__name__)


##
DIRECTORY = Path(os.getenv('DIR_FIGHND', ''))


class MainSchema(NamedTuple):
    id: int = 0
    filename: str = ''
    directory: str = ''
    caption: str = ''
    citation: str = ''
    explanation: str = ''
    tags: str = ''
    thumbnail: bytes = b''

    def _for_log(self) -> MainSchema:
        '''Change self to simble contents just for log.'''
        return self._replace(thumbnail=b'...')


def select_a_record(_id: int) -> MainSchema:
    '''Return all data.'''
    name_table = 'Images'
    with SQLTable(name_table) as t:
        data = t.select('*', where=f'id = {_id}')[0]
    return MainSchema(*data)


def get_alldata() -> list[MainSchema]:
    '''Return all data.'''
    name_table = 'Images'
    with SQLTable(name_table) as t:
        data = t.selectall()
    return [MainSchema(*d) for d in data]


def get_imagepaths() -> Generator[Path, None, None]:
    '''Return image path list.'''
    name_table = 'Images'
    with SQLTable(name_table) as t:
        dirs = t.select('directory')
    return (Path(d).absolute() for d in dirs)


def exist_database() -> bool:
    '''Check whether database exists.'''
    return Path(SQLTable.dbname).exists()


def initialize_database() -> None:
    '''Init db by creating database and tables.'''
    name_table = 'Images'

    with SQLTable(name_table) as t:
        assert not t.exist()
        t.create_table(**MainSchema()._asdict())


def insert_data(schema: MainSchema) -> int:
    '''Insert data to database and Return id.'''
    name_table = 'Images'
    with SQLTable(name_table) as t:
        _id = t.insert(**schema._asdict())
        t.con.commit()
    return _id


def update_data(schema: MainSchema) -> None:
    '''Update data in database.'''
    name_table = 'Images'
    with SQLTable(name_table) as t:
        t.update(ID=schema.id, columns=schema._asdict())
        t.con.commit()
