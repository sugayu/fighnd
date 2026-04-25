'''I/O interface to OS.'''

from __future__ import annotations
import sys
from logging import getLogger
from pathlib import Path
import datetime
import subprocess
import shutil

import flet as ft

from .. import path
from .. import backend

__all__ = ['open_image', 'pop_clipboard', 'pick_file', 'save_file']

logger = getLogger(__name__)


##
imageviewer = {
    'linux': 'xdg-open',
    'wind32': 'explorer',
    'darwin': 'open',
}[sys.platform]


def open_image(self, path: Path) -> None:
    '''Open image with a default viewr.'''
    subprocess.Popen([imageviewer, path])


def pop_clipboard(path: Path) -> None:
    # image = Image.open(path)
    # # num_byteio = io.BytesIO()
    # # num_byteio.save(image, 'jpeg')
    # # pyperclip.copy(num_byteio.getvalue())
    # data = image.tobytes("jpeg")
    # pyperclip.copy(data)
    # # txt = str(path.absolute())
    # # subprocess.Popen(['pbcopy', '<', txt])
    # # task = subprocess.Popen(['pbcopy', '<', txt], close_fds=True)
    # # task.communicate(input=txt.encode('utf-8'))
    subprocess.Popen(['picclip', path])


async def pick_file() -> str:
    '''Pick and Save files then Move to the edit mode.'''
    file_picker = ft.FilePicker()
    fname = await file_picker.pick_files(allow_multiple=False)
    if not fname:
        logger.info('No file was selected.')
        return ''
    # self.selected_files.value = ", ".join([f.path for f in files])
    return fname[0].path


def pick_files_result(self, e: ft.Event):
    '''Pick files dialog

    Note:
        DEPRECATED
    '''

    if not e.files:
        return

    self.selected_files.value = ", ".join([f.path for f in e.files])
    self.selected_files.update()


def save_file(fname_original: str) -> backend.database.MainSchema:
    '''Save a file to the auto-created path.'''
    fpath_original = Path(fname_original)
    newfpath = create_newfilepath(fpath_original)

    newfpath.parent.mkdir(exist_ok=True)
    shutil.move(fpath_original, newfpath)

    schema = backend.database.MainSchema(
        filename=newfpath.name,
        directory=str(newfpath.parent),
    )
    _id = backend.database.insert_data(schema)
    logger.info(f'new ID: {_id}')
    return backend.database.select_a_record(_id)


def create_newfilepath(fpath_original: Path) -> Path:
    '''Create a new file path base on the date.'''
    now = datetime.datetime.now()
    dpath = path / now.strftime('%Y%m')
    fname = now.strftime('%Y%m%d%H%M%S') + fpath_original.suffix
    return dpath / fname


def handle_save_file(self, e: ft.Event[ft.Button]) -> None:
    '''Save file.'''
    self.save_file_path.value = ft.FilePicker().save_file()
    # e.path if e.path else "Cancelled!"
    self.save_file_path.update()


def save_file_result(self, e: ft.Event):
    '''Save file dialog

    Note:
        DEPRECATED
    '''

    self.save_file_path.value = e.path if e.path else "Cancelled!"
    self.save_file_path.update()
