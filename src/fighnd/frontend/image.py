'''Base, gallery view front end.'''

import asyncio
from typing import Callable
from logging import getLogger
from pathlib import Path
from dataclasses import dataclass, field
from copy import deepcopy

import flet as ft

from .share import selectedimage
from .. import backend
from ..backend import database

logger = getLogger(__name__)

__all__ = ['imageview']


##
ROUTE = '/fig'


# @ft.observable
@dataclass
class SelectedDataContainer:
    path_image: Path = Path('')
    id: int = 0
    filename: str = ''
    caption: str = 'This is caption'
    citation: str = 'Citation'
    explanation: str = 'This is explanation'
    tags: list[str] = field(default_factory=list)
    thumbnail: bytes = b''
    editable_mode: bool = False

    def set(self, data: database.MainSchema) -> None:
        logger.info('Setter of SelectedDataContainer')
        self.id = data.id
        self.path_image = Path(data.directory) / data.filename
        self.filename = data.filename
        self.caption = data.caption
        self.citation = data.citation
        self.explanation = data.explanation
        self.tags = [data.tags]
        self.thumbnail = data.thumbnail

    def dump(self) -> database.MainSchema:
        logger.info('Dump')
        return database.MainSchema(
            id=self.id,
            filename=self.filename,
            directory=str(self.path_image.parent),
            caption=self.caption,
            citation=self.citation,
            explanation=self.explanation,
            tags=','.join(self.tags),
            thumbnail=self.thumbnail,
        )

    def set_filename(self, fname: str) -> None:
        '''Set both filename and path.'''
        self.filename = fname
        self.path_image = self.path_image.with_name(fname)


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
    controls = frame_main()

    return ft.View(
        route=ROUTE, controls=[controls], width=1200, scroll=ft.ScrollMode.ALWAYS
    )


@ft.component
def frame_main() -> ft.Column:
    '''Main frame of imageview.'''
    _data: SelectedDataContainer = selectedimage.data
    editable_mode, set_editable_mode = ft.use_state(_data.editable_mode)
    _data.editable_mode = editable_mode

    data = deepcopy(_data) if editable_mode else _data

    def save_data():
        database.update_data(data.dump())
        backend.io.move(_data.path_image, data.path_image)
        selectedimage.data = data

    appbar = frame_appbar(data, editable_mode)
    main_image = ft.Row(
        controls=[mainimage_button(data.path_image)],
        alignment=ft.MainAxisAlignment.CENTER,
        # scroll="always",
        # wrap=True,
    )
    menu = frame_menu(editable_mode, set_editable_mode, save_data)
    info = frame_info(data, editable_mode)
    return ft.Column(controls=[appbar, main_image, menu, info])


@ft.component
def frame_appbar(data: SelectedDataContainer, editable_mode: bool) -> ft.Column:
    '''Application bar.'''

    if editable_mode:

        fname = Path(data.filename)

        def set_textfield(e: ft.Event):
            data.set_filename(e.control.value + fname.suffix)

        return ft.AppBar(
            title=ft.TextField(
                value=fname.stem,
                suffix=fname.suffix,
                on_blur=set_textfield,
            ),
            bgcolor=ft.Colors.SURFACE_DIM,
        )
    else:
        return ft.AppBar(
            title=ft.Text(data.filename),
            bgcolor=ft.Colors.SURFACE_DIM,
        )


@ft.component
def frame_info(data: SelectedDataContainer, editable_mode: bool) -> ft.Column:
    '''Infomation fame.'''

    def set_textfield(e: ft.Event):
        setattr(data, e.control.label, e.control.value)

    if editable_mode:
        controls = [
            ft.TextField(
                label='explanation', value=data.explanation, on_blur=set_textfield
            ),
            ft.TextField(label='citation', value=data.citation, on_blur=set_textfield),
            ft.TextField(
                label='tag', value='; '.join(data.tags), on_blur=set_textfield
            ),
        ]
    else:
        controls = [
            ft.Text(data.explanation),
            ft.Text(data.citation),
            ft.Text('; '.join(data.tags)),
        ]
    return ft.Column(
        controls=controls,
        alignment=ft.MainAxisAlignment.START,
    )


@ft.component
def frame_menu(
    editable_mode: bool, set_editable_mode: Callable, func_save: Callable
) -> ft.Column:
    '''Menu fame.'''
    if editable_mode:

        def save(e: ft.Event):
            func_save()
            set_editable_mode(False)

        controls = [ft.Button('Save', icon=ft.Icons.SAVE, on_click=save)]

    else:
        controls = [
            ft.Button(
                'Edit', icon=ft.Icons.EDIT, on_click=lambda _: set_editable_mode(True)
            ),
        ]

    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.START,
    )


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
