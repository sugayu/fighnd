from pathlib import Path
from . import config
from logging import getLogger

__version__ = '0.0.0'

logger = getLogger(__name__)
logger.info(f'HOMEPATH: {config.homepath}')
config.homepath.mkdir(exist_ok=True)
