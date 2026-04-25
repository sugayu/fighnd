'''Image process functions'''

from __future__ import annotations
from logging import getLogger
from PIL import Image
from io import BytesIO

__all__ = ['get_thumbnail']

logger = getLogger(__name__)


##
def get_thumbnail(fname_image) -> bytes:
    '''Convert an input image to thumbnail.'''
    img = Image.open(fname_image, 'r')
    thumbnail_size = (128, 128)
    img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
    thumbnail = BytesIO()
    img.save(thumbnail, 'PNG')
    return thumbnail.getvalue()
