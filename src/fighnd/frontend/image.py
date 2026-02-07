'''Base, gallery view front end.'''

import os
import asyncio
from logging import getLogger
from pathlib import Path
from dataclasses import dataclass

import flet as ft

from .. import backend

__all__ = [
    'imageview',
]


##
ROUTE = '/fig'


@ft.component
def imageview() -> ft.View:
    controls = [
        ft.Button(
            'Return',
            on_click=lambda _: asyncio.create_task(ft.context.page.push_route('/')),
        )
    ]
    return ft.View(
        route=ROUTE,
        controls=controls,
        width=1200,
    )


@dataclass
class DataContainer:
    path_image: Path
    filename: str
    explanation: str
    citation: str
    tags: list[str]
