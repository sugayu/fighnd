'''Base, gallery view front end.'''

import asyncio
from logging import getLogger
from pathlib import Path
from dataclasses import dataclass, field

import flet as ft

from .share import selectedimage
from .. import backend

logger = getLogger(__name__)

__all__ = [
    'imageview',
]


##
ROUTE = '/fig'


@ft.component
def imageview() -> ft.View:
    logger.info('ImageView')

    # data, _ = ft.use_state(
    #     SelectedDataContainer(
    #         path_image=Path(''),
    #         filename='',
    #         explanation='This is explanation',
    #         citation='Citation',
    #         tags=['tagA', 'tagB'],
    #     )
    # )
    data = selectedimage.data

    controls = [
        ft.AppBar(
            title=ft.Text(data.filename),
            bgcolor=ft.Colors.SURFACE_DIM,
        ),
        ft.Row(
            controls=[mainimage_button(data.path_image)],
            alignment=ft.MainAxisAlignment.CENTER,
            # scroll="always",
            # wrap=True,
        ),
        ft.Text(data.explanation),
        ft.Text(data.citation),
        ft.Text('; '.join(data.tags)),
    ]

    return ft.View(
        route=ROUTE, controls=controls, width=1200, scroll=ft.ScrollMode.ALWAYS
    )


@ft.observable
@dataclass
class SelectedDataContainer:
    path_image: Path = Path('')
    filename: str = ''
    explanation: str = 'This is explanation'
    citation: str = 'Citation'
    tags: list[str] = field(default_factory=list)

    def set(self, fname: Path) -> None:
        logger.info('Setter')
        self.path_image = fname
        self.filename = fname.name


@dataclass
class MainImageConfig:
    width: int
    height: int


MainImageConfigContext = ft.create_context(MainImageConfig(width=600, height=500))


@ft.component
def mainimage_button(datapath: Path) -> None:
    '''Main image with a button function.'''

    config = ft.use_context(MainImageConfigContext)

    img = ft.Image(
        src=str(datapath.absolute()),
        width=config.width,
        height=config.height,
        fit=ft.BoxFit.CONTAIN,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.BorderRadius.all(10),
    )
    button = ft.Button(
        content='',
        on_click=lambda _: backend.pop_clipboard(datapath),
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            overlay_color={
                ft.ControlState.PRESSED: ft.Colors.BLUE_300,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            shape=ft.RoundedRectangleBorder(radius=1),
            elevation=0,
        ),
        width=config.width,
        height=config.height,
        opacity=0.5,
    )
    return ft.Stack([img, button])


selectedimage.data = SelectedDataContainer()
