'''Shared data.'''

from __future__ import annotations
from typing import Any
from dataclasses import dataclass
from logging import getLogger


__all__ = ['selectedimage']

logger = getLogger(__name__)


##
@dataclass
class SharedBox:
    '''Input anything.'''

    data: Any = None


selectedimage = SharedBox()
