'''Database backend.'''

from __future__ import annotations
import os
from typing import Generator
from logging import getLogger
from pathlib import Path
import numpy as np

__all__ = ['get_imagepaths']

logger = getLogger(__name__)


##
DIRECTORY = Path(os.getenv('DIR_FIGHND', ''))


def get_imagepaths() -> Generator[Path, None, None]:
    '''Return image path list.'''
    return DIRECTORY.iterdir()
