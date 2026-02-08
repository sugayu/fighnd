'''I/O interface to OS.'''

from __future__ import annotations
import sys
from logging import getLogger
from pathlib import Path
import subprocess

__all__ = ['open_image', 'pop_clipboard']

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
