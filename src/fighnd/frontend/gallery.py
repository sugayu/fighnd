'''Base, gallery view front end.'''

import os
import asyncio
from logging import getLogger
from pathlib import Path
from dataclasses import dataclass

import flet as ft

from .image import ROUTE as route_image
from .share import selectedimage
from .. import backend
from ..backend import database
from .. import config

__all__ = [
    'galleryview',
]


logger = getLogger(__name__)

##
ROUTE = '/'


@ft.component
def galleryview() -> ft.View:
    controls = [functions(), gallery()]
    return ft.View(
        route=ROUTE,
        controls=controls,
        width=config.frame_width,
    )


@ft.component
def functions() -> ft.Control:
    '''Functional item list to manipulate the app and images.'''

    button_add = ft.Button(
        "Add a new image",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=add_new_file,
    )
    # button_save = ft.Button(
    #     "Save file",
    #     icon=ft.Icons.SAVE,
    #     # on_click=lambda _: backend.save_file_dialog.save_file(),
    #     # disabled=page.web,
    # )

    return ft.Row(controls=[button_add])


async def add_new_file(e: ft.Event[ft.Button]) -> None:
    '''Pick and Save files then Move to the edit mode.'''
    fname_pick = await backend.pick_file()
    if not fname_pick:
        logger.info('No file was picked.')
        return

    logger.info(f'Picked file: {fname_pick}')
    record = backend.save_file(fname_pick)
    logger.info(f'New record: {record._log}')

    logger.info('Change page to /fig')
    selectedimage.data.set(record)
    selectedimage.data.editable_mode = True
    asyncio.create_task(ft.context.page.push_route(route_image))


@ft.component
def gallery() -> ft.Control:
    '''Main gallery.'''

    data = database.get_alldata()
    controls = [thumbnailbutton(d) for d in data]

    images = ft.Row(
        width=config.frame_width,
        wrap=True,
        scroll='always',
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=config.gallery_spacing,
        run_spacing=config.gallery_run_spacing,
        controls=controls,
    )

    return ft.Column(
        # width=1200,
        height=config.frame_height,
        controls=[images],
        scroll='always',
        alignment=ft.MainAxisAlignment.CENTER,
    )


@dataclass
class ThumbnailConfig:
    width: int
    height: int
    inner_ratio: float = 0.90

    def __post_init__(self) -> None:
        self.inner_width = self.width * self.inner_ratio
        self.inner_height = self.width * self.inner_ratio


ThumbnailConfigContext = ft.create_context(
    ThumbnailConfig(
        width=config.gallery_thumnail_size[0],
        height=config.gallery_thumnail_size[1],
    )
)


@ft.component
def thumbnailbutton(data: database.MainSchema) -> ft.Control:
    '''Image thumbnail button component.'''

    thumbconfig = ft.use_context(ThumbnailConfigContext)
    fname = Path(data.directory) / data.filename
    if not fname.exists():
        logger.warning(f'No image exists: {fname}')

    def _select_image():
        logger.info('change_page')
        selectedimage.data.set(data)
        selectedimage.data.editable_mode = False
        asyncio.create_task(ft.context.page.push_route(route_image))

    # open_dialog = OpenImageDialog(fname)

    img = ft.Image(
        # src=str(fname.absolute()),
        src=data.thumbnail,
        width=thumbconfig.inner_width,
        height=thumbconfig.inner_height,
        fit=ft.BoxFit.COVER,
        repeat=ft.ImageRepeat.NO_REPEAT,
        border_radius=ft.BorderRadius.all(config.gallery_border_radius),
    )
    button = ft.Button(
        content='',
        # content=img,
        # on_click=open_dialog,
        on_click=_select_image,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            overlay_color={
                ft.ControlState.PRESSED: ft.Colors.BLUE_300,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            shape=ft.RoundedRectangleBorder(radius=config.gallery_border_radius),
            elevation=0,
        ),
        width=thumbconfig.inner_width,
        height=thumbconfig.inner_height,
        opacity=config.gallery_button_opacity,
    )
    stack = ft.Stack(
        [img, button],
        alignment=ft.Alignment.CENTER,
    )
    return ft.Card(
        content=stack,
        shadow_color=ft.Colors.GREY_600,
        bgcolor=ft.Colors.GREY_300,
        width=thumbconfig.width,
        height=thumbconfig.height,
        shape=ft.RoundedRectangleBorder(radius=config.gallery_border_radius),
    )


# class TopView(ft.View):
#     '''Top page view of the application.'''

#     ROUTE = '/'

#     def __init__(self, controls=None, **kwargs) -> None:
#         # self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
#         # self.save_file_dialog = ft.FilePicker(on_result=self.save_file_result)
#         self.selected_files = ft.Text()
#         self.save_file_path = ft.Text()

#         # Image gallary

#         if controls is None:
#             controls = [
#                 ft.AppBar(
#                     title=ft.Text("TopView"), bgcolor=ft.Colors.ON_SURFACE_VARIANT
#                 ),
#                 ft.Row([button_upload, self.selected_files]),
#                 ft.Row([button_save, self.save_file_path]),
#             ]
#         super().__init__(route=self.ROUTE, controls=controls, **kwargs)
